# upthink

[Upstage AI Ambassador] 개인 지식 관리 with Upstage Solar pro 2

## 지원 환경

- **macOS**
- **Windows** (PowerShell, CMD)

## 환경 설정

### 1. uv 설치

- https://docs.astral.sh/uv/getting-started/installation/

#### Homebrew
```
brew install uv
```

#### Windows
```
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### 2. 프로젝트 설정
```
# git clone
git clone https://github.com/geminii01/upthink.git && cd upthink

# develop 브랜치로 전환
git checkout develop

# 환경 변수 설정 (필수!)
cp .env.example .env
# .env 파일을 열어서 API 키 입력
# UPSTAGE_API_KEY=your_api_key_here
# TAVILY_API_KEY=your_api_key_here

# Python 3.13과 의존성 자동 설치
uv sync
```

### 3. 실행
```
streamlit run frontend/app.py
```