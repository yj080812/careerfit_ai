# backend/routers/analyze.py

from fastapi import APIRouter
from pydantic import BaseModel
from typing import List

from services.rag_service import search_documents
from services.llm_service import get_llm_response

router = APIRouter()


class AnalyzeRequest(BaseModel):
    major: str
    skills: List[str]
    job_type: str


class AnalyzeResponse(BaseModel):
    answer: str
    sources: List[dict]
    confidence: str = "medium"


@router.post("/analyze", response_model=AnalyzeResponse, tags=["Analyze"])
def analyze_career(request: AnalyzeRequest):
    """
    RAG 기반 역량 분석:
    ChromaDB 검색 → Gemini 답변 → sources + confidence 반환

    요리 비유:
    1. 사용자의 주문서를 자연어로 정리합니다.
    2. 레시피 북(ChromaDB)에서 관련 공고 카드를 찾습니다.
    3. 카드가 있으면 Gemini 셰프에게 전달합니다.
    4. 카드가 없으면 재료 부족 안내를 반환합니다.
    """

    query = (
        f"{request.major} 학생이 지원할 수 있는 {request.job_type} 직무를 찾고 있습니다. "
        f"보유 스킬은 {', '.join(request.skills)}입니다. "
        f"{', '.join(request.skills)} 스킬이 필요한 취업 공고를 추천해 주세요."
    )

    context_docs = search_documents(query=query, n_results=3)

    if not context_docs:
        return AnalyzeResponse(
            answer=(
                "제공된 자료만으로는 판단하기 어렵습니다. "
                "취업·공모전 또는 직무·스킬 관련 질문을 입력해 주세요."
            ),
            sources=[],
            confidence="low"
        )

    result = get_llm_response(
        query=query,
        context_docs=context_docs
    )

    return AnalyzeResponse(
        answer=result.get("answer", "분석 결과를 생성하지 못했습니다."),
        sources=result.get("sources", []),
        confidence=result.get("confidence", "medium")
    )