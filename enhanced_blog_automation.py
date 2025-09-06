#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
개선된 블로그 자동화 시스템 v2.0
- 다양한 토픽 생성
- 고품질 콘텐츠 생성
- 중복 방지 시스템
- 이미지 처리 개선
"""

import os
import json
import hashlib
import random
from datetime import datetime, timedelta
import requests
import google.generativeai as genai
from typing import Dict, List, Optional
import time

class ImprovedBlogAutomation:
    def __init__(self):
        self.config = self.load_config()
        self.history_file = "post_history.json"
        self.history = self.load_history()
        
    def load_config(self) -> Dict:
        """설정 로드"""
        config = {
            'google_client_id': os.environ.get('GOOGLE_CLIENT_ID', ''),
            'google_client_secret': os.environ.get('GOOGLE_CLIENT_SECRET', ''),
            'blog_id': os.environ.get('BLOGGER_BLOG_ID', ''),
            'gemini_api_key': os.environ.get('GEMINI_API_KEY', '')
        }
        
        # Gemini API 설정 - 최신 모델 사용
        if config['gemini_api_key']:
            genai.configure(api_key=config['gemini_api_key'])
            # gemini-1.5-flash 사용 (더 빠르고 효율적)
            self.model = genai.GenerativeModel('gemini-1.5-flash')
        else:
            raise ValueError("Gemini API 키가 필요합니다")
        
        # 토큰 정보 로드
        try:
            with open('blogger_token.json', 'r', encoding='utf-8') as f:
                config['token_data'] = json.load(f)
        except FileNotFoundError:
            print("⚠️ blogger_token.json이 없습니다. 새로 생성합니다.")
            config['token_data'] = None
            
        return config
    
    def load_history(self) -> List[Dict]:
        """포스팅 히스토리 로드"""
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def save_history(self, post_data: Dict):
        """포스팅 히스토리 저장"""
        self.history.append(post_data)
        # 최근 100개만 유지
        if len(self.history) > 100:
            self.history = self.history[-100:]
        
        with open(self.history_file, 'w', encoding='utf-8') as f:
            json.dump(self.history, f, ensure_ascii=False, indent=2)
    
    def generate_dynamic_topic(self) -> str:
        """다양하고 창의적인 토픽 생성"""
        # 기본 주제 카테고리 (대폭 확장)
        base_topics = [
            "AI 프롬프트 엔지니어링", "ChatGPT 활용법", "Claude 사용 팁", 
            "Gemini 고급 기능", "AI 이미지 생성", "AI 음악 제작",
            "AI 코딩 도우미", "AI 글쓰기 비법", "AI 번역 활용",
            "AI 데이터 분석", "머신러닝 기초", "딥러닝 입문",
            "AI 윤리와 미래", "AI 비즈니스 활용", "AI 교육 혁신",
            "AI 창작 도구", "AI 자동화 시스템", "AI 트렌드 분석",
            "Perplexity 검색 팁", "Midjourney 사용법", "Stable Diffusion 가이드",
            "AI 영상 편집", "AI 프레젠테이션", "AI 마케팅 전략",
            "노코드 AI 도구", "AI API 활용", "AI 플러그인 추천",
            "AI 보안과 프라이버시", "AI 협업 도구", "AI 생산성 향상"
        ]
        
        # 수식어/관점 (다양한 각도)
        modifiers = [
            "2025년 최신", "초보자를 위한", "전문가가 알려주는",
            "실전", "5분 마스터", "완전정복", "핵심정리",
            "실수하지 않는", "효율 200% 높이는", "무료로 시작하는",
            "비용 절감", "시간 단축", "퀄리티 높이는", "창의적인",
            "실무 적용", "케이스 스터디", "비교 분석", "심화 학습",
            "트러블슈팅", "최적화 가이드", "성공 사례", "실패 극복",
            "단계별", "체크리스트", "꿀팁 모음", "숨겨진 기능"
        ]
        
        # 타겟 대상
        targets = [
            "직장인", "학생", "창업자", "프리랜서", "개발자",
            "디자이너", "마케터", "교육자", "연구원", "콘텐츠 크리에이터",
            "블로거", "유튜버", "작가", "기획자", "중장년층",
            "입문자", "중급자", "고급 사용자", "팀리더", "스타트업"
        ]
        
        # 특별 포맷
        formats = [
            "가이드", "체크리스트", "비교 분석", "Q&A",
            "인터뷰", "후기", "리뷰", "튜토리얼", "팁 모음",
            "사례 연구", "실험 결과", "벤치마크", "로드맵", "전략"
        ]
        
        # 랜덤 조합으로 독특한 토픽 생성
        topic_patterns = [
            f"{random.choice(modifiers)} {random.choice(base_topics)} {random.choice(formats)}",
            f"{random.choice(targets)}을 위한 {random.choice(base_topics)} {random.choice(formats)}",
            f"{random.choice(base_topics)} - {random.choice(modifiers)} {random.choice(formats)}",
            f"{random.choice(base_topics)}: {random.choice(targets)}의 {random.choice(formats)}",
            f"[{datetime.now().strftime('%Y년 %m월')}] {random.choice(base_topics)} {random.choice(modifiers)} 정리"
        ]
        
        return random.choice(topic_patterns)
    
    def check_duplicate(self, title: str, content: str) -> bool:
        """중복 콘텐츠 체크"""
        # 제목 해시
        title_hash = hashlib.md5(title.encode()).hexdigest()
        
        # 콘텐츠 첫 500자 해시 (간단한 중복 체크)
        content_preview = content[:500] if len(content) > 500 else content
        content_hash = hashlib.md5(content_preview.encode()).hexdigest()
        
        for post in self.history:
            # 제목이 너무 유사한 경우
            if 'title_hash' in post and post['title_hash'] == title_hash:
                return True
            
            # 같은 주제를 24시간 내 다시 다룬 경우
            if 'timestamp' in post:
                post_time = datetime.fromisoformat(post['timestamp'])
                if (datetime.now() - post_time).total_seconds() < 86400:
                    if 'topic' in post and title.lower() in post['topic'].lower():
                        return True
        
        return False
    
    def get_quality_image_url(self, keyword: str) -> str:
        """고품질 이미지 URL 생성 (다양한 소스)"""
        # Unsplash API (더 많은 이미지, 실시간)
        unsplash_collections = {
            "ai_tech": [
                "photo-1677442136019-21780ecad995",
                "photo-1686191128892-3b5fdc17b7bf", 
                "photo-1655635643532-b47e63c4a580",
                "photo-1664906225771-ad618ea1fee8",
                "photo-1675271591211-41ae13f0e71f",
                "photo-1620712943543-bcc4688e7bd0"
            ],
            "workspace": [
                "photo-1498050108023-c5249f4df085",
                "photo-1521737604893-d14cc237f11d",
                "photo-1581091226825-a6a2a5aee158",
                "photo-1518770660439-4636190af475",
                "photo-1461749280684-dccba630e2f6",
                "photo-1504639725590-34d0984388bd"
            ],
            "learning": [
                "photo-1513258496099-48168024aec0",
                "photo-1501504905252-473c47e087f8",
                "photo-1522202176988-66273c2fd55f",
                "photo-1517245386807-d1c09bbb0fd4",
                "photo-1523050854058-8df90110c9f1",
                "photo-1507003211169-0a1dd7228f2d"
            ],
            "creative": [
                "photo-1626785774573-e9d366118b80",
                "photo-1618005182384-a83a8bd57fbe",
                "photo-1559028012-481c04fa702d",
                "photo-1626447857058-2ba6a8868cb5",
                "photo-1618004912476-29818d81ae2e",
                "photo-1605810230434-7631ac76ec81"
            ]
        }
        
        # 키워드에 따라 적절한 카테고리 선택
        if "ai" in keyword.lower() or "tech" in keyword.lower():
            images = unsplash_collections["ai_tech"]
        elif "study" in keyword.lower() or "learn" in keyword.lower():
            images = unsplash_collections["learning"]
        elif "work" in keyword.lower() or "office" in keyword.lower():
            images = unsplash_collections["workspace"]
        else:
            images = unsplash_collections["creative"]
        
        # 랜덤 선택 + 파라미터 추가 (고품질)
        selected_image = random.choice(images)
        return f"https://images.unsplash.com/{selected_image}?w=1200&h=630&fit=crop&auto=format&q=90"
    
    def generate_high_quality_content(self, topic: str) -> Dict:
        """고품질 블로그 콘텐츠 생성"""
        
        # 더 상세하고 구체적인 프롬프트
        prompt = f"""
        당신은 AI 분야 전문 블로거입니다. 다음 주제로 고품질 블로그 포스트를 작성하세요.
        
        주제: {topic}
        
        요구사항:
        1. 제목: 클릭하고 싶은 매력적인 제목 (이모지 1개 포함)
        2. 길이: 2000-3000자 (충분히 상세하게)
        3. 구성:
           - 흥미로운 도입부 (독자 관심 유발)
           - 3-4개의 주요 섹션 (각각 구체적인 예시 포함)
           - 실전 팁 5개 이상
           - 실제 활용 사례 2개 이상
           - 핵심 요약
           - 독자 행동 유도 (CTA)
        
        4. 톤앤매너:
           - 친근하고 이해하기 쉬운 설명
           - 전문적이면서도 부담없는 어투
           - 구체적인 수치나 데이터 포함
        
        5. 차별화 포인트:
           - 다른 블로그에서 보기 어려운 독특한 인사이트
           - 개인적 경험이나 사례 추가
           - 실무에 바로 적용 가능한 팁
        
        JSON 형식으로 응답하세요:
        {{
            "title": "제목",
            "subtitle": "부제목",
            "content": "HTML 형식의 본문",
            "tags": ["태그1", "태그2", ...],
            "summary": "한 줄 요약"
        }}
        """
        
        try:
            # Gemini API 호출 (더 많은 토큰 허용)
            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.8,  # 창의성 증가
                    max_output_tokens=4000,  # 충분한 길이
                    top_p=0.9,
                    top_k=40
                )
            )
            
            # JSON 파싱
            content_text = response.text
            if "```json" in content_text:
                content_text = content_text.split("```json")[1].split("```")[0]
            elif "```" in content_text:
                content_text = content_text.split("```")[1].split("```")[0]
            
            result = json.loads(content_text)
            
            # 이미지 추가
            image_keyword = topic.split()[0] if topic else "AI"
            result['image_url'] = self.get_quality_image_url(image_keyword)
            
            return result
            
        except Exception as e:
            print(f"콘텐츠 생성 오류: {e}")
            # 폴백 콘텐츠
            return {
                "title": f"🤖 {topic}",
                "subtitle": "AI와 함께하는 스마트한 일상",
                "content": self.generate_fallback_content(topic),
                "tags": ["AI", "인공지능", "자동화"],
                "summary": "AI 기술을 활용한 실용적인 가이드",
                "image_url": self.get_quality_image_url("AI")
            }
    
    def generate_fallback_content(self, topic: str) -> str:
        """폴백 콘텐츠 생성"""
        return f"""
        <article style="max-width: 900px; margin: 0 auto; font-family: 'Noto Sans KR', sans-serif;">
            <h2>{topic}</h2>
            <p>이 주제에 대한 자세한 내용을 준비 중입니다.</p>
            <p>AI 기술의 발전과 함께 우리의 일상도 빠르게 변화하고 있습니다.</p>
        </article>
        """
    
    def create_beautiful_html(self, content_data: Dict) -> str:
        """아름다운 HTML 포스트 생성"""
        # 랜덤 색상 테마
        themes = [
            {"primary": "#6366f1", "secondary": "#8b5cf6", "accent": "#ec4899"},
            {"primary": "#3b82f6", "secondary": "#0ea5e9", "accent": "#06b6d4"},
            {"primary": "#10b981", "secondary": "#14b8a6", "accent": "#22d3ee"},
            {"primary": "#f59e0b", "secondary": "#f97316", "accent": "#ef4444"},
            {"primary": "#8b5cf6", "secondary": "#a855f7", "accent": "#d946ef"}
        ]
        theme = random.choice(themes)
        
        html = f"""
        <!DOCTYPE html>
        <html lang="ko">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700;900&display=swap');
            </style>
        </head>
        <body>
            <article style="max-width: 900px; margin: 0 auto; font-family: 'Noto Sans KR', sans-serif; line-height: 1.8; color: #1f2937;">
                
                <!-- 히어로 섹션 -->
                <header style="background: linear-gradient(135deg, {theme['primary']} 0%, {theme['secondary']} 100%); 
                               padding: 60px 40px; border-radius: 20px; color: white; margin-bottom: 40px;
                               box-shadow: 0 20px 40px rgba(0,0,0,0.1);">
                    <h1 style="font-size: 42px; font-weight: 900; margin: 0 0 15px 0; 
                               text-shadow: 0 2px 4px rgba(0,0,0,0.2);">
                        {content_data.get('title', 'AI 블로그')}
                    </h1>
                    <p style="font-size: 20px; font-weight: 300; opacity: 0.95; margin: 0;">
                        {content_data.get('subtitle', 'AI와 함께하는 스마트한 일상')}
                    </p>
                </header>
                
                <!-- 메인 이미지 -->
                <figure style="margin: 40px 0; text-align: center;">
                    <img src="{content_data.get('image_url', '')}" 
                         alt="{content_data.get('title', 'AI 이미지')}"
                         style="width: 100%; max-width: 800px; height: auto; 
                                border-radius: 16px; box-shadow: 0 10px 30px rgba(0,0,0,0.15);
                                object-fit: cover;">
                    <figcaption style="margin-top: 15px; color: #6b7280; font-size: 14px;">
                        {content_data.get('summary', '')}
                    </figcaption>
                </figure>
                
                <!-- 본문 콘텐츠 -->
                <div style="font-size: 18px; line-height: 1.9; color: #374151;">
                    {content_data.get('content', '')}
                </div>
                
                <!-- 태그 섹션 -->
                <footer style="margin-top: 60px; padding-top: 30px; border-top: 2px solid #e5e7eb;">
                    <div style="display: flex; flex-wrap: wrap; gap: 10px; margin-bottom: 20px;">
                        {"".join([f'<span style="background: {theme["accent"]}20; color: {theme["accent"]}; padding: 8px 16px; border-radius: 20px; font-size: 14px; font-weight: 500;">#{tag}</span>' for tag in content_data.get('tags', [])])}
                    </div>
                    
                    <div style="background: #f9fafb; padding: 25px; border-radius: 12px; 
                                border-left: 4px solid {theme['primary']};">
                        <p style="margin: 0; color: #6b7280; font-size: 16px;">
                            💡 이 글이 도움이 되셨나요? 더 많은 AI 팁과 가이드를 원하신다면 
                            구독과 좋아요를 눌러주세요!
                        </p>
                    </div>
                </footer>
                
            </article>
        </body>
        </html>
        """
        
        return html
    
    def post_to_blogger(self, title: str, content: str, labels: List[str]) -> bool:
        """Blogger에 포스팅"""
        if not self.config.get('token_data'):
            print("❌ 인증 토큰이 없습니다")
            return False
        
        try:
            # Blogger API 엔드포인트
            url = f"https://www.googleapis.com/blogger/v3/blogs/{self.config['blog_id']}/posts"
            
            # 포스트 데이터
            post_data = {
                "kind": "blogger#post",
                "title": title,
                "content": content,
                "labels": labels
            }
            
            # 액세스 토큰 (token 또는 access_token)
            access_token = self.config['token_data'].get('token') or self.config['token_data'].get('access_token')
            
            # 토큰 갱신이 필요한 경우
            if 'refresh_token' in self.config['token_data']:
                refresh_url = "https://oauth2.googleapis.com/token"
                refresh_data = {
                    'client_id': self.config['google_client_id'],
                    'client_secret': self.config['google_client_secret'],
                    'refresh_token': self.config['token_data']['refresh_token'],
                    'grant_type': 'refresh_token'
                }
                
                try:
                    refresh_response = requests.post(refresh_url, data=refresh_data)
                    if refresh_response.status_code == 200:
                        new_tokens = refresh_response.json()
                        access_token = new_tokens['access_token']
                        print("✅ 토큰 자동 갱신 성공")
                except Exception as e:
                    print(f"⚠️ 토큰 갱신 실패: {e}")
            
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            }
            
            response = requests.post(url, json=post_data, headers=headers)
            
            if response.status_code == 200:
                print(f"✅ 포스팅 성공: {title}")
                return True
            else:
                print(f"❌ 포스팅 실패: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ 포스팅 오류: {e}")
            return False
    
    def run(self):
        """메인 실행 함수"""
        print("🚀 개선된 블로그 자동화 시스템 시작")
        print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # 1. 다이나믹 토픽 생성
        max_attempts = 5
        for attempt in range(max_attempts):
            topic = self.generate_dynamic_topic()
            print(f"\n📝 생성된 토픽 (시도 {attempt + 1}): {topic}")
            
            # 2. 중복 체크 (임시 - 실제 콘텐츠 생성 전)
            if not self.check_duplicate(topic, ""):
                break
            else:
                print("⚠️ 유사한 토픽이 최근에 포스팅됨. 새 토픽 생성...")
                time.sleep(1)
        
        # 3. 고품질 콘텐츠 생성
        print("✍️ AI 콘텐츠 생성 중...")
        content_data = self.generate_high_quality_content(topic)
        
        # 4. 실제 중복 체크
        if self.check_duplicate(content_data['title'], content_data['content']):
            print("⚠️ 중복 콘텐츠 감지. 새로운 콘텐츠로 재생성...")
            topic = self.generate_dynamic_topic()
            content_data = self.generate_high_quality_content(topic)
        
        # 5. HTML 포맷팅
        html_content = self.create_beautiful_html(content_data)
        
        # 6. 포스팅
        success = self.post_to_blogger(
            content_data['title'],
            html_content,
            content_data.get('tags', ['AI', '인공지능'])
        )
        
        # 7. 히스토리 저장
        if success:
            self.save_history({
                'timestamp': datetime.now().isoformat(),
                'title': content_data['title'],
                'title_hash': hashlib.md5(content_data['title'].encode()).hexdigest(),
                'topic': topic,
                'tags': content_data.get('tags', []),
                'success': True
            })
            
            print("\n✅ 블로그 포스팅 완료!")
            print(f"📌 제목: {content_data['title']}")
            print(f"🏷️ 태그: {', '.join(content_data.get('tags', []))}")
        else:
            print("\n❌ 포스팅 실패")
        
        return success


def main():
    """메인 함수"""
    automation = ImprovedBlogAutomation()
    automation.run()


if __name__ == "__main__":
    main()