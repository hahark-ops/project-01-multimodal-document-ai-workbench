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
