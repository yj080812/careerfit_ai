# backend/data/preprocess.py

# 데이터 전처리 파이프라인
# 실행: backend/ 폴더에서 python data/preprocess.py

import json
import os
import sqlite3
from datetime import date

import pandas as pd


# ─── 1. 파일 경로 설정

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JOBS_CSV = os.path.join(BASE_DIR, "jobs.csv")
DB_PATH = os.path.join(BASE_DIR, "careerfit.db")
RAG_JSON = os.path.join(BASE_DIR, "rag_documents.json")


# ─── 2. CSV 읽기

def load_data(filepath: str) -> pd.DataFrame:
    """
    CSV 파일을 읽어 DataFrame으로 반환합니다.
    인코딩 오류가 발생하면 cp949로 재시도합니다.
    """
    try:
        df = pd.read_csv(filepath, encoding="utf-8")
        print(f"✅ 파일 읽기 성공 (UTF-8): {filepath}")
    except UnicodeDecodeError:
        df = pd.read_csv(filepath, encoding="cp949")
        print(f"✅ 파일 읽기 성공 (CP949): {filepath}")

    print(f"   행 수: {len(df)}, 열 수: {len(df.columns)}")
    print(f"   컬럼: {df.columns.tolist()}")

    return df


# ─── 3-1. 결측치 확인

def check_missing(df: pd.DataFrame) -> pd.DataFrame:
    """
    각 컬럼의 결측치 수와 비율을 확인합니다.

    요리 비유:
    재료 중 빠진 것이 있는지 확인하는 단계입니다.
    """
    print("\n=== 결측치 확인 ===")

    missing = df.isnull().sum()
    missing_pct = (df.isnull().sum() / len(df) * 100).round(1)

    result = pd.DataFrame({
        "결측치 수": missing,
        "결측치 비율(%)": missing_pct
    })

    print(result[result["결측치 수"] > 0])

    if missing.sum() == 0:
        print("   ✅ 결측치 없음")
    else:
        print(f"   ⚠️ 총 {missing.sum()}개 결측치 발견")

    return df


# ─── 3-2. 결측치 처리

def handle_missing(df: pd.DataFrame) -> pd.DataFrame:
    """
    결측치를 처리합니다.
    - title, required_skills가 비어 있으면 제거
    - 나머지 텍스트 컬럼은 빈 문자열로 처리
    """
    print("\n=== 결측치 처리 ===")

    before = len(df)

    df = df.dropna(subset=["title", "required_skills"]).copy()

    text_cols = [
        "company",
        "title",
        "job_type",
        "required_skills",
        "preferred_skills",
        "description",
        "deadline"
    ]

    for col in text_cols:
        if col in df.columns:
            df[col] = df[col].fillna("")

    after = len(df)

    print(f"   처리 전: {before}행 → 처리 후: {after}행")
    print(f"   제거된 행: {before - after}행")

    return df


# ─── 3-3. 중복 제거

def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """
    company + title 조합이 같으면 중복으로 판단합니다.
    """
    print("\n=== 중복 확인 ===")

    before = len(df)

    duplicated = df.duplicated(subset=["company", "title"], keep=False)

    if duplicated.sum() > 0:
        print(f"   ⚠️ 중복 발견: {duplicated.sum()}행")
        print(df[duplicated][["company", "title"]])
    else:
        print("   ✅ 중복 없음")

    df = df.drop_duplicates(subset=["company", "title"], keep="first")

    after = len(df)

    print(f"   제거 후: {after}행 (제거: {before - after}행)")

    return df


# ─── 3-4. 스킬 키워드 표준화

SKILL_NORMALIZATION = {
    "python": "Python",
    "sql": "SQL",
    "ai": "AI",
    "ml": "머신러닝",
    "machine learning": "머신러닝",
    "deep learning": "딥러닝",
    "r": "R",
    "js": "JavaScript",
    "javascript": "JavaScript",
    "tableau": "Tableau",
    "powerbi": "Power BI",
    "power bi": "Power BI",
    "excel": "Excel",
    "엑셀": "Excel",
}


def normalize_skills(skills_str: str) -> str:
    """
    스킬 키워드 문자열을 표준화합니다.
    입력: "python, sql, Machine Learning"
    출력: "Python, SQL, 머신러닝"
    """
    if not isinstance(skills_str, str) or not skills_str.strip():
        return ""

    skills = [s.strip() for s in skills_str.split(",")]
    normalized = []

    for skill in skills:
        lower = skill.lower()
        normalized.append(SKILL_NORMALIZATION.get(lower, skill))

    return ", ".join(normalized)


def standardize_skills(df: pd.DataFrame) -> pd.DataFrame:
    """
    required_skills, preferred_skills 컬럼에 스킬 표준화를 적용합니다.
    """
    print("\n=== 스킬 키워드 표준화 ===")

    for col in ["required_skills", "preferred_skills"]:
        if col in df.columns:
            df[col] = df[col].apply(normalize_skills)

    print("   ✅ 표준화 완료")

    print("\n   [표준화 결과 샘플]")
    print(df[["title", "required_skills"]].head(3).to_string())

    return df


# ─── 3-5. SQLite 저장

def save_to_sqlite(df: pd.DataFrame, db_path: str) -> None:
    """
    전처리된 DataFrame을 SQLite 데이터베이스에 저장합니다.

    요리 비유:
    손질이 끝난 재료를 냉장고(SQLite)에 정리해서 넣는 단계입니다.
    """
    print("\n=== SQLite 저장 ===")

    conn = sqlite3.connect(db_path)

    df.to_sql("jobs", conn, if_exists="replace", index=False)

    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM jobs")
    count = cursor.fetchone()[0]

    print(f"   ✅ 저장 완료: jobs 테이블에 {count}행 저장됨")
    print(f"   파일 위치: {db_path}")

    conn.close()


# ─── 3-6. SQLite 조회 테스트

def query_sqlite(db_path: str) -> None:
    """
    SQLite에서 데이터를 조회해 저장 결과를 확인합니다.
    """
    print("\n=== SQLite 조회 테스트 ===")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM jobs")
    print(f"   전체 공고 수: {cursor.fetchone()[0]}개")

    print("\n   [직무 분류별 공고 수]")
    cursor.execute("""
        SELECT job_type, COUNT(*) as count
        FROM jobs
        GROUP BY job_type
        ORDER BY count DESC
    """)

    for row in cursor.fetchall():
        print(f"   - {row[0]}: {row[1]}개")

    print("\n   [Python이 필요한 공고]")
    cursor.execute("""
        SELECT company, title, required_skills
        FROM jobs
        WHERE required_skills LIKE '%Python%'
        LIMIT 3
    """)

    for row in cursor.fetchall():
        print(f"   - {row[0]} | {row[1]}")
        print(f"     스킬: {row[2]}")

    conn.close()


# ─── 4. RAG 문서 품질 개선용 헬퍼 함수

def safe_str(value) -> str:
    """
    NaN, None 값을 빈 문자열로 안전하게 변환합니다.
    ChromaDB metadata에는 None이 들어가면 오류가 날 수 있습니다.
    """
    if pd.isna(value):
        return ""
    return str(value).strip()


def infer_major_fit(job_type: str, title: str, description: str, required_skills: str) -> tuple[str, str]:
    """
    직무 정보로 추천 전공과 전공 적합성 문장을 추론합니다.

    주의:
    실제 서비스에서는 CSV에 recommended_major, major_reason 컬럼을 두는 것이 더 좋습니다.
    지금은 실습용 목업 데이터 기준의 간단한 규칙입니다.
    """
    combined_text = f"{job_type} {title} {description} {required_skills}"

    if any(keyword in combined_text for keyword in ["경영", "전략", "마케팅", "고객", "커머스", "이커머스", "공급망", "물류", "리스크", "금융"]):
        return (
            "경영학부, 통계학과",
            "경영학과 학생은 전략, 마케팅, 재무, 운영관리, 고객 분석 관점에서 이 직무와 관련성이 높습니다."
        )

    if any(keyword in combined_text for keyword in ["데이터 분석", "데이터 사이언티스트", "통계", "A/B", "분석"]):
        return (
            "통계학과, 경영학부",
            "통계학과 학생은 데이터 분석, 통계 해석, 실험 설계 관점에서 이 직무와 관련성이 높습니다."
        )

    if any(keyword in combined_text for keyword in ["프론트엔드", "백엔드", "개발", "React", "JavaScript", "AI", "ML", "머신러닝", "딥러닝"]):
        return (
            "컴퓨터과학부, 통계학과",
            "컴퓨터과학부 학생은 서비스 구현, 모델 개발, 시스템 설계 관점에서 이 직무와 관련성이 높습니다."
        )

    return (
        "전공 무관",
        "보유 스킬과 프로젝트 경험에 따라 지원 가능성을 판단해야 합니다."
    )


def build_search_keywords(
    company: str,
    title: str,
    job_type: str,
    required_skills: str,
    preferred_skills: str,
    recommended_major: str
) -> str:
    """
    ChromaDB 의미 검색에 도움이 되는 키워드 문장을 만듭니다.
    """
    return (
        f"검색 키워드: {company}, {title}, {job_type}, "
        f"{required_skills}, {preferred_skills}, {recommended_major}, "
        f"취업 공고, 직무 추천, 스킬 매칭, 전공 적합성"
    )


# ─── 5. RAG 문서 변환

def convert_to_rag_documents(df: pd.DataFrame) -> list:
    """
    DataFrame의 각 행을 RAG 검색에 적합한 자연어 문서로 변환합니다.

    요리 비유:
    냉장고의 재료 목록을 Gemini 셰프가 바로 읽을 수 있는 레시피 카드로 변환합니다.
    """
    print("\n=== RAG 문서 변환 ===")

    documents = []

    for _, row in df.iterrows():
        company = safe_str(row.get("company", ""))
        title = safe_str(row.get("title", ""))
        job_type = safe_str(row.get("job_type", ""))
        required_skills = safe_str(row.get("required_skills", ""))
        preferred_skills = safe_str(row.get("preferred_skills", ""))
        description = safe_str(row.get("description", ""))
        deadline = safe_str(row.get("deadline", ""))
        row_id = safe_str(row.get("id", ""))

        recommended_major, major_reason = infer_major_fit(
            job_type=job_type,
            title=title,
            description=description,
            required_skills=required_skills
        )

        search_keywords = build_search_keywords(
            company=company,
            title=title,
            job_type=job_type,
            required_skills=required_skills,
            preferred_skills=preferred_skills,
            recommended_major=recommended_major
        )

        doc_text = (
            f"{company}에서 {title}를 채용합니다. "
            f"직무 분야는 {job_type}입니다. "
            f"필수 스킬은 {required_skills if required_skills else '정보 없음'}입니다. "
            f"우대 스킬은 {preferred_skills if preferred_skills else '없음'}입니다. "
            f"주요 업무는 {description if description else '정보 없음'} "
            f"추천 전공은 {recommended_major}입니다. "
            f"전공 적합성: {major_reason} "
            f"이 공고는 Python, SQL, 데이터 분석, 경영학과, 통계학과, 컴퓨터과학부 등 "
            f"사용자의 전공과 보유 스킬을 기준으로 비교할 수 있습니다. "
            f"{search_keywords}"
        )

        metadata = {
            "id": row_id,
            "company": company,
            "title": title,
            "job_type": job_type,
            "deadline": deadline,
            "source": "jobs.csv",
            "required_skills": required_skills,
            "preferred_skills": preferred_skills,
            "recommended_major": recommended_major,
            "major_reason": major_reason,
            "deadline_month": deadline[5:7] if len(deadline) >= 7 and deadline[4] == "-" else "",
            "is_startup": "true" if "스타트업" in company else "false",
            "first_saved_date": date.today().isoformat()
        }

        documents.append({
            "text": doc_text,
            "metadata": metadata,
            "doc_id": f"job_{row_id}"
        })

    print(f"   ✅ {len(documents)}개 문서 변환 완료")

    if documents:
        print("\n   [첫 번째 문서 미리보기]")
        print(f"   ID: {documents[0]['doc_id']}")
        print(f"   텍스트: {documents[0]['text'][:180]}...")
        print(f"   메타데이터: {documents[0]['metadata']}")

    return documents


def save_rag_documents(documents: list, json_path: str) -> None:
    """
    RAG 문서를 JSON 파일로 저장합니다.
    ChromaDB에 저장하기 전 중간 저장 역할을 합니다.
    """
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(documents, f, ensure_ascii=False, indent=2)

    print(f"\n   ✅ RAG 문서 JSON 저장: {json_path}")


# ─── 6. 실행

if __name__ == "__main__":
    df_jobs = load_data(JOBS_CSV)
    df_jobs = check_missing(df_jobs)
    df_jobs = handle_missing(df_jobs)
    df_jobs = remove_duplicates(df_jobs)
    df_jobs = standardize_skills(df_jobs)

    save_to_sqlite(df_jobs, DB_PATH)
    query_sqlite(DB_PATH)

    rag_docs = convert_to_rag_documents(df_jobs)
    save_rag_documents(rag_docs, RAG_JSON)

    print(f"\n✅ 전처리 완료: 최종 {len(df_jobs)}행, RAG 문서 {len(rag_docs)}개")