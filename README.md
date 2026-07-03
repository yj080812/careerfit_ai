# CareerFit AI

> 취업·공모전 데이터 기반 맞춤형 AI 포트폴리오 코치



## 프로젝트 개요



[본인이 작성한 문제 정의 한 단락]

취업 준비생들은 채용 공고와 공모전 정보를 바탕으로 어떤 역량을 준비해야 하는지, 자신의 경험을 어떻게 포트폴리오로 정리해야 하는지 어려움을 겪습니다.

CareerFit AI는 취업·공모전 데이터를 분석하고 AI를 활용하여 사용자 맞춤형 커리어 및 포트폴리오 방향을 추천하는 서비스입니다.


## 기술 스택



| 영역 | 기술 |

|---|---|

| 백엔드 | Python, FastAPI |

| AI API | Gemini 2.5 Flash-Lite |

| 데이터 | Pandas, SQLite, ChromaDB |

| 프론트엔드 | React, Vite |

| 실행 환경 | Docker |

# 로컬 실행 방법

## 사전 요구 사항

- Python 3.11 이상
- Gemini API Key

## 백엔드 실행

```bash
cd backend
python -m venv venv
```

### Windows

```bash
venv\Scripts\activate
```

### macOS / Linux

```bash
source venv/bin/activate
```

### 패키지 설치

```bash
pip install -r requirements.txt
```

### 서버 실행

```bash
uvicorn main:app --reload
```

---

# 구현 기능

## FastAPI 서버

- FastAPI 프로젝트 구성
- Router 분리
- CORS 설정

### Health API

- `/health`
- 서버 상태 확인

### Jobs API

- `/jobs`
- `/jobs/{id}`
- 채용 공고 조회

### Analyze API

- `/analyze`
- Gemini API 기반 커리어 분석

---

# 데이터 파이프라인

## 취업·공모전 데이터 구조 설계

- CSV 데이터 구조 설계
- 채용 공고 및 공모전 데이터 관리

## 데이터 전처리

- 결측치 확인 및 처리
- 중복 데이터 제거
- 데이터 품질 검증

## 스킬 키워드 표준화

- Python, SQL 등 기술 스택 표준화
- 동일 의미의 스킬명 통일

## SQLite 저장

- 전처리 데이터 저장
- SQL 조회 테스트

## RAG 문서 생성

- 채용 공고를 자연어 문서로 변환
- JSON 형태의 RAG 문서 생성
- ChromaDB 저장을 위한 데이터 준비

---


## 진행 현황

3일차까지



- [x] 1일차: 프로젝트 기획 및 개발 환경 세팅

- [x] 2일차: FastAPI 서버 구축 및 Gemini API 연결

- [x] 3일차: 데이터 파이프라인 구축

- [ ] 4일차: RAG 기반 서비스 + React UI

- [ ] 5일차: Docker + 포트폴리오 완성