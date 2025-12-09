# UpThink

**[Upstage AI Ambassador]** 개인 지식 관리 with Upstage Solar pro 2

## Overview

> 🎬 시연 영상 보러가기: [YouTube](https://www.youtube.com/watch?v=8bjLew7KTW4)

UpThink는 개인 지식 관리 환경(Obsidian)에서 발생하는 반복적인 수작업 비용을 최소화하는 서비스입니다.

지식을 정리하는 과정에서 필연적으로 발생하는 다음의 병목 현상들을 해결합니다.

▪︎ㅤ이미지 데이터 처리: 시각 정보를 텍스트로 변환하는 수동 작업 \
▪︎ㅤ태그 관리: 태그 컨벤션 유지 및 스타일링 고민 \
▪︎ㅤ지식 연결성 부재: 연관된 과거 노트를 찾기 위한 탐색 비용 \
▪︎ㅤ비구조화된 문서: 방대한 노트 분할의 필요성

UpThink는 Upstage Solar Pro 2의 강력한 언어 이해 능력을 기반으로 이러한 과정을 자동화합니다. \
사용자는 단순 반복 작업에서 벗어나, 가장 중요한 사고 활동에만 몰입할 수 있습니다.

## Architecture

<img width="1395" alt="Image" src="https://github.com/user-attachments/assets/75be6352-930d-4bfb-ae4c-6d9fe15e7d05" />

## Features

### 1️⃣ 이미지 대체 텍스트 생성

노트 내 이미지를 탐색하여 Upstage Document Parse로 텍스트를 추출한 후, Solar Pro 2를 사용하여 이미지를 설명하는 대체 텍스트를 생성합니다. \
생성된 대체 텍스트는 이미지 링크의 바로 아래에 추가되어, 사용자가 수정된 Markdown 파일을 다운로드할 수 있습니다.

### 2️⃣ 태그 추천

Obsidian Vault 경로에 있는 모든 Markdown 파일에서 2가지 태그 패턴을 추출합니다. 사용자가 업로드한 파일 내용과 직접 설정한 가이드라인(언어, 포맷 등)을 기반으로 태그를 생성하고, 기존 태그와의 유사도를 비교해 최종 태그를 선별합니다. \
최종 선정된 태그 목록은 YAML Frontmatter 형식으로 노트 최상단에 자동으로 추가되어, 사용자가 수정된 Markdown 파일을 다운로드할 수 있습니다.

### 3️⃣ 연관 노트 추천

Upstage Embedding을 활용하여 노트 chunk를 임베딩하고, ChromaDB를 벡터 저장소로 사용하여 의미 기반 검색을 구현하였습니다. 증분 업데이트 구조를 구축해 재임베딩 비용을 최소화하였습니다.

### 4️⃣ 노트 분할

노트에 혼재된 여러 맥락에서 Solar Pro 2를 통해 주제(topic)와 coverage, 해당 주제 노트에 포함할 keywords, 참조할 본문의 line_numbers를 추출 및 제안하고, 사용자가 주제를 확인해 편집, 삭제, 추가, 선별하여 선별된 주제들에 대한 노트 초안과 가이드라인을 생성, markdown 파일을 지정된 경로에 저장합니다.

## Upstage Product Usage

- [Upstage Solar Pro 2](https://console.upstage.ai/docs/capabilities/generate/reasoning)
- [Upstage Document Parse](https://console.upstage.ai/docs/capabilities/digitize/document-parsing)
- [Upstage Information Extract](https://console.upstage.ai/docs/capabilities/extract/universal-extraction)
- [Upstage Embedding](https://console.upstage.ai/docs/capabilities/embed)

## Installation

**지원 환경**
- macOS
- Windows (PowerShell, CMD)

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
git clone https://github.com/geminii01/product-usecase-knowledge-management-upthink.git
cd product-usecase-knowledge-management-upthink
```
```
# 환경 변수 설정 (필수!)
cp .env.example .env

# .env 파일을 열어서 API 키 입력
# UPSTAGE_API_KEY=your_api_key_here
# TAVILY_API_KEY=your_api_key_here
```
```
# Python 3.13과 의존성 자동 설치
uv sync
```

### 3. 실행
```
streamlit run frontend/app.py

# 아래 Local URL로 접속!
# http://localhost:8501
```

## Members & Roles

|김수연|오주영|윤이지|홍재민|
|:-:|:-:|:-:|:-:|
| <a href="https://github.com/rlatndusgu" target="_blank"><img src="https://avatars.githubusercontent.com/u/204878926?v=4" height=130 width=130></img></a><br><a href="https://github.com/rlatndusgu" target="_blank"><img src="https://img.shields.io/badge/GitHub-black.svg?&style=round&logo=github"/> | <a href="https://github.com/Secludor" target="_blank"><img src="https://avatars.githubusercontent.com/u/129930239?v=4" height=130 width=130></img></a><br><a href="https://github.com/Secludor" target="_blank"><img src="https://img.shields.io/badge/GitHub-black.svg?&style=round&logo=github"/> | <a href="https://github.com/Yiji-1015" target="_blank"><img src="https://avatars.githubusercontent.com/u/122429800?v=4" height=130 width=130></img></a><br><a href="https://github.com/Yiji-1015" target="_blank"><img src="https://img.shields.io/badge/GitHub-black.svg?&style=round&logo=github"/> | <a href="https://github.com/geminii01" target="_blank"><img src="https://avatars.githubusercontent.com/u/171089104?v=4" height=130 width=130></img></a><br><a href="https://github.com/geminii01" target="_blank"><img src="https://img.shields.io/badge/GitHub-black.svg?&style=round&logo=github"/> |
|▪︎ 이미지 대체 텍스트 생성 기능 개발|▪︎ 노트 분할 기능 개발<br>▪︎ 최신성 검증 개발|▪︎ PM<br>▪︎ 연관 노트 추천 기능 개발|▪︎ 태그 추천 기능 개발<br>▪︎ GitHub 관리 & 팀 코드 통합|