# harness/skills/design-skill.md — CareerFit AI UI 디자인 규칙

## 1. 목적

CareerFit AI React UI를 취업·공모전 데이터 기반 AI 포트폴리오 코치처럼 보이게 만든다.

이 문서는 Cursor, ChatGPT, 기타 바이브코딩 도구로 UI를 만들 때 따라야 할 디자인 기준이다.  
AI가 코드를 빠르게 생성하더라도, 색상·타이포그래피·레이아웃·컴포넌트 역할은 이 문서를 기준으로 유지한다.

요리 비유로 보면, 바이브코딩은 믹서기이고 이 문서는 레스토랑 운영 매뉴얼이다.  
믹서기가 빠르게 재료를 섞어주더라도, 어떤 재료를 넣고 어떤 접시에 담을지는 사람이 정한다.

---

## 2. 프로젝트 정보

- 프로젝트명: CareerFit AI
- 서비스 성격: 취업·공모전 데이터 기반 맞춤형 AI 포트폴리오 코치
- 주요 사용자: 대학생, 취업 준비생, 공모전 준비생
- 디자인 톤: 전문성 + 친근함
- 핵심 가치:
  - 입력은 간단하게
  - 결과는 짧고 명확하게
  - 근거 sources는 숨기지 않게
  - confidence는 사용자가 이해할 수 있게
  - 오류는 친절하게 안내하기

---

## 3. 디자인 목표

CareerFit AI UI는 다음 목표를 가진다.

1. 신뢰감 있는 AI 코치 서비스처럼 보여야 한다.
2. 대학생 사용자가 부담 없이 입력할 수 있어야 한다.
3. 발표 화면에서 한눈에 서비스 흐름이 이해되어야 한다.
4. 입력, 분석 결과, 출처, 신뢰도가 명확히 분리되어야 한다.
5. 과도하게 화려하기보다 포트폴리오에서 설명 가능한 디자인이어야 한다.

---

## 4. 컬러 팔레트

Tailwind CSS 기본 색상 체계를 우선 사용한다.

| 역할 | HEX | Tailwind 예시 | 의미 |
|---|---:|---|---|
| primary | `#3B82F6` | `blue-500`, `blue-600` | 신뢰, 전문성, 주요 버튼 |
| secondary | `#10B981` | `emerald-500`, `green-500` | 성장, 추천, 긍정 결과 |
| background | `#F8FAFC` | `slate-50` | 전체 배경 |
| surface | `#FFFFFF` | `white` | 카드 배경 |
| text-primary | `#1E293B` | `slate-800` | 제목, 핵심 텍스트 |
| text-secondary | `#334155` | `slate-700` | 카드 제목, 강조 본문 |
| text-muted | `#64748B` | `slate-500` | 설명, 보조 텍스트 |
| border | `#E2E8F0` | `slate-200`, `slate-300` | 카드, 입력창 테두리 |
| error | `#EF4444` | `red-500`, `red-700` | 오류 메시지 |
| error-bg | `#FEF2F2` | `red-50` | 오류 배경 |
| warning | `#F59E0B` | `amber-500`, `yellow-700` | 보통 신뢰도 |
| success | `#10B981` | `green-500`, `green-700` | 높은 신뢰도 |

기본 사용 예시:

- 주요 버튼: `bg-blue-500 hover:bg-blue-600 text-white`
- 카드: `bg-white border border-slate-200 rounded-xl`
- 제목: `text-slate-800`
- 설명: `text-slate-500`
- 오류: `bg-red-50 border border-red-200 text-red-700`

---

## 5. 타이포그래피 규칙

Tailwind 기본 sans-serif 계열을 사용한다.

기본 폰트:

- `font-sans`

텍스트 계층:

| 요소 | Tailwind 클래스 | 사용 위치 |
|---|---|---|
| 페이지 제목 | `text-2xl font-bold text-slate-800` | CareerFit AI 제목 |
| 카드 제목 | `text-lg font-semibold text-slate-700` | InputForm, ResultCard, SourceCard 제목 |
| 소제목 | `text-sm font-medium text-slate-600` | label, source 항목 제목 |
| 본문 | `text-base text-slate-600` | 일반 본문 |
| 결과 본문 | `text-sm text-slate-700 leading-relaxed` | AI 분석 결과 |
| 설명 | `text-sm text-slate-500` | 서비스 설명, 보조 안내 |
| 보조 정보 | `text-xs text-slate-500` | distance, confidence 보조 정보 |

타이포그래피 금지 사항:

- 한 화면에서 폰트 크기를 지나치게 많이 섞지 않는다.
- 제목에 너무 화려한 색상을 사용하지 않는다.
- 긴 문장은 `leading-relaxed`로 줄 간격을 확보한다.
- 결과 본문은 너무 작게 만들지 않는다.

---

## 6. 컴포넌트 구조

### 6-1. App.jsx

역할: 최상위 컴포넌트, 상태 관리, API 요청, 결과 렌더링을 담당한다.

담당 상태:

- `result`
- `isLoading`
- `error`

포함 요소:

- Header
- InputForm
- loading 상태
- error 상태
- ResultCard
- SourceCard

권장 구조:

- `App`
  - `Header`
  - `InputForm`
  - `ResultCard`
  - `SourceCard`

실습 단계에서는 `Header`를 별도 컴포넌트로 분리하지 않고 `App.jsx` 내부에 작성해도 된다.

---

### 6-2. InputForm.jsx

역할: 사용자의 전공, 보유 스킬, 관심 직무를 입력받는다.

입력 필드:

- 전공
- 보유 스킬
- 관심 직무

카드 스타일:

- `bg-white rounded-xl shadow-sm border border-slate-200 p-6`

입력창 스타일:

- `w-full border border-slate-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500`

버튼 스타일:

- `w-full bg-blue-500 hover:bg-blue-600 disabled:bg-slate-300 text-white font-medium py-2 px-4 rounded-lg transition-colors text-sm`

입력 UX 규칙:

- 모든 input에는 label을 둔다.
- placeholder는 예시 중심으로 작성한다.
- 필수 입력이 비어 있으면 버튼을 비활성화한다.
- 버튼 텍스트는 “역량 분석 요청”처럼 행동을 명확히 표현한다.

---

### 6-3. ResultCard.jsx

역할: AI 분석 답변을 출력한다.

포함 내용:

- 현재 역량 평가
- 추천 공고 또는 공모전
- 부족한 역량 및 준비 방향
- confidence 표시

카드 스타일:

- `bg-white rounded-xl shadow-sm border border-slate-200 p-6`

결과 본문 스타일:

- `text-sm text-slate-700 leading-relaxed whitespace-pre-line`

강조 규칙:

- ResultCard는 초록 왼쪽 테두리를 사용할 수 있다.
- 예: `border-l-4 border-l-emerald-500`
- 단, 전체 카드가 너무 강한 색으로 채워지지 않도록 한다.

추천 ResultCard 스타일:

- `bg-white rounded-xl shadow-sm border border-slate-200 border-l-4 border-l-emerald-500 p-6`

---

### 6-4. SourceCard.jsx

역할: RAG가 참고한 공고 데이터를 보여준다.

포함 내용:

- 회사명
- 직무명
- 직무 유형
- 필수 스킬
- 추천 전공
- distance
- matched_reason

출처 카드 스타일:

- `bg-slate-50 border border-slate-200 rounded-lg p-4`

sources 표시 규칙:

- sources를 숨기지 않는다.
- 사용자가 AI 답변의 근거를 확인할 수 있어야 한다.
- distance는 너무 강조하지 말고 보조 정보로 표시한다.
- 출처가 없으면 “참고한 공고 데이터가 없습니다.”라고 표시한다.

---

## 7. 레이아웃 규칙

전체 화면:

- `min-h-screen bg-slate-50 py-10 px-4`

콘텐츠 최대 너비:

- `max-w-2xl mx-auto`

카드 간격:

- `space-y-4`

컴포넌트 간격:

- `gap-4`

카드 내부 여백:

- `p-6`

모서리 규칙:

| 요소 | Tailwind 클래스 |
|---|---|
| 카드 | `rounded-xl` |
| 버튼 | `rounded-lg` |
| 입력창 | `rounded-lg` |
| 작은 배지 | `rounded-full` |

모바일 대응:

- 입력 폼과 결과 카드는 세로로 배치한다.
- 가로 스크롤이 생기지 않도록 `max-w-2xl`을 유지한다.
- 버튼은 모바일에서 누르기 쉽게 `w-full`을 사용한다.
- 너무 긴 source 텍스트는 카드 내부에서 줄바꿈되도록 한다.

---

## 8. UI 상태 규칙

반드시 구분해야 하는 상태는 다음과 같다.

### empty

아직 분석 전 상태.

표시 방향:

- 입력 폼만 보여준다.
- 결과 영역을 비워두거나 “정보를 입력하면 분석 결과가 표시됩니다.” 정도의 안내를 둔다.

### loading

분석 요청 중 상태.

필수 규칙:

- `role="status"`
- `aria-live="polite"`

표시 문구 예시:

- `분석 중입니다. 잠시만 기다려 주세요...`

### success

분석 성공 상태.

표시 요소:

- answer
- confidence
- sources

### error

요청 실패 상태.

필수 규칙:

- `role="alert"`

표시 문구 예시:

- `FastAPI 서버에 연결할 수 없습니다.`
- `요청 시간이 너무 오래 걸립니다. 서버 상태 또는 LLM 설정을 확인하세요.`

### no sources

sources가 비어 있는 상태.

표시 문구:

- `참고한 공고 데이터가 없습니다.`

---

## 9. confidence 표시 규칙

confidence는 AI 답변의 신뢰도 힌트이다.  
완전히 생략하지 않는다.

| 값 | 의미 | Tailwind 예시 |
|---|---|---|
| high | 근거 문서와 질문이 잘 맞음 | `bg-green-50 text-green-700 border-green-200` |
| medium | 어느 정도 관련 있음 | `bg-yellow-50 text-yellow-700 border-yellow-200` |
| low | 근거가 부족함 | `bg-red-50 text-red-700 border-red-200` |

표시 스타일 예시:

- `inline-flex items-center px-3 py-1 rounded-full border text-xs font-medium`

문구 예시:

- high: 신뢰도 높음
- medium: 신뢰도 보통
- low: 신뢰도 낮음

---

## 10. 접근성 규칙

label 사용:

- 모든 입력창에는 명확한 label을 둔다.
- 예: `전공`, `보유 스킬`, `관심 직무`

label 스타일:

- `block text-sm font-medium text-slate-600 mb-1`

버튼 텍스트:

- 아이콘만 있는 버튼을 사용하지 않는다.
- 버튼에는 반드시 텍스트 레이블을 포함한다.
- 예: “역량 분석 요청”, “다시 분석하기”

로딩 상태:

- 로딩 메시지에는 `role="status"`와 `aria-live="polite"`를 사용한다.

오류 메시지:

- 오류 메시지에는 `role="alert"`를 사용한다.

---

## 11. 보안 규칙

절대 금지:

- React 코드에 API Key를 넣지 않는다.
- API Key를 화면에 표시하지 않는다.
- API Key를 `localStorage`, `sessionStorage`에 저장하지 않는다.
- `VITE_GEMINI_API_KEY`처럼 브라우저에 노출되는 환경변수로 Key를 관리하지 않는다.
- `.env` 파일을 GitHub에 올리지 않는다.

올바른 구조:

- 프론트엔드: 사용자 입력만 FastAPI에 전달
- 백엔드: `.env`에서 API Key를 읽고 LLM API 호출
- FastAPI: `/analyze`에서 RAG 검색 + LLM 호출 처리

---

## 12. 금지 사항

디자인 금지:

- 다크 배경에 흰 텍스트를 기본값으로 쓰지 않는다. 가독성 우선.
- 지나치게 많은 색상을 사용하지 않는다.
- 버튼 색상을 화면마다 다르게 쓰지 않는다.
- 카드 그림자와 테두리를 과하게 사용하지 않는다.
- 과도한 애니메이션을 넣지 않는다.

UX 금지:

- 로딩 상태 없이 버튼만 멈추게 하지 않는다.
- 오류 메시지를 콘솔에만 출력하지 않는다.
- sources를 숨기지 않는다.
- confidence를 완전히 생략하지 않는다.
- 실제 없는 채용 정보처럼 보이게 꾸미지 않는다.
- 결과 영역에 긴 원문 데이터를 그대로 출력하지 않는다.

보안 금지:

- API Key를 화면에 표시하지 않는다.
- API Key를 localStorage에 저장하지 않는다.
- React 코드에 API Key를 직접 작성하지 않는다.

---

## 13. 발표용 기준

발표자가 화면을 보며 다음을 설명할 수 있어야 한다.

1. 사용자가 무엇을 입력하는가?
2. AI가 어떤 분석 결과를 주는가?
3. 어떤 공고 또는 데이터가 근거인가?
4. confidence가 높거나 낮은 이유는 무엇인가?
5. 오류가 발생했을 때 사용자는 무엇을 해야 하는가?

---

## 14. UI 원칙 요약

CareerFit AI의 UI는 다음 기준을 따른다.

1. 입력은 간단하게
2. 결과는 짧고 명확하게
3. 출처는 숨기지 않게
4. 신뢰도는 사용자에게 보이게
5. 오류는 친절하게
6. API Key는 절대 프론트엔드에 넣지 않게