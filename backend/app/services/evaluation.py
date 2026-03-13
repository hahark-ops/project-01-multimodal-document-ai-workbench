import json
from pathlib import Path

from app.schemas.evaluations import (
    EvaluationCaseResult,
    EvaluationMetrics,
    EvaluationRunResponse,
)
from app.services.grounded_answer import answer_question
from app.services.retrieval import search_document_chunks

DATA_DIR = Path(__file__).resolve().parents[1] / "data" / "evaluation_suites"


class EvaluationSuiteNotFoundError(Exception):
    pass


def _load_suite(suite_id: str) -> dict:
    file_path = DATA_DIR / f"{suite_id}.json"
    if not file_path.exists():
        raise EvaluationSuiteNotFoundError(f"Evaluation suite '{suite_id}' was not found.")
    return json.loads(file_path.read_text(encoding="utf-8"))


def _has_keyword_match(answer_text: str, expected_keywords: list[str]) -> bool:
    lowered_answer = answer_text.lower()
    return all(keyword.lower() in lowered_answer for keyword in expected_keywords)


def _rate(value: int, total: int) -> float:
    if total == 0:
        return 0.0
    return round(value / total, 4)


def run_evaluation(
    document_id: str,
    *,
    suite_id: str = "nc_dac_sample_contract_v1",
    top_k: int = 3,
    max_citations: int = 2,
) -> EvaluationRunResponse:
    suite = _load_suite(suite_id)
    cases: list[EvaluationCaseResult] = []

    retrieval_hits = 0
    citation_hits = 0
    answer_keyword_hits = 0
    passes = 0

    for item in suite["questions"]:
        retrieval_payload = search_document_chunks(
            item["question"],
            document_id=document_id,
            top_k=top_k,
        )
        answer_payload = answer_question(
            item["question"],
            document_id=document_id,
            top_k=top_k,
            max_citations=max_citations,
        )

        top_result_pages = [result.page_number for result in retrieval_payload.results]
        citation_pages = [citation.page_number for citation in answer_payload.citations]

        retrieval_hit = item["expected_page"] in top_result_pages
        citation_hit = item["expected_page"] in citation_pages
        answer_keyword_hit = _has_keyword_match(
            answer_payload.answer_text,
            item["expected_keywords"],
        )
        passed = retrieval_hit and citation_hit and answer_keyword_hit

        retrieval_hits += int(retrieval_hit)
        citation_hits += int(citation_hit)
        answer_keyword_hits += int(answer_keyword_hit)
        passes += int(passed)

        cases.append(
            EvaluationCaseResult(
                question_id=item["question_id"],
                question=item["question"],
                expected_page=item["expected_page"],
                expected_keywords=item["expected_keywords"],
                retrieval_hit=retrieval_hit,
                citation_hit=citation_hit,
                answer_keyword_hit=answer_keyword_hit,
                passed=passed,
                answer_text=answer_payload.answer_text,
                top_result_pages=top_result_pages,
                citation_pages=citation_pages,
            )
        )

    question_count = len(cases)
    metrics = EvaluationMetrics(
        question_count=question_count,
        retrieval_hit_rate=_rate(retrieval_hits, question_count),
        citation_hit_rate=_rate(citation_hits, question_count),
        answer_keyword_hit_rate=_rate(answer_keyword_hits, question_count),
        overall_pass_rate=_rate(passes, question_count),
    )

    return EvaluationRunResponse(
        suite_id=suite["suite_id"],
        suite_name=suite["suite_name"],
        document_id=document_id,
        metrics=metrics,
        cases=cases,
    )
