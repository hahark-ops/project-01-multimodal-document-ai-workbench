"use client";

import { useEffect, useState } from "react";

import { getApiBaseUrl, getApiErrorMessage, parseJsonSafely } from "@/lib/api";
import {
  EvaluationRunResponse,
  isEvaluationRunResponse,
  isSummaryResponse,
  SummaryResponse
} from "@/lib/document-ai";

type SummaryEvaluationPanelProps = {
  documentId: string;
};

export function SummaryEvaluationPanel({
  documentId
}: SummaryEvaluationPanelProps) {
  const [summaryPayload, setSummaryPayload] = useState<SummaryResponse | null>(null);
  const [evaluationPayload, setEvaluationPayload] = useState<EvaluationRunResponse | null>(null);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [isLoadingSummary, setIsLoadingSummary] = useState(false);
  const [isRunningEvaluation, setIsRunningEvaluation] = useState(false);

  useEffect(() => {
    let ignore = false;

    async function loadSummary() {
      setIsLoadingSummary(true);
      setErrorMessage(null);
      setSummaryPayload(null);

      try {
        const apiBaseUrl = getApiBaseUrl();
        const response = await fetch(`${apiBaseUrl}/summaries/generate`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify({
            document_id: documentId,
            max_points: 3,
            max_highlights: 3
          })
        });

        const payload = await parseJsonSafely(response);
        if (!response.ok) {
          throw new Error(getApiErrorMessage(payload) ?? "요약 생성 중 오류가 발생했습니다.");
        }
        if (!isSummaryResponse(payload)) {
          throw new Error("요약 응답을 해석할 수 없습니다.");
        }

        if (!ignore) {
          setSummaryPayload(payload);
        }
      } catch (error) {
        if (!ignore) {
          setErrorMessage(
            error instanceof Error ? error.message : "요약 생성 중 알 수 없는 오류가 발생했습니다."
          );
        }
      } finally {
        if (!ignore) {
          setIsLoadingSummary(false);
        }
      }
    }

    void loadSummary();

    return () => {
      ignore = true;
    };
  }, [documentId]);

  async function handleRunEvaluation() {
    setIsRunningEvaluation(true);
    setErrorMessage(null);

    try {
      const apiBaseUrl = getApiBaseUrl();
      const response = await fetch(`${apiBaseUrl}/evaluations/run`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          document_id: documentId,
          suite_id: "nc_dac_sample_contract_v1",
          top_k: 3,
          max_citations: 2
        })
      });

      const payload = await parseJsonSafely(response);
      if (!response.ok) {
        throw new Error(getApiErrorMessage(payload) ?? "평가 실행 중 오류가 발생했습니다.");
      }
      if (!isEvaluationRunResponse(payload)) {
        throw new Error("평가 응답을 해석할 수 없습니다.");
      }

      setEvaluationPayload(payload);
    } catch (error) {
      setErrorMessage(
        error instanceof Error ? error.message : "평가 실행 중 알 수 없는 오류가 발생했습니다."
      );
    } finally {
      setIsRunningEvaluation(false);
    }
  }

  return (
    <section className="mt-6 rounded-[2rem] border border-slate-200 bg-white/85 p-6 shadow-[0_24px_80px_rgba(15,23,42,0.06)] backdrop-blur">
      <div className="flex flex-wrap items-start justify-between gap-4">
        <div>
          <p className="text-sm font-medium uppercase tracking-[0.2em] text-slate-500">
            Phase 4 Summary And Evaluation
          </p>
          <h3 className="mt-3 text-2xl font-semibold text-slate-950">
            Summary And Quality Snapshot
          </h3>
          <p className="mt-2 max-w-2xl text-sm leading-6 text-slate-600">
            문서 전체 요약과 핵심 포인트를 보고, 준비된 질문 세트로 retrieval 및 grounded
            answer 품질을 빠르게 확인합니다.
          </p>
        </div>
        <button
          className="rounded-full bg-slate-950 px-5 py-3 text-sm font-medium text-white transition hover:bg-slate-800 disabled:cursor-not-allowed disabled:bg-slate-400"
          disabled={isRunningEvaluation}
          onClick={handleRunEvaluation}
          type="button"
        >
          {isRunningEvaluation ? "Evaluating..." : "Run Evaluation Suite"}
        </button>
      </div>

      {errorMessage ? (
        <div className="mt-6 rounded-2xl border border-rose-200 bg-rose-50 px-4 py-3 text-sm text-rose-700">
          {errorMessage}
        </div>
      ) : null}

      <div className="mt-6 grid gap-6 xl:grid-cols-[1fr_1fr]">
        <div className="rounded-3xl border border-slate-200 bg-slate-50 p-5">
          <div className="flex items-center justify-between gap-3">
            <p className="text-sm font-medium uppercase tracking-[0.2em] text-slate-500">
              Summary
            </p>
            <span className="rounded-full bg-white px-3 py-1 text-xs text-slate-600">
              {isLoadingSummary ? "Loading..." : summaryPayload ? `${summaryPayload.latency_ms} ms` : "Waiting"}
            </span>
          </div>

          {summaryPayload ? (
            <div className="mt-4 grid gap-4">
              <div className="rounded-2xl bg-slate-950 px-5 py-5 text-slate-50">
                <p className="text-xs uppercase tracking-[0.2em] text-slate-300">Summary text</p>
                <p className="mt-3 text-sm leading-7 text-slate-100">{summaryPayload.summary_text}</p>
              </div>

              <div className="grid gap-3">
                {summaryPayload.key_points.map((point) => (
                  <div
                    key={point}
                    className="rounded-2xl border border-slate-200 bg-white px-4 py-4 text-sm leading-6 text-slate-700"
                  >
                    {point}
                  </div>
                ))}
              </div>
            </div>
          ) : (
            <div className="mt-4 rounded-2xl border border-dashed border-slate-200 px-4 py-8 text-sm text-slate-500">
              요약을 불러오는 중입니다.
            </div>
          )}
        </div>

        <div className="rounded-3xl border border-slate-200 bg-white p-5 shadow-sm">
          <div className="flex items-center justify-between gap-3">
            <p className="text-sm font-medium uppercase tracking-[0.2em] text-slate-500">
              Evaluation
            </p>
            <span className="rounded-full bg-slate-100 px-3 py-1 text-xs text-slate-600">
              {evaluationPayload ? `${evaluationPayload.metrics.question_count} questions` : "Not run"}
            </span>
          </div>

          {evaluationPayload ? (
            <div className="mt-4 grid gap-4">
              <div className="grid gap-3 sm:grid-cols-2">
                <div className="rounded-2xl bg-emerald-50 px-4 py-4">
                  <p className="text-xs uppercase tracking-[0.2em] text-emerald-700">Retrieval hit rate</p>
                  <p className="mt-2 text-xl font-semibold text-emerald-900">
                    {(evaluationPayload.metrics.retrieval_hit_rate * 100).toFixed(0)}%
                  </p>
                </div>
                <div className="rounded-2xl bg-sky-50 px-4 py-4">
                  <p className="text-xs uppercase tracking-[0.2em] text-sky-700">Citation hit rate</p>
                  <p className="mt-2 text-xl font-semibold text-sky-900">
                    {(evaluationPayload.metrics.citation_hit_rate * 100).toFixed(0)}%
                  </p>
                </div>
                <div className="rounded-2xl bg-amber-50 px-4 py-4">
                  <p className="text-xs uppercase tracking-[0.2em] text-amber-700">Answer keyword hit</p>
                  <p className="mt-2 text-xl font-semibold text-amber-900">
                    {(evaluationPayload.metrics.answer_keyword_hit_rate * 100).toFixed(0)}%
                  </p>
                </div>
                <div className="rounded-2xl bg-slate-100 px-4 py-4">
                  <p className="text-xs uppercase tracking-[0.2em] text-slate-600">Overall pass</p>
                  <p className="mt-2 text-xl font-semibold text-slate-900">
                    {(evaluationPayload.metrics.overall_pass_rate * 100).toFixed(0)}%
                  </p>
                </div>
              </div>

              <div className="grid gap-3">
                {evaluationPayload.cases.map((item) => (
                  <article
                    key={item.question_id}
                    className="rounded-2xl border border-slate-200 bg-slate-50 px-4 py-4"
                  >
                    <div className="flex flex-wrap items-center justify-between gap-2">
                      <p className="text-sm font-semibold text-slate-900">{item.question}</p>
                      <span
                        className={`rounded-full px-3 py-1 text-xs ${
                          item.passed
                            ? "bg-emerald-100 text-emerald-700"
                            : "bg-rose-100 text-rose-700"
                        }`}
                      >
                        {item.passed ? "pass" : "check needed"}
                      </span>
                    </div>
                    <p className="mt-3 text-sm leading-6 text-slate-600">{item.answer_text}</p>
                    <p className="mt-3 text-xs uppercase tracking-[0.2em] text-slate-400">
                      Expected page {item.expected_page} / Retrieved {item.top_result_pages.join(", ")} / Cited {item.citation_pages.join(", ")}
                    </p>
                  </article>
                ))}
              </div>
            </div>
          ) : (
            <div className="mt-4 rounded-2xl border border-dashed border-slate-200 px-4 py-8 text-sm text-slate-500">
              평가 스위트를 실행하면 질문별 결과와 지표가 여기에 표시됩니다.
            </div>
          )}
        </div>
      </div>
    </section>
  );
}
