// frontend/src/App.jsx

import { useState } from "react";
import InputForm from "./components/InputForm";
import ResultCard from "./components/ResultCard";
import SourceCard from "./components/SourceCard";
import { apiFetch, API_ENDPOINTS, API_BASE_URL } from "./config/api";

// ⚠️ API Key는 절대 프론트엔드 코드에 넣지 않습니다.
// API Key는 backend/.env 또는 Render Environment Variables에서만 관리합니다.

function App() {
  const [result, setResult] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  function validateFormData(formData) {
    if (!formData.major || !formData.major.trim()) {
      return "전공을 입력해 주세요.";
    }

    if (!formData.skills || formData.skills.length === 0) {
      return "보유 스킬을 1개 이상 입력해 주세요.";
    }

    if (!formData.jobType || !formData.jobType.trim()) {
      return "관심 직무를 입력해 주세요.";
    }

    return null;
  }

  function getConfidenceStyle(confidence) {
    if (confidence === "high") {
      return "bg-green-50 text-green-700 border-green-200";
    }

    if (confidence === "low") {
      return "bg-red-50 text-red-700 border-red-200";
    }

    return "bg-yellow-50 text-yellow-700 border-yellow-200";
  }

  function getConfidenceLabel(confidence) {
    if (confidence === "high") {
      return "신뢰도 높음";
    }

    if (confidence === "low") {
      return "신뢰도 낮음";
    }

    return "신뢰도 보통";
  }

  async function handleAnalyze(formData) {
    const validationMessage = validateFormData(formData);

    if (validationMessage) {
      setError(validationMessage);
      setResult(null);
      return;
    }

    setIsLoading(true);
    setError(null);
    setResult(null);

    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 30000);

    try {
      const response = await apiFetch(API_ENDPOINTS.analyze, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        signal: controller.signal,
        body: JSON.stringify({
          major: formData.major.trim(),
          skills: formData.skills,
          job_type: formData.jobType.trim(),
        }),
      });

      if (!response.ok) {
        throw new Error(`서버 오류가 발생했습니다. 상태 코드: ${response.status}`);
      }

      const data = await response.json();
      setResult(data);
    } catch (err) {
      if (err.name === "AbortError") {
        setError("요청 시간이 너무 오래 걸립니다. 서버 상태 또는 LLM 설정을 확인하세요.");
      } else if (err.message.includes("Failed to fetch")) {
        setError(`FastAPI 서버에 연결할 수 없습니다. API 주소를 확인하세요: ${API_BASE_URL}`);
      } else {
        setError(err.message || "알 수 없는 오류가 발생했습니다.");
      }
    } finally {
      clearTimeout(timeoutId);
      setIsLoading(false);
    }
  }

  return (
    <main className="min-h-screen bg-slate-50 py-10 px-4">
      <div className="max-w-2xl mx-auto">
        <header className="mb-8">
          <h1 className="text-2xl font-bold text-slate-800 mb-2">
            CareerFit AI
          </h1>
          <p className="text-slate-500 text-sm">
            취업·공모전 데이터 기반 맞춤형 AI 포트폴리오 코치
          </p>
        </header>

        <InputForm onSubmit={handleAnalyze} isLoading={isLoading} />

        {error && (
          <div
            role="alert"
            className="mt-4 p-4 bg-red-50 border border-red-200 rounded-lg text-red-700 text-sm"
          >
            {error}
          </div>
        )}

        {isLoading && (
          <div
            role="status"
            aria-live="polite"
            className="mt-8 text-center text-slate-500 text-sm"
          >
            분석 중입니다. 잠시만 기다려 주세요...
          </div>
        )}

        {result && (
          <section className="mt-8 space-y-4" aria-label="분석 결과">
            <div
              className={`inline-flex items-center px-3 py-1 rounded-full border text-xs font-medium ${getConfidenceStyle(
                result.confidence
              )}`}
            >
              {getConfidenceLabel(result.confidence)}
            </div>

            <ResultCard answer={result.answer} />

            {result.sources && result.sources.length > 0 ? (
              <SourceCard sources={result.sources} />
            ) : (
              <div className="p-4 bg-slate-100 border border-slate-200 rounded-lg text-slate-600 text-sm">
                참고한 공고 데이터가 없습니다.
              </div>
            )}
          </section>
        )}
      </div>
    </main>
  );
}

export default App;