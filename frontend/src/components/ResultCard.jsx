function ResultCard({ result }) {
  if (!result) {
    return null
  }

  const {
    answer,
    matched_skills = [],
    missing_skills = [],
    recommended_projects = [],
    confidence = 'low',
  } = result

  const confidenceConfig = {
    high: {
      label: '신뢰도 높음',
      shortLabel: 'High',
      description: '입력한 전공·스킬·관심 직무와 근거 데이터가 잘 맞습니다.',
      className: 'bg-green-50 text-green-700 border-green-200',
      barClassName: 'bg-green-500',
      widthClassName: 'w-full',
    },
    medium: {
      label: '신뢰도 보통',
      shortLabel: 'Medium',
      description: '일부 조건은 맞지만, 추가 확인이 필요합니다.',
      className: 'bg-yellow-50 text-yellow-700 border-yellow-200',
      barClassName: 'bg-yellow-500',
      widthClassName: 'w-2/3',
    },
    low: {
      label: '신뢰도 낮음',
      shortLabel: 'Low',
      description: '근거가 부족하거나 입력 정보와의 관련성이 낮을 수 있습니다.',
      className: 'bg-red-50 text-red-700 border-red-200',
      barClassName: 'bg-red-500',
      widthClassName: 'w-1/3',
    },
  }

  const currentConfidence =
    confidenceConfig[confidence] || confidenceConfig.low

  const summaryItems = [
    {
      label: '매칭 역량',
      value: matched_skills.length,
      helper: '현재 입력과 잘 맞는 스킬',
    },
    {
      label: '보완 역량',
      value: missing_skills.length,
      helper: '추가로 준비하면 좋은 스킬',
    },
    {
      label: '추천 프로젝트',
      value: recommended_projects.length,
      helper: '포트폴리오에 넣기 좋은 활동',
    },
  ]

  return (
    <section className="bg-white rounded-xl shadow-sm border border-slate-200 border-l-4 border-l-emerald-500 p-6 space-y-5">
      <div className="flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between">
        <div>
          <p className="text-sm font-medium text-emerald-600">
            AI 포트폴리오 코치 분석
          </p>
          <h2 className="text-lg font-semibold text-slate-800">
            맞춤 역량 분석 결과
          </h2>
          <p className="text-sm text-slate-500 mt-1">
            입력한 전공, 보유 스킬, 관심 직무를 바탕으로 준비 방향을 정리했습니다.
          </p>
        </div>

        <div
          className={`inline-flex w-fit items-center px-3 py-1 rounded-full border text-xs font-medium ${currentConfidence.className}`}
          title={currentConfidence.description}
        >
          {currentConfidence.label}
        </div>
      </div>

      <div className="grid gap-3 sm:grid-cols-3">
        {summaryItems.map((item) => (
          <div
            key={item.label}
            className="rounded-lg border border-slate-200 bg-slate-50 p-4"
          >
            <p className="text-xs font-medium text-slate-500">
              {item.label}
            </p>
            <p className="text-2xl font-bold text-slate-800 mt-1">
              {item.value}
              <span className="text-sm font-medium text-slate-500 ml-1">
                개
              </span>
            </p>
            <p className="text-xs text-slate-500 mt-1">
              {item.helper}
            </p>
          </div>
        ))}
      </div>

      <div className="rounded-lg bg-slate-50 border border-slate-200 p-4">
        <div className="flex items-center justify-between gap-3 mb-2">
          <h3 className="text-sm font-semibold text-slate-700">
            1. 현재 역량 평가
          </h3>
          <span className="text-xs text-slate-400">
            AI summary
          </span>
        </div>

        <p className="text-sm text-slate-700 leading-relaxed whitespace-pre-line">
          {answer || '분석 결과가 없습니다.'}
        </p>
      </div>

      <div className="grid gap-4 md:grid-cols-2">
        <div className="rounded-lg border border-emerald-200 bg-emerald-50 p-4">
          <div className="flex items-center justify-between mb-3">
            <h3 className="text-sm font-semibold text-emerald-700">
              2. 잘 맞는 역량
            </h3>
            <span className="text-xs text-emerald-600">
              Strength
            </span>
          </div>

          {matched_skills.length > 0 ? (
            <div className="flex flex-wrap gap-2">
              {matched_skills.map((skill, index) => (
                <span
                  key={`${skill}-${index}`}
                  className="inline-flex items-center rounded-full bg-white border border-emerald-200 px-3 py-1 text-xs font-medium text-emerald-700"
                >
                  {skill}
                </span>
              ))}
            </div>
          ) : (
            <p className="text-sm text-slate-500">
              아직 명확히 매칭된 역량이 없습니다.
            </p>
          )}
        </div>

        <div className="rounded-lg border border-amber-200 bg-amber-50 p-4">
          <div className="flex items-center justify-between mb-3">
            <h3 className="text-sm font-semibold text-amber-700">
              3. 보완하면 좋은 역량
            </h3>
            <span className="text-xs text-amber-600">
              Gap
            </span>
          </div>

          {missing_skills.length > 0 ? (
            <div className="flex flex-wrap gap-2">
              {missing_skills.map((skill, index) => (
                <span
                  key={`${skill}-${index}`}
                  className="inline-flex items-center rounded-full bg-white border border-amber-200 px-3 py-1 text-xs font-medium text-amber-700"
                >
                  {skill}
                </span>
              ))}
            </div>
          ) : (
            <p className="text-sm text-slate-500">
              현재 응답 기준으로 뚜렷한 부족 역량은 없습니다.
            </p>
          )}
        </div>
      </div>

      <div className="rounded-lg border border-blue-200 bg-blue-50 p-4">
        <div className="flex items-center justify-between mb-3">
          <h3 className="text-sm font-semibold text-blue-700">
            4. 추천 프로젝트
          </h3>
          <span className="text-xs text-blue-600">
            Portfolio action
          </span>
        </div>

        {recommended_projects.length > 0 ? (
          <ol className="space-y-2">
            {recommended_projects.map((project, index) => (
              <li
                key={`${project}-${index}`}
                className="flex gap-3 text-sm text-slate-700 leading-relaxed"
              >
                <span className="mt-0.5 flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-white border border-blue-200 text-xs font-semibold text-blue-700">
                  {index + 1}
                </span>
                <span>{project}</span>
              </li>
            ))}
          </ol>
        ) : (
          <p className="text-sm text-slate-500">
            추천 프로젝트 정보가 없습니다.
          </p>
        )}
      </div>

      <div className="rounded-lg border border-slate-200 bg-white p-4">
        <div className="flex flex-col gap-2 sm:flex-row sm:items-center sm:justify-between">
          <div>
            <h3 className="text-sm font-semibold text-slate-700">
              5. 신뢰도 해석
            </h3>
            <p className="text-xs text-slate-500 mt-1 leading-relaxed">
              {currentConfidence.description}
            </p>
          </div>

          <span
            className={`inline-flex w-fit items-center px-3 py-1 rounded-full border text-xs font-medium ${currentConfidence.className}`}
          >
            {currentConfidence.shortLabel}
          </span>
        </div>

        <div className="mt-3 h-2 w-full rounded-full bg-slate-100 overflow-hidden">
          <div
            className={`h-full rounded-full ${currentConfidence.barClassName} ${currentConfidence.widthClassName}`}
          />
        </div>
      </div>
    </section>
  )
}

export default ResultCard