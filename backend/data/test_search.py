# ChromaDB 저장 및 검색 테스트
# 실행: backend/ 폴더에서 python data/test_search.py

import chromadb
import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RAG_JSON = os.path.join(BASE_DIR, "rag_documents.json")
CHROMA_PATH = os.path.join(os.path.dirname(BASE_DIR), "chroma_db")

DISTANCE_THRESHOLD = 1.2

CAREER_KEYWORDS = [
    "공고", "채용", "직무", "취업", "지원", "스킬", "역량",
    "데이터", "분석", "개발자", "경영", "통계", "Python", "SQL",
    "포트폴리오", "프로젝트", "공모전", "회사", "기업"
]


def is_career_related_query(query: str) -> bool:
    """
    취업·공모전과 관련 없는 질문을 먼저 걸러냅니다.
    예: '오늘 점심 뭐 먹을까' → False
    """
    query_lower = query.lower()
    return any(keyword.lower() in query_lower for keyword in CAREER_KEYWORDS)


def load_rag_documents(json_path: str) -> list:
    """저장된 RAG 문서 JSON을 불러옵니다."""
    with open(json_path, "r", encoding="utf-8") as f:
        documents = json.load(f)

    print(f"✅ RAG 문서 {len(documents)}개 로드됨")
    return documents


def save_to_chromadb(documents: list, chroma_path: str) -> chromadb.Collection:
    """
    RAG 문서를 ChromaDB에 저장합니다.

    요리 비유:
    레시피 카드를 레시피 북(ChromaDB)에 정리해서 꽂아놓는 단계입니다.
    """
    print("\n=== ChromaDB 저장 ===")

    client = chromadb.PersistentClient(path=chroma_path)

    collection = client.get_or_create_collection(
        name="careerfit_jobs",
        metadata={"description": "CareerFit AI 취업·공모전 데이터"}
    )

    existing_count = collection.count()
    if existing_count > 0:
        print(f"   기존 문서 {existing_count}개 발견 → 초기화 후 재저장합니다")
        existing = collection.get()
        if existing["ids"]:
            collection.delete(ids=existing["ids"])

    collection.add(
        documents=[doc["text"] for doc in documents],
        metadatas=[doc["metadata"] for doc in documents],
        ids=[doc["doc_id"] for doc in documents]
    )

    print(f"   ✅ {collection.count()}개 문서 저장 완료")
    print(f"   저장 위치: {chroma_path}")

    return collection


def print_search_results(results: dict) -> None:
    """
    검색 결과를 distance 기준으로 평가해 출력합니다.
    """
    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    valid_count = 0

    for i, (doc, meta, distance) in enumerate(zip(documents, metadatas, distances)):
        print(f"  결과 {i + 1}:")
        print(f"    회사: {meta.get('company', '?')} | 직무: {meta.get('title', '?')}")
        print(f"    직무유형: {meta.get('job_type', '?')}")
        print(f"    추천전공: {meta.get('recommended_major', '?')}")
        print(f"    거리: {distance:.4f}")

        if distance <= DISTANCE_THRESHOLD:
            print("    평가: ✅ 사용 가능")
            valid_count += 1
        else:
            print("    평가: ⚠️ 관련성 낮음 - Gemini 근거로 쓰기 전 재검토 필요")

        print(f"    문서: {doc[:150]}...")

    if valid_count == 0:
        print("  최종 판단: ⚠️ Gemini에 넘길 만한 근거 문서가 없습니다.")
    else:
        print(f"  최종 판단: ✅ {valid_count}개 문서를 근거로 사용할 수 있습니다.")


def test_search(collection: chromadb.Collection) -> None:
    """
    저장된 문서로 질문 기반 검색을 테스트합니다.

    요리 비유:
    레시피 북에 질문을 던지고, 나온 레시피 카드가 진짜 주문과 맞는지 확인하는 단계입니다.
    """
    print("\n=== ChromaDB 검색 테스트 ===")

    test_queries = [
        "Python과 SQL이 필요한 데이터 분석 공고",
        "경영학과 학생이 지원할 수 있는 직무",
        "전공: 경영학부, 보유 스킬: Python, SQL, 관심 직무: 데이터 분석",
        "오늘 점심 뭐 먹을까",
    ]

    for query in test_queries:
        print(f"\n질문: '{query}'")

        if not is_career_related_query(query):
            print("  평가: ❌ CareerFit AI 범위 밖 질문입니다.")
            print("  응답 방향: 취업·공모전 관련 질문을 입력해 주세요.")
            continue

        results = collection.query(
            query_texts=[query],
            n_results=3
        )

        print_search_results(results)


if __name__ == "__main__":
    documents = load_rag_documents(RAG_JSON)
    collection = save_to_chromadb(documents, CHROMA_PATH)
    test_search(collection)

    print("\n✅ ChromaDB 저장 및 검색 테스트 완료")