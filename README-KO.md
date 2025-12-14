# UpThink

**[Upstage AI Ambassador]** 개인 지식 관리 with Upstage Solar Pro 2 ✨

## Overview

UpThink는 개인 지식 관리 환경(Obsidian)에서 발생하는 반복적인 수작업 비용을 최소화하는 서비스입니다. \
지식을 정리하는 과정에서 필연적으로 발생하는 다음의 병목 현상들을 해결합니다.

| 문제 | 설명 |
|------|------|
| **이미지 데이터 처리** | 시각 정보를 텍스트로 변환하는 수동 작업 |
| **태그 관리** | 태그 컨벤션 유지 및 스타일링 고민 |
| **지식 연결성 부재** | 연관된 과거 노트를 찾기 위한 탐색 비용 |
| **비구조화된 문서** | 방대한 노트 분할의 필요성 |

UpThink는 **Upstage Solar Pro 2**의 강력한 언어 이해 능력을 기반으로 이러한 과정을 자동화합니다. \
사용자는 단순 반복 작업에서 벗어나, 가장 중요한 사고 활동에만 몰입할 수 있습니다.

### Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Tech Stack](#tech-stack)
- [Architecture](#architecture)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Members & Roles](#members--roles)
- [Acknowledgements](#acknowledgements)

## Key Features

### 1️⃣ 이미지 대체 텍스트 생성

노트 내 이미지에서 텍스트를 추출하고, 접근성을 위한 대체 텍스트(alt text)를 자동으로 생성합니다.

- **Upstage Document Parse**로 이미지에서 OCR 및 문서 구조 추출
- **Solar Pro 2**로 추출된 텍스트를 바탕으로 50단어 내외의 대체 텍스트 생성
- 마크다운 파일 내 모든 이미지를 일괄 처리
- 이미지 링크 `![[image.png]]` 바로 아래에 자동 삽입

### 2️⃣ 태그 추천

노트 내용을 분석하여 적절한 태그를 추천하고, 기존 Vault의 태그 컨벤션과 일관성을 유지합니다.

- Vault 내 기존 태그 자동 수집 (해시태그 `#tag` 및 YAML frontmatter 지원)
- 사용자 정의 가이드라인 설정 (언어, 대소문자, 구분자, 태그 개수)
- **Solar Pro 2**로 노트 내용 기반 태그 생성
- **Qwen Embedding** 모델로 기존 태그와 유사도 비교 및 매칭
- YAML frontmatter 형식으로 태그 자동 삽입

### 3️⃣ 연관 노트 추천

현재 노트와 의미적으로 유사한 노트를 찾아 자동으로 연결합니다.

- **Upstage Embedding Model**과 **Chroma DB**로 Vault 내 노트 벡터화
- 신규 노트 작성 시 연관 노트 자동 검색 및 추천
- 백링크 `[[note]]` 형식으로 자동 삽입

### 4️⃣ 노트 분할

방대한 노트를 주제별로 분리하여 원자적(Atomic)이고 상호 연결된 지식 체계를 구축합니다.

- **Solar Pro 2**로 노트 내 주제(Topic) 자동 추출
- 템플릿 기반의 유연한 분할 전략 지원
- 분할된 원자 노트 자동 생성 및 백링크 삽입

## Tech Stack

| 분류 | 기술 |
|------|------|
| **Language** | Python 3.13 |
| **Frontend** | Streamlit |
| **LLM** | Upstage Solar Pro 2 |
| **Document AI** | Upstage Document Parse |
| **Embedding** | Upstage Embedding, Qwen3-Embedding-0.6B |
| **Vector DB** | Chroma DB |
| **Framework** | LangChain |
| **Package Manager** | uv |

## Architecture

<img width="500" alt="Image" src="https://github.com/user-attachments/assets/ada44519-ae1c-4490-a4ae-22c2520b237b" />
<br>
<br>

| 레이어 | 구성 요소 | 설명 |
|--------|-----------|------|
| **Frontend** | Streamlit | 웹 기반 사용자 인터페이스 |
| **Backend** | Python 모듈 | 4가지 핵심 기능 구현 |
| **Upstage API** | Solar Pro 2, Document Parse, Embedding Model | LLM, OCR, 벡터 임베딩 |
| **Local** | Qwen Embedding, Chroma DB | 태그 유사도 비교, 노트 벡터 저장 |

### Flow Chart

#### 이미지 대체 텍스트 생성

<img width="600" alt="Image" src="https://github.com/user-attachments/assets/b514fb97-6632-4116-b07b-095841ff318a" />

#### 태그 추천

<img width="600" alt="Image" src="https://github.com/user-attachments/assets/a4c58f5c-3c01-481a-b560-333d42bca391" />

#### 연관 노트 추천

<img width="600" alt="Image" src="https://github.com/user-attachments/assets/9c71821d-7ae4-401e-a70f-de2b9e680078" />

#### 노트 분할

<img width="600" alt="Image" src="https://github.com/user-attachments/assets/55e80ef8-3c3f-4a95-883a-d5dcea0185e9" />

## Installation

### 지원 환경
- macOS
- Windows (PowerShell, CMD)

### uv 설치

- https://docs.astral.sh/uv/getting-started/installation/

#### Homebrew

```
brew install uv
```

#### Windows

```
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### 프로젝트 설정

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

### 실행

```
streamlit run frontend/app.py

# 아래 Local URL로 접속!
# http://localhost:8501
```

## Usage

### 🎬 시연 영상 보러가기: [YouTube](https://www.youtube.com/watch?v=8bjLew7KTW4) 🎬

### 기본 사용법

1. 사이드바에서 **Vault 경로**를 입력합니다. (Obsidian Vault의 절대 경로)
2. 처리할 **마크다운 파일**을 업로드합니다.
3. 원하는 기능 페이지로 이동하여 실행합니다.

## Project Structure

```
upthink/
├── frontend/                     # Streamlit 프론트엔드
│   ├── app.py                    # 메인 앱 (라우팅, 공통 사이드바)
│   ├── home.py                   # 홈 페이지
│   ├── image_ocr.py              # 이미지 대체 텍스트 생성 UI
│   ├── tag_suggest.py            # 태그 추천 UI
│   ├── related_note.py           # 연관 노트 추천 UI
│   ├── note_split.py             # 노트 분할 UI
│   └── note_freshness.py         # 최신 정보 확인 UI
│
├── backend/                      # 백엔드 로직
│   ├── image_ocr/                # 이미지 OCR 및 대체 텍스트 생성
│   │   ├── ocr_processor.py      # Document Parse API 연동
│   │   ├── alt_text_generator.py # Solar Pro 2 대체 텍스트 생성
│   │   └── markdown_processor.py # 마크다운 이미지 처리
│   │
│   ├── tag_suggest/              # 태그 추천
│   │   ├── tag_extractor.py      # Vault 태그 추출
│   │   ├── tag_guidelines.py     # 가이드라인 생성
│   │   ├── tag_generator.py      # Solar Pro 2 태그 생성
│   │   ├── tag_comparator.py     # Qwen Embedding 유사도 비교
│   │   └── markdown_processor.py # YAML frontmatter 처리
│   │
│   ├── related_note/             # 연관 노트 추천
│   │   └── related_note.py       # Chroma DB 기반 유사도 검색
│   │
│   ├── note_split/               # 노트 분할
│   │   ├── config.py             # 설정
│   │   ├── models.py             # 데이터 모델
│   │   ├── core/                 # 상태 관리, 파일 처리
│   │   ├── llm/                  # LLM 클라이언트, 프롬프트 로더
│   │   └── ui/                   # UI 컴포넌트
│   │
│   └── note_freshness/           # 최신성 검증
│       ├── api/                  # Tavily, Wikipedia API
│       ├── core/                 # 상태 관리
│       └── llm/                  # LLM 연동
│
├── prompts/                      # 프롬프트 템플릿 (YAML)
├── pyproject.toml                # 프로젝트 설정 및 의존성
└── .env.example                  # 환경 변수 예시
```

### 주요 함수

#### 1️⃣ 이미지 대체 텍스트 생성

| Step | Flow | Backend 모듈 |
|:----:|------|--------------|
| 1 | Vault 경로 & Markdown 파일 설정 | - |
| 2 | 이미지 대체 텍스트 생성 | `MarkdownImageProcessor.process_images()` |
| 2 | OCR 분석 및 LLM 추론 | `OCRProcessor.extract_text()` |
| 2 | 대체 텍스트 생성 | `AltTextGenerator.generate_alt_text()` |
| 3 | 처리 결과 확인 및 다운로드 | - |

#### 2️⃣ 태그 추천

| Step | Flow | Backend 모듈 |
|:----:|------|--------------|
| 1 | Vault 경로 & Markdown 파일 설정 | - |
| 2 | 기존 태그 분석 및 확인 | `TagExtractor.get_unique_tags()`, `TagExtractor.count_tags()` |
| 2 | 태그 작성 가이드라인 설정 | `GuidelineGenerator()` |
| 3 | 태그 생성 및 비교 | `TagGenerator.generate_tags()`, `TagComparator.compare_tags()`|
| 4 | 최종 태그 제안 | `TagComparator.get_final_tags()` |
| 4 | Vault 경로에 저장 | `add_yaml_frontmatter()` |

#### 3️⃣ 연관 노트 추천

| Step | Flow | Backend 모듈 |
|:----:|------|--------------|
| 1 | Vault 경로 설정 | `Related_Note()` |
| 2 | 임베딩되지 않은 노트 확인 | `Related_Note.get_unembedded_notes()` |
| 2 | 임베딩 | `Related_Note.index_unembedded_notes()` |
| 3 | Markdown 파일 경로 설정 | - |
| 3 | 연관 노트 추천 결과 확인 | `Related_Note.find_related_notes()` |
| 3 | 백링크 삽입 | `Related_Note.append_related_links()` |

#### 4️⃣ 노트 분할

| Step | Flow | Backend 모듈 |
|:----:|------|--------------|
| 1 | 노트 경로 & 저장 폴더 설정 | `FileHandler.read_note()` |
| 2 | 템플릿 선택 | `PromptLoader.load_template()` |
| 2 | Extract Topics 버튼 | `UpstageClient.generate_with_template_sync()` |
| 2 | 주제 파싱 | `ResponseParser.parse_topics_from_json()` |
| 3 | Generate Atomic Notes 버튼 | `FileHandler.create_atomic_note()` |
| 3 | 백링크 삽입 | `FileHandler.insert_backlinks()` |

## Members & Roles

|김수연|오주영|윤이지|홍재민|
|:-:|:-:|:-:|:-:|
| <a href="https://github.com/rlatndusgu" target="_blank"><img src="https://avatars.githubusercontent.com/u/204878926?v=4" height=130 width=130></img></a><br><a href="https://github.com/rlatndusgu" target="_blank"><img src="https://img.shields.io/badge/GitHub-black.svg?&style=round&logo=github"/> | <a href="https://github.com/Secludor" target="_blank"><img src="https://avatars.githubusercontent.com/u/129930239?v=4" height=130 width=130></img></a><br><a href="https://github.com/Secludor" target="_blank"><img src="https://img.shields.io/badge/GitHub-black.svg?&style=round&logo=github"/> | <a href="https://github.com/Yiji-1015" target="_blank"><img src="https://avatars.githubusercontent.com/u/122429800?v=4" height=130 width=130></img></a><br><a href="https://github.com/Yiji-1015" target="_blank"><img src="https://img.shields.io/badge/GitHub-black.svg?&style=round&logo=github"/> | <a href="https://github.com/geminii01" target="_blank"><img src="https://avatars.githubusercontent.com/u/171089104?v=4" height=130 width=130></img></a><br><a href="https://github.com/geminii01" target="_blank"><img src="https://img.shields.io/badge/GitHub-black.svg?&style=round&logo=github"/> |
|▪︎ 이미지 대체 텍스트 생성 기능 개발|▪︎ 노트 분할 기능 개발<br>▪︎ 최신성 검증 통합|▪︎ PM<br>▪︎ 연관 노트 추천 기능 개발|▪︎ 태그 추천 기능 개발<br>▪︎ GitHub 관리 & 팀 코드 통합|

## Acknowledgements

이 프로젝트는 **Upstage AI Ambassador** 활동의 일환으로 진행되었습니다. \
Credit 지원과 함께 프로젝트를 진행할 수 있도록 기회를 제공해 주신 **[Upstage](https://www.upstage.ai/)** 에 감사드립니다.