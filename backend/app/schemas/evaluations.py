from pydantic import BaseModel, Field


class EvaluationRunRequest(BaseModel):
    document_id: str = Field(..., min_length=1)
    suite_id: str = "nc_dac_sample_contract_v1"
    top_k: int = Field(default=3, ge=1, le=10)
    max_citations: int = Field(default=2, ge=1, le=5)


class EvaluationMetrics(BaseModel):
    question_count: int
    retrieval_hit_rate: float
    citation_hit_rate: float
    answer_keyword_hit_rate: float
    overall_pass_rate: float


class EvaluationCaseResult(BaseModel):
    question_id: str
    question: str
    expected_page: int
    expected_keywords: list[str]
    retrieval_hit: bool
    citation_hit: bool
    answer_keyword_hit: bool
    passed: bool
    answer_text: str
    top_result_pages: list[int]
    citation_pages: list[int]


class EvaluationRunResponse(BaseModel):
    suite_id: str
    suite_name: str
    document_id: str
    metrics: EvaluationMetrics
    cases: list[EvaluationCaseResult]
