# 🤖 Blog Automation System

자동 블로그 포스팅 시스템 - Blogger + Gemini AI

## 🚀 기능

- **자동 포스팅**: 매일 3회 (오전 9시, 오후 2시, 오후 8시) 자동 실행
- **AI 콘텐츠 생성**: Google Gemini AI로 블로그 포스트 자동 생성
- **Google Drive 동기화**: 10분마다 자동 동기화
- **다국어 지원**: 한국어 우선 지원

## ⚙️ 설정 방법

### 1. GitHub Secrets 설정

다음 시크릿들을 GitHub 저장소에 추가해야 합니다:

```
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret  
BLOGGER_BLOG_ID=your_blogger_blog_id
BLOGGER_TOKEN_JSON={"access_token":"...","refresh_token":"..."}
GEMINI_API_KEY=your_gemini_api_key
```

### 2. 워크플로우

- `blog-automation.yml`: 매일 3회 블로그 자동 포스팅
- `google_auto_sync.yml`: Google Drive 동기화

## 🔧 수동 실행

GitHub Actions에서 "Run workflow" 버튼으로 수동 실행 가능

## 📝 로그 확인

Actions 탭에서 실행 로그와 결과를 확인할 수 있습니다.