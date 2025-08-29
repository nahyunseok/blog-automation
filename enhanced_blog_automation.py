#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GitHub Actions용 향상된 블로그 자동화 시스템
- Gemini AI로 고품질 콘텐츠 생성
- Google Blogger API 자동 포스팅
- 스케줄링 및 중복 방지
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
        "AI": ["artificial-intelligence", "technology", "robot", "computer", "ai"],
        "생산성": ["productivity", "workspace", "laptop", "office", "work"],
        "창작": ["creativity", "art", "design", "creative", "innovation"],
        "미래": ["future", "tech", "digital", "innovation", "modern"],
        "비교": ["comparison", "analysis", "charts", "data", "statistics"]
    }
    
    # 주제 기반 이미지 키워드 선택
    img_keyword = "technology"
    for key, keywords in image_keywords.items():
        if key in topic:
            img_keyword = random.choice(keywords)
            break
    
    # 색상 테마 랜덤 선택
    color_themes = [
        {"primary": "#667eea", "secondary": "#764ba2", "accent": "#ff6b6b"},
        {"primary": "#4ecdc4", "secondary": "#44a08d", "accent": "#f093fb"},
        {"primary": "#a8edea", "secondary": "#fed6e3", "accent": "#ff9a9e"},
        {"primary": "#667eea", "secondary": "#764ba2", "accent": "#ffeaa7"}
    ]
    theme = random.choice(color_themes)
    
    prompt = f"""
    주제: {topic}
    
    프리미엄 블로그 포스트를 위한 고품질 콘텐츠를 작성해주세요.
    
    반드시 다음 HTML 구조를 사용해야 합니다:
    
    <div style="max-width: 800px; margin: 0 auto; font-family: 'Noto Sans KR', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; line-height: 1.8; background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); border-radius: 20px; padding: 40px; box-shadow: 0 20px 40px rgba(0,0,0,0.1);">
        
        <div style="text-align: center; margin-bottom: 50px;">
            <div style="width: 120px; height: 120px; margin: 0 auto 30px; background: linear-gradient(45deg, {theme['primary']} 0%, {theme['secondary']} 100%); border-radius: 50%; display: flex; align-items: center; justify-content: center; box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4);">
                <span style="font-size: 60px;">[주제에 맞는 이모지]</span>
            </div>
            <h1 style="color: #2c3e50; font-size: 32px; font-weight: 800; margin: 0; text-shadow: 2px 2px 4px rgba(0,0,0,0.1);">[매력적인 제목]</h1>
            <p style="color: #34495e; font-size: 18px; font-weight: 500; margin: 15px 0 0 0;">[흥미로운 부제목]</p>
        </div>
        
        <div style="text-align: center; margin: 40px 0;">
            <img src="https://images.unsplash.com/photo-[이미지ID]?w=600&h=300&fit=crop&crop=center" 
                 alt="{topic}" 
                 style="width: 100%; max-width: 600px; height: 300px; object-fit: cover; border-radius: 15px; box-shadow: 0 15px 35px rgba(0,0,0,0.1);">
        </div>
        
        [여기에 3-4개 섹션, 각각 다른 색상 테마와 아이콘 사용]
        
        <div style="background: linear-gradient(135deg, {theme['primary']} 0%, {theme['secondary']} 100%); color: white; padding: 40px; border-radius: 15px; margin: 40px 0; box-shadow: 0 15px 35px rgba(102, 126, 234, 0.3);">
            [핵심 팁이나 요약 섹션]
        </div>
        
        <div style="background: #fff; padding: 30px; border-radius: 15px; text-align: center; margin-top: 40px; box-shadow: 0 8px 25px rgba(0,0,0,0.1);">
            [마무리 및 독자 참여 유도]
        </div>
    </div>

    요구사항:
    1. 위 HTML 구조를 정확히 따르되, 내용은 창의적으로 작성
    2. Unsplash 이미지 사용 (실제 photo ID 포함)
    3. 각 섹션마다 다른 색상과 이모지 사용
    4. 2500-3500자 분량의 실질적 내용
    5. 개인적 경험담과 구체적 예시 포함
    6. 독자 참여를 유도하는 마무리
    
    이미지 키워드: {img_keyword}
    색상 테마: {theme}
    """
    
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
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
        'labels': labels or ['AI', '자동포스팅', '블로그', '테크']
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
        labels = ['AI', '자동포스팅', '블로그', 'GitHub Actions']
    
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