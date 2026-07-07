import chromadb
import json
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
CHROMA_PATH = str(BASE_DIR / "chroma_db")
RAG_JSON = str(BASE_DIR / "data" / "rag_documents.json")

COLLECTION_NAME = "careerfit_jobs"
DISTANCE_THRESHOLD = 1.2

CAREER_KEYWORDS = [
    "공고", "채용", "직무", "취업", "지원", "스킬", "역량",
    "데이터", "분석", "개발자", "경영", "통계", "Python", "SQL",
    "포트폴리오", "프로젝트", "공모전", "회사", "기업"
]

client = chromadb.PersistentClient(path=CHROMA_PATH)


def is_career_related_query(query: str) -> bool:
    """
    CareerFit AI의 주제와 관련 있는 질문인지 확인합니다.

    요리 비유:
    우리 레스토랑은 취업·공모전 메뉴 전문점입니다.
    '점심 뭐 먹을까' 같은 주문은 주방으로 보내기 전에 홀에서 정중히 돌려보냅니다.
    """
    query_lower = query.lower()
    return any(keyword.lower() in query_lower for keyword in CAREER_KEYWORDS)


def get_or_create_collection() -> chromadb.Collection:
    """
    ChromaDB 컬렉션을 가져오거나, 비어있으면 RAG 문서를 로드합니다.

    요리 비유:
    레시피 북을 열고, 비어있으면 레시피 카드를 채워넣습니다.
    """
    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"description": "CareerFit AI 취업·공모전 데이터"}
    )

    if collection.count() == 0:
        print("⚠️ ChromaDB가 비어있습니다. RAG 문서를 다시 저장합니다...")
        _load_documents(collection)

    return collection


def _load_documents(collection: chromadb.Collection) -> None:
    """
    rag_documents.json에서 문서를 읽어 ChromaDB에 저장합니다.
    """
    with open(RAG_JSON, "r", encoding="utf-8") as f:
        documents = json.load(f)

    collection.add(
        documents=[doc["text"] for doc in documents],
        metadatas=[doc["metadata"] for doc in documents],
        ids=[doc["doc_id"] for doc in documents]
    )

    print(f"✅ {collection.count()}개 문서 저장 완료")


def _filter_results(results: dict) -> list:
    """
    ChromaDB 검색 결과 중 distance가 너무 큰 문서를 제외합니다.

    distance가 낮을수록 질문과 더 유사합니다.
    """
    filtered_docs = []

    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]
    distances = results.get("distances", [[]])[0]

    for text, metadata, distance in zip(documents, metadatas, distances):
        rounded_distance = round(distance, 4)

        if rounded_distance <= DISTANCE_THRESHOLD:
            filtered_docs.append({
                "text": text,
                "metadata": metadata,
                "distance": rounded_distance
            })

    return filtered_docs


def search_documents(query: str, n_results: int = 3) -> list:
    """
    사용자 질문과 의미적으로 유사한 문서를 ChromaDB에서 검색합니다.

    Args:
        query: 사용자 질문 텍스트
        n_results: 검색할 후보 문서 수

    Returns:
        [{"text": str, "metadata": dict, "distance": float}, ...]

    개선 포인트:
    1. 취업·공모전 관련 질문인지 먼저 확인
    2. ChromaDB에서 후보 문서 검색
    3. distance 기준으로 관련성 낮은 문서 제외
    """

    if not is_career_related_query(query):
        return []

    collection = get_or_create_collection()
    collection_count = collection.count()

    if collection_count == 0:
        return []

    results = collection.query(
        query_texts=[query],
        n_results=min(n_results, collection_count)
    )

    return _filter_results(results)