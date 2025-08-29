#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GitHub Actions용 향상된 블로그 자동화 시스템
- Gemini AI로 고품질 콘텐츠 생성
- Google Blogger API 자동 포스팅
- 스케줄링 및 중복 방지
- 실제 이미지 URL 및 프리미엄 스타일링
"""

import os
import json
import sys
import argparse
from datetime import datetime, timedelta
import random
import requests
import google.generativeai as genai

def load_config():
    """설정 로드"""
    config = {
        'google_client_id': os.environ.get('GOOGLE_CLIENT_ID', '***'),
        'google_client_secret': os.environ.get('GOOGLE_CLIENT_SECRET', '***'),
        'blog_id': os.environ.get('BLOGGER_BLOG_ID', '***'),
        'gemini_api_key': os.environ.get('GEMINI_API_KEY', '***')
    }
    
    # 토큰 정보 로드
    try:
        with open('blogger_token.json', 'r', encoding='utf-8') as f:
            token_data = json.load(f)
            config['token_data'] = token_data
    except:
        print("❌ blogger_token.json 로드 실패")
        return None
    
    # Gemini API 설정
    if config['gemini_api_key'] and config['gemini_api_key'] != '***':
        genai.configure(api_key=config['gemini_api_key'])
    else:
        print("❌ Gemini API 키가 없습니다")
        return None
    
    return config

def get_unsplash_image_id(keyword):
    """키워드에 맞는 고품질 Unsplash 이미지 ID 반환"""
    image_collections = {
        "ai": ["1525876698956-fb31d5f6c7d8", "1677442136019-21780ecad995", "1555255707-c07be19750ed"],
        "technology": ["1518709268804-e9c82eae8e82", "1461749280684-dccba630e2f6", "1519389950473-47ba0277781c"],
        "computer": ["1488590528505-98d02b6ab33a", "1517077304055-6e89abbf09b0", "1484807352052-23338990c6c6"],
        "robot": ["1535378620166-273708d44e4c", "1551033406-611cf9a28f24", "1546776230-6d0d4fd7ea78"],
        "productivity": ["1484480974693-6ca0a78fb36b", "1611224923853-80b023f02d71", "1507003211169-0a1dd7ef0a96"],
        "workspace": ["1586953208448-b95a79798f07", "1541746972725-54cb8b6dd6ad", "1587560699334-bea93391dcef"],
        "creativity": ["1506905925346-21bda4d32df4", "1558655146-364adaf1fcc9", "1513475382585-d06e58bcb0e0"],
        "innovation": ["1485827404703-d89219db76e5", "1451187580459-43490c3819c7", "1519452634681-115ef5bd4e45"],
        "future": ["1518611012118-696072aa579a", "1507146153580-69a1fe6d8aa1", "1518709594765-be188be2a4c8"],
        "study": ["1434030216411-0b793f4b4173", "1513258496099-48168024aec0", "1456513080510-7bf3a84b82d8"]
    }
    
    matching_images = []
    for key, images in image_collections.items():
        if key in keyword.lower() or keyword.lower() in key:
            matching_images.extend(images)
    
    if not matching_images:
        matching_images = image_collections["technology"]
    
    return random.choice(matching_images)

def generate_premium_blog_content(topic=None):
    """AI로 프리미엄 스타일 블로그 콘텐츠 생성"""
    if not topic:
        # "AI 같이 공부하자" 블로그 주제에 맞는 토픽들
        topics = [
            "AI 공부 시작하는 완전 초보 가이드 - 어디서부터 해야 할까?",
            "ChatGPT vs Claude vs Gemini 실제 써보니 이런 차이가!",
            "AI 프롬프트 잘 쓰는 법 - 답답한 답변 이제 그만",
            "AI로 공부 효율 10배 높이기 - 실제 활용 후기",
            "요즘 핫한 AI 도구들 직접 써본 솔직 후기",
            "AI와 함께 영어/코딩/디자인 공부하는 방법",
            "AI 학습에 꼭 필요한 기초 지식 총정리",
            "중장년층도 쉽게! AI 도구 활용 가이드",
            "AI 업무 자동화 - 매일 반복 작업 해결법",
            "2025년 AI 트렌드 - 올해는 이것부터!",
            "AI 공부하다가 막혔을 때 해결법",
            "무료 AI 도구만으로도 이런 걸 할 수 있어요"
        ]
        topic = random.choice(topics)
    
    # 주제에 맞는 이미지 키워드 선택
    image_keywords = {
        "AI": ["ai", "robot", "technology"], 
        "공부": ["study", "productivity", "workspace"], 
        "도구": ["technology", "computer", "innovation"],
        "자동화": ["robot", "technology", "productivity"],
        "트렌드": ["future", "innovation", "technology"],
        "가이드": ["study", "productivity", "workspace"]
    }
    
    # 주제 기반 이미지 키워드 선택
    img_keyword = "technology"
    for key, keywords in image_keywords.items():
        if key in topic:
            img_keyword = random.choice(keywords)
            break
    
    # 실제 이미지 ID 가져오기
    image_id = get_unsplash_image_id(img_keyword)
    
    # 색상 테마 랜덤 선택
    color_themes = [
        {"primary": "#667eea", "secondary": "#764ba2", "accent": "#ff6b6b"},
        {"primary": "#4ecdc4", "secondary": "#44a08d", "accent": "#f093fb"},
        {"primary": "#a8edea", "secondary": "#fed6e3", "accent": "#ff9a9e"},
        {"primary": "#667eea", "secondary": "#764ba2", "accent": "#ffeaa7"}
    ]
    theme = random.choice(color_themes)
    
    # 이모지 선택
    topic_emojis = {
        "AI": "🤖", "공부": "📚", "도구": "🔧", "가이드": "📖",
        "자동화": "⚙️", "트렌드": "🚀", "비교": "⚖️", "활용": "💡"
    }
    
    emoji = "🤖"
    for key, em in topic_emojis.items():
        if key in topic:
            emoji = em
            break
    
    prompt = f"""
    주제: {topic}
    
    프리미엄 블로그 포스트를 위한 고품질 HTML 콘텐츠를 작성해주세요.
    
    다음 HTML 템플릿을 사용하되, 실제 내용으로 완성해주세요:
    
    <div style="max-width: 900px; margin: 0 auto; font-family: 'Noto Sans KR', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; line-height: 1.8; color: #333; background: #fff;">
        
        <!-- 헤더 섹션 -->
        <div style="text-align: center; margin-bottom: 50px; background: linear-gradient(135deg, {theme['primary']} 0%, {theme['secondary']} 100%); padding: 60px 40px; border-radius: 20px; color: white; position: relative; overflow: hidden;">
            <div style="position: absolute; top: -50px; right: -50px; width: 200px; height: 200px; background: rgba(255,255,255,0.1); border-radius: 50%; opacity: 0.3;"></div>
            <div style="position: absolute; bottom: -30px; left: -30px; width: 150px; height: 150px; background: rgba(255,255,255,0.1); border-radius: 50%; opacity: 0.2;"></div>
            <div style="position: relative; z-index: 10;">
                <div style="font-size: 80px; margin-bottom: 20px;">{emoji}</div>
                <h1 style="font-size: 36px; font-weight: 800; margin: 0 0 20px 0; text-shadow: 2px 2px 4px rgba(0,0,0,0.3); line-height: 1.2;">[매력적인 제목으로 교체]</h1>
                <p style="font-size: 20px; font-weight: 300; margin: 0; opacity: 0.9; line-height: 1.4;">[흥미로운 부제목으로 교체]</p>
            </div>
        </div>
        
        <!-- 메인 이미지 -->
        <div style="text-align: center; margin: 50px 0;">
            <img src="https://images.unsplash.com/photo-{image_id}?w=800&h=400&fit=crop&crop=center&auto=format&q=80" 
                 alt="{topic}" 
                 style="width: 100%; max-width: 800px; height: 400px; object-fit: cover; border-radius: 20px; box-shadow: 0 20px 60px rgba(0,0,0,0.15); transition: transform 0.3s ease;">
        </div>
        
        <!-- 서론 섹션 -->
        <div style="background: #f8fafc; padding: 40px; border-radius: 15px; margin: 40px 0; border-left: 5px solid {theme['primary']};">
            <h2 style="color: {theme['primary']}; font-size: 28px; font-weight: 700; margin: 0 0 20px 0; display: flex; align-items: center;">
                <span style="margin-right: 10px;">💭</span> 들어가며
            </h2>
            <p style="font-size: 18px; line-height: 1.8; margin: 0; color: #555;">[서론 내용 - 독자의 관심을 끌고 주제의 중요성을 설명]</p>
        </div>
        
        <!-- 주요 내용 섹션들 (3-4개) -->
        <div style="margin: 50px 0;">
            <h2 style="color: #2c3e50; font-size: 30px; font-weight: 800; margin: 0 0 30px 0; position: relative; padding-left: 20px;">
                <span style="position: absolute; left: -5px; top: 0; width: 4px; height: 100%; background: {theme['accent']}; border-radius: 2px;"></span>
                🎯 [섹션 제목 1]
            </h2>
            <div style="background: white; padding: 35px; border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); margin-bottom: 30px;">
                <p style="font-size: 18px; line-height: 1.8; margin-bottom: 20px; color: #444;">[구체적이고 실용적인 내용]</p>
                <ul style="font-size: 18px; line-height: 1.8; color: #555; padding-left: 20px;">
                    <li style="margin-bottom: 10px;">[구체적인 팁이나 예시 1]</li>
                    <li style="margin-bottom: 10px;">[구체적인 팁이나 예시 2]</li>
                    <li style="margin-bottom: 10px;">[구체적인 팁이나 예시 3]</li>
                </ul>
            </div>
        </div>
        
        <!-- 핵심 팁 하이라이트 박스 -->
        <div style="background: linear-gradient(135deg, {theme['primary']} 0%, {theme['secondary']} 100%); color: white; padding: 50px 40px; border-radius: 20px; margin: 50px 0; text-align: center; position: relative; overflow: hidden;">
            <div style="position: absolute; top: 20px; left: 20px; font-size: 120px; opacity: 0.1;">💡</div>
            <h3 style="font-size: 28px; font-weight: 700; margin: 0 0 25px 0; position: relative; z-index: 10;">🔥 핵심 포인트</h3>
            <p style="font-size: 20px; line-height: 1.6; margin: 0; font-weight: 400; position: relative; z-index: 10;">[가장 중요한 핵심 내용이나 팁]</p>
        </div>
        
        <!-- 실제 경험담 섹션 -->
        <div style="margin: 50px 0;">
            <h2 style="color: #2c3e50; font-size: 30px; font-weight: 800; margin: 0 0 30px 0; position: relative; padding-left: 20px;">
                <span style="position: absolute; left: -5px; top: 0; width: 4px; height: 100%; background: {theme['accent']}; border-radius: 2px;"></span>
                📝 실제 사용 후기
            </h2>
            <div style="background: #fff7ed; padding: 35px; border-radius: 15px; border: 1px solid #fed7aa; margin-bottom: 30px;">
                <p style="font-size: 18px; line-height: 1.8; color: #9a3412; margin: 0; font-style: italic;">[개인적인 경험담이나 구체적인 예시를 포함한 내용]</p>
            </div>
        </div>
        
        <!-- 마무리 및 실행 가이드 -->
        <div style="background: #f0f9ff; padding: 40px; border-radius: 15px; margin: 50px 0 30px 0; border: 1px solid #bae6fd; text-align: center;">
            <h3 style="color: #0c4a6e; font-size: 26px; font-weight: 700; margin: 0 0 20px 0;">🎯 오늘부터 시작해보세요!</h3>
            <p style="font-size: 18px; line-height: 1.8; color: #0c4a6e; margin: 0 0 25px 0;">[독자가 실제로 행동할 수 있는 구체적인 가이드]</p>
            <div style="display: inline-block; background: {theme['primary']}; color: white; padding: 12px 30px; border-radius: 30px; font-weight: 600; font-size: 16px;">
                💪 지금 바로 실행하기
            </div>
        </div>
        
        <!-- 댓글 참여 유도 -->
        <div style="background: white; padding: 30px; border-radius: 15px; text-align: center; margin-top: 40px; box-shadow: 0 8px 25px rgba(0,0,0,0.1);">
            <p style="font-size: 18px; color: #666; margin: 0 0 15px 0;">이 글이 도움이 되셨나요? 여러분의 경험도 댓글로 공유해주세요!</p>
            <div style="font-size: 24px; margin: 10px 0;">💬 ❤️ 🔄</div>
            <p style="font-size: 14px; color: #999; margin: 0;">좋아요, 댓글, 공유로 더 많은 분들과 함께해요 ✨</p>
        </div>
    </div>

    요구사항:
    1. 위 HTML 템플릿의 [대괄호] 부분을 모두 실제 내용으로 교체
    2. 주제에 맞는 구체적이고 실용적인 내용으로 작성
    3. 3000-4000자 분량의 고품질 콘텐츠
    4. 개인적 경험담과 구체적 예시 포함
    5. 독자가 바로 실행할 수 있는 실용적 팁 제공
    6. SEO 친화적이고 읽기 쉬운 구조
    7. 이미지는 이미 올바른 ID로 설정됨: {image_id}
    8. 색상 테마도 이미 설정됨: {theme}
    """
    
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(
            prompt,
            generation_config={
                "temperature": 0.8,
                "max_output_tokens": 4000,
                "top_p": 0.9,
                "top_k": 40
            }
        )
        return response.text, topic
    except Exception as e:
        print(f"❌ 콘텐츠 생성 실패: {e}")
        return None, None

def post_to_blog(config, title, content, labels=None):
    """블로그에 포스팅"""
    token_data = config['token_data']
    
    # 토큰 갱신이 필요한 경우 처리
    if 'refresh_token' in token_data:
        # refresh token으로 새 access token 획득
        refresh_data = {
            'client_id': config['google_client_id'],
            'client_secret': config['google_client_secret'],
            'refresh_token': token_data['refresh_token'],
            'grant_type': 'refresh_token'
        }
        
        try:
            refresh_response = requests.post('https://oauth2.googleapis.com/token', data=refresh_data)
            if refresh_response.status_code == 200:
                new_tokens = refresh_response.json()
                token_data['token'] = new_tokens['access_token']
                print("✅ 토큰 자동 갱신 완료")
            else:
                print("⚠️ 토큰 갱신 실패, 기존 토큰 사용")
        except:
            print("⚠️ 토큰 갱신 중 오류, 기존 토큰 사용")
    
    # 블로그 포스팅
    headers = {
        'Authorization': f'Bearer {token_data["token"]}',
        'Content-Type': 'application/json'
    }
    
    post_data = {
        'kind': 'blogger#post',
        'blog': {'id': config['blog_id']},
        'title': title,
        'content': content,
        'labels': labels or ['AI', '블로그', '테크']
    }
    
    url = f'https://www.googleapis.com/blogger/v3/blogs/{config["blog_id"]}/posts'
    
    try:
        response = requests.post(url, headers=headers, json=post_data)
        
        if response.status_code == 200:
            post = response.json()
            print('✅ 블로그 포스팅 성공!')
            print(f'제목: {post.get("title")}')
            print(f'URL: {post.get("url")}')
            return post
        else:
            print(f'❌ 포스팅 실패: {response.status_code}')
            print(response.text)
            return None
    except Exception as e:
        print(f'❌ 포스팅 중 오류: {e}')
        return None

def load_post_history():
    """포스팅 히스토리 로드"""
    try:
        with open('post_history.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return {'posts': [], 'last_post_date': None}

def save_post_history(history):
    """포스팅 히스토리 저장"""
    try:
        with open('post_history.json', 'w', encoding='utf-8') as f:
            json.dump(history, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"⚠️ 히스토리 저장 실패: {e}")

def should_post_today(history, max_posts_per_day=3):
    """오늘 포스팅 가능 여부 확인"""
    today = datetime.now().strftime('%Y-%m-%d')
    today_posts = [p for p in history['posts'] if p.get('date', '').startswith(today)]
    
    return len(today_posts) < max_posts_per_day

def main():
    parser = argparse.ArgumentParser(description='Enhanced Blog Automation')
    parser.add_argument('--topic', help='특정 주제로 포스팅')
    parser.add_argument('--labels', help='포스트 라벨 (쉼표 구분)')
    parser.add_argument('--auto', action='store_true', help='자동 모드')
    
    args = parser.parse_args()
    
    print("🚀 향상된 블로그 자동화 시작")
    print("=" * 50)
    
    # 설정 로드
    config = load_config()
    if not config:
        print("❌ 설정 로드 실패")
        sys.exit(1)
    
    print("✅ 설정 로드 완료")
    
    # 포스팅 히스토리 확인
    history = load_post_history()
    
    if args.auto:
        if not should_post_today(history):
            print("⏸️ 오늘 포스팅 한도 달성, 건너뛰기")
            return
    
    # 콘텐츠 생성
    print("🤖 프리미엄 AI 콘텐츠 생성 중...")
    content, topic = generate_premium_blog_content(args.topic)
    
    if not content:
        print("❌ 콘텐츠 생성 실패")
        sys.exit(1)
    
    print(f"✅ 콘텐츠 생성 완료: {topic}")
    
    # 라벨 처리
    labels = []
    if args.labels:
        labels = [label.strip() for label in args.labels.split(',')]
    else:
        labels = ['AI', '블로그', 'GitHub Actions']
    
    # 블로그 포스팅
    print("📝 블로그 포스팅 중...")
    post_result = post_to_blog(config, topic, content, labels)
    
    if post_result:
        # 히스토리 업데이트
        history['posts'].append({
            'date': datetime.now().isoformat(),
            'title': topic,
            'url': post_result.get('url'),
            'labels': labels,
            'method': 'github_actions'
        })
        history['last_post_date'] = datetime.now().isoformat()
        
        save_post_history(history)
        
        print("🎉 블로그 자동화 완료!")
    else:
        print("❌ 블로그 자동화 실패")
        sys.exit(1)

if __name__ == "__main__":
    main()