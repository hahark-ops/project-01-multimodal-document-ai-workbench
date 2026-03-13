import { isRecord } from "@/lib/api";

export type UploadPageSummary = {
  page_number: number;
  char_count: number;
  text_preview: string;
};

export type UploadResponse = {
  document_id: string;
  filename: string;
  status: string;
  page_count: number;
  chunk_count: number;
  pages: UploadPageSummary[];
};

export type PageDetail = {
  page_number: number;
  char_count: number;
  text: string;
};

export type DocumentDetail = {
  document_id: string;
  filename: string;
  status: string;
  page_count: number;
  chunk_count: number;
  pages: PageDetail[];
};

export type ChunkPreview = {
  chunk_id: string;
  document_id: string;
  page_number: number;
  chunk_index: number;
  char_count: number;
  word_count: number;
  text_preview: string;
};

export type DocumentChunksResponse = {
  document_id: string;
  chunk_count: number;
  chunks: ChunkPreview[];
};

export type RetrievalResult = {
  chunk_id: string;
  document_id: string;
  page_number: number;
  chunk_index: number;
  char_count: number;
  word_count: number;
  score: number;
  text: string;
};

export type RetrievalSearchResponse = {
  query: string;
  document_id?: string;
  top_k: number;
  results: RetrievalResult[];
};

export type Citation = {
  citation_id: string;
  chunk_id: string;
  page_number: number;
  chunk_index: number;
  score: number;
  excerpt: string;
};

export type GroundedAnswerResponse = {
  question: string;
  document_id: string;
  answer_text: string;
  answer_strategy: string;
  top_k: number;
  citations: Citation[];
  latency_ms: number;
};

export type SummaryHighlight = {
  highlight_id: string;
  page_number: number;
  chunk_index: number;
  importance_score: number;
  excerpt: string;
};

export type SummaryResponse = {
  document_id: string;
  summary_text: string;
  key_points: string[];
  highlights: SummaryHighlight[];
  summary_strategy: string;
  latency_ms: number;
};

export type EvaluationMetrics = {
  question_count: number;
  retrieval_hit_rate: number;
  citation_hit_rate: number;
  answer_keyword_hit_rate: number;
  overall_pass_rate: number;
};

export type EvaluationCaseResult = {
  question_id: string;
  question: string;
  expected_page: number;
  expected_keywords: string[];
  retrieval_hit: boolean;
  citation_hit: boolean;
  answer_keyword_hit: boolean;
  passed: boolean;
  answer_text: string;
  top_result_pages: number[];
  citation_pages: number[];
};

export type EvaluationRunResponse = {
  suite_id: string;
  suite_name: string;
  document_id: string;
  metrics: EvaluationMetrics;
  cases: EvaluationCaseResult[];
};

function isUploadPageSummary(value: unknown): value is UploadPageSummary {
  return (
    isRecord(value) &&
    typeof value.page_number === "number" &&
    typeof value.char_count === "number" &&
    typeof value.text_preview === "string"
  );
}

function isPageDetail(value: unknown): value is PageDetail {
  return (
    isRecord(value) &&
    typeof value.page_number === "number" &&
    typeof value.char_count === "number" &&
    typeof value.text === "string"
  );
}

function isChunkPreview(value: unknown): value is ChunkPreview {
  return (
    isRecord(value) &&
    typeof value.chunk_id === "string" &&
    typeof value.document_id === "string" &&
    typeof value.page_number === "number" &&
    typeof value.chunk_index === "number" &&
    typeof value.char_count === "number" &&
    typeof value.word_count === "number" &&
    typeof value.text_preview === "string"
  );
}

function isRetrievalResult(value: unknown): value is RetrievalResult {
  return (
    isRecord(value) &&
    typeof value.chunk_id === "string" &&
    typeof value.document_id === "string" &&
    typeof value.page_number === "number" &&
    typeof value.chunk_index === "number" &&
    typeof value.char_count === "number" &&
    typeof value.word_count === "number" &&
    typeof value.score === "number" &&
    typeof value.text === "string"
  );
}

function isCitation(value: unknown): value is Citation {
  return (
    isRecord(value) &&
    typeof value.citation_id === "string" &&
    typeof value.chunk_id === "string" &&
    typeof value.page_number === "number" &&
    typeof value.chunk_index === "number" &&
    typeof value.score === "number" &&
    typeof value.excerpt === "string"
  );
}

function isSummaryHighlight(value: unknown): value is SummaryHighlight {
  return (
    isRecord(value) &&
    typeof value.highlight_id === "string" &&
    typeof value.page_number === "number" &&
    typeof value.chunk_index === "number" &&
    typeof value.importance_score === "number" &&
    typeof value.excerpt === "string"
  );
}

function isEvaluationMetrics(value: unknown): value is EvaluationMetrics {
  return (
    isRecord(value) &&
    typeof value.question_count === "number" &&
    typeof value.retrieval_hit_rate === "number" &&
    typeof value.citation_hit_rate === "number" &&
    typeof value.answer_keyword_hit_rate === "number" &&
    typeof value.overall_pass_rate === "number"
  );
}

function isEvaluationCaseResult(value: unknown): value is EvaluationCaseResult {
  return (
    isRecord(value) &&
    typeof value.question_id === "string" &&
    typeof value.question === "string" &&
    typeof value.expected_page === "number" &&
    Array.isArray(value.expected_keywords) &&
    value.expected_keywords.every((item) => typeof item === "string") &&
    typeof value.retrieval_hit === "boolean" &&
    typeof value.citation_hit === "boolean" &&
    typeof value.answer_keyword_hit === "boolean" &&
    typeof value.passed === "boolean" &&
    typeof value.answer_text === "string" &&
    Array.isArray(value.top_result_pages) &&
    value.top_result_pages.every((item) => typeof item === "number") &&
    Array.isArray(value.citation_pages) &&
    value.citation_pages.every((item) => typeof item === "number")
  );
}

export function isUploadResponse(value: unknown): value is UploadResponse {
  return (
    isRecord(value) &&
    typeof value.document_id === "string" &&
    typeof value.filename === "string" &&
    typeof value.status === "string" &&
    typeof value.page_count === "number" &&
    typeof value.chunk_count === "number" &&
    Array.isArray(value.pages) &&
    value.pages.every(isUploadPageSummary)
  );
}

export function isDocumentDetail(value: unknown): value is DocumentDetail {
  return (
    isRecord(value) &&
    typeof value.document_id === "string" &&
    typeof value.filename === "string" &&
    typeof value.status === "string" &&
    typeof value.page_count === "number" &&
    typeof value.chunk_count === "number" &&
    Array.isArray(value.pages) &&
    value.pages.every(isPageDetail)
  );
}

export function isDocumentChunksResponse(value: unknown): value is DocumentChunksResponse {
  return (
    isRecord(value) &&
    typeof value.document_id === "string" &&
    typeof value.chunk_count === "number" &&
    Array.isArray(value.chunks) &&
    value.chunks.every(isChunkPreview)
  );
}

export function isRetrievalSearchResponse(value: unknown): value is RetrievalSearchResponse {
  return (
    isRecord(value) &&
    typeof value.query === "string" &&
    typeof value.top_k === "number" &&
    Array.isArray(value.results) &&
    value.results.every(isRetrievalResult)
  );
}

export function isGroundedAnswerResponse(value: unknown): value is GroundedAnswerResponse {
  return (
    isRecord(value) &&
    typeof value.question === "string" &&
    typeof value.document_id === "string" &&
    typeof value.answer_text === "string" &&
    typeof value.answer_strategy === "string" &&
    typeof value.top_k === "number" &&
    typeof value.latency_ms === "number" &&
    Array.isArray(value.citations) &&
    value.citations.every(isCitation)
  );
}

export function isSummaryResponse(value: unknown): value is SummaryResponse {
  return (
    isRecord(value) &&
    typeof value.document_id === "string" &&
    typeof value.summary_text === "string" &&
    Array.isArray(value.key_points) &&
    value.key_points.every((item) => typeof item === "string") &&
    Array.isArray(value.highlights) &&
    value.highlights.every(isSummaryHighlight) &&
    typeof value.summary_strategy === "string" &&
    typeof value.latency_ms === "number"
  );
}

export function isEvaluationRunResponse(value: unknown): value is EvaluationRunResponse {
  return (
    isRecord(value) &&
    typeof value.suite_id === "string" &&
    typeof value.suite_name === "string" &&
    typeof value.document_id === "string" &&
    isEvaluationMetrics(value.metrics) &&
    Array.isArray(value.cases) &&
    value.cases.every(isEvaluationCaseResult)
  );
}
