# backend/routers/jobs.py

from fastapi import APIRouter

from typing import List

router = APIRouter()



# 목업 데이터: 3일차에 실제 CSV 데이터로 교체한다

MOCK_JOBS = [
    {
        "id": 1,
        "company": "네이버",
        "title": "데이터 분석가 인턴",
        "required_skills": ["Python", "SQL", "통계분석"],
        "preferred_skills": ["Pandas", "Tableau"],
        "description": "서비스 이용 데이터를 분석하여 사용자 행동 패턴과 주요 지표를 도출합니다. 분석 결과를 바탕으로 서비스 개선 방향을 제안하고, 대시보드 제작을 지원합니다.",
        "deadline": "2026-08-31"
    },
    {
        "id": 2,
        "company": "카카오페이",
        "title": "금융 데이터 분석가",
        "required_skills": ["Python", "SQL", "확률과 통계"],
        "preferred_skills": ["머신러닝", "Power BI"],
        "description": "결제 및 금융 서비스 데이터를 분석하여 고객 행동과 리스크 요인을 파악합니다. 통계 모델과 데이터 시각화를 활용해 의사결정에 필요한 인사이트를 제공합니다.",
        "deadline": "2026-08-25"
    },
    {
        "id": 3,
        "company": "CJ올리브네트웍스",
        "title": "마케팅 데이터 분석가",
        "required_skills": ["Python", "SQL", "데이터 시각화"],
        "preferred_skills": ["R", "A/B 테스트"],
        "description": "고객 구매 데이터와 캠페인 성과 데이터를 분석하여 마케팅 전략 수립을 지원합니다. 통계적 검정과 실험 분석을 통해 프로모션 효과를 평가합니다.",
        "deadline": "2026-08-20"
    }
]



@router.get("/jobs", tags=["Jobs"])

def get_jobs():

    """

    취업 공고 목록을 반환하는 엔드포인트.

    현재는 목업 데이터를 반환하며, 3일차에 실제 데이터로 교체한다.

    """

    return {

        "count": len(MOCK_JOBS),

        "jobs": MOCK_JOBS

    }



@router.get("/jobs/{job_id}", tags=["Jobs"])

def get_job_by_id(job_id: int):

    """

    특정 공고의 상세 정보를 반환한다.

    """

    for job in MOCK_JOBS:

        if job["id"] == job_id:

            return job

    # 찾지 못한 경우

    from fastapi import HTTPException

    raise HTTPException(status_code=404, detail=f"공고 ID {job_id}를 찾을 수 없습니다.")