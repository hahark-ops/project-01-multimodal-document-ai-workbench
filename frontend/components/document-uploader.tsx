"use client";

import { startTransition, useState } from "react";

type UploadPageSummary = {
  page_number: number;
  char_count: number;
  text_preview: string;
};

type UploadResponse = {
  document_id: string;
  filename: string;
  status: string;
  page_count: number;
  pages: UploadPageSummary[];
};

type PageDetail = {
  page_number: number;
  char_count: number;
  text: string;
};

type DocumentDetail = {
  document_id: string;
  filename: string;
  status: string;
  page_count: number;
  pages: PageDetail[];
};

type APIError = {
  error?: {
    code: string;
    message: string;
  };
};

function getApiBaseUrl(): string {
  if (process.env.NEXT_PUBLIC_API_BASE_URL) {
    return process.env.NEXT_PUBLIC_API_BASE_URL;
  }

  if (typeof window === "undefined") {
    return "http://localhost:8000";
  }

  const { protocol, hostname } = window.location;
  if (hostname === "localhost" || hostname === "127.0.0.1") {
    return `${protocol}//${hostname}:8000`;
  }

  throw new Error("NEXT_PUBLIC_API_BASE_URL must be set outside local development.");
}

async function parseJsonSafely(response: Response): Promise<unknown | null> {
  const responseText = await response.text();
  if (!responseText) {
    return null;
  }

  try {
    return JSON.parse(responseText) as unknown;
  } catch {
    return null;
  }
}

function truncateText(text: string, maxLength: number): string {
  if (text.length <= maxLength) {
    return text;
  }
  return `${text.slice(0, maxLength)}...`;
}

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === "object" && value !== null;
}

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

function isUploadResponse(value: unknown): value is UploadResponse {
  return (
    isRecord(value) &&
    typeof value.document_id === "string" &&
    typeof value.filename === "string" &&
    typeof value.status === "string" &&
    typeof value.page_count === "number" &&
    Array.isArray(value.pages) &&
    value.pages.every(isUploadPageSummary)
  );
}

function isDocumentDetail(value: unknown): value is DocumentDetail {
  return (
    isRecord(value) &&
    typeof value.document_id === "string" &&
    typeof value.filename === "string" &&
    typeof value.status === "string" &&
    typeof value.page_count === "number" &&
    Array.isArray(value.pages) &&
    value.pages.every(isPageDetail)
  );
}

function getApiErrorMessage(value: unknown): string | null {
  if (!isRecord(value)) {
    return null;
  }

  const error = value.error;
  if (!isRecord(error) || typeof error.message !== "string") {
    return null;
  }

  return error.message;
}

export function DocumentUploader() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [uploadResult, setUploadResult] = useState<UploadResponse | null>(null);
  const [documentDetail, setDocumentDetail] = useState<DocumentDetail | null>(null);

  async function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();

    if (!selectedFile) {
      setErrorMessage("먼저 PDF 파일을 선택해 주세요.");
      return;
    }

    setIsSubmitting(true);
    setErrorMessage(null);
    setUploadResult(null);
    setDocumentDetail(null);

    try {
      const apiBaseUrl = getApiBaseUrl();
      const formData = new FormData();
      formData.append("file", selectedFile);

      const uploadResponse = await fetch(`${apiBaseUrl}/documents/upload`, {
        method: "POST",
        body: formData
      });

      const uploadPayload = await parseJsonSafely(uploadResponse);
      if (!uploadResponse.ok) {
        throw new Error(getApiErrorMessage(uploadPayload) ?? "업로드 중 오류가 발생했습니다.");
      }
      if (!isUploadResponse(uploadPayload)) {
        throw new Error("업로드 응답을 해석할 수 없습니다.");
      }

      const parsedSummary: UploadResponse = uploadPayload;
      setUploadResult(parsedSummary);

      const detailResponse = await fetch(`${apiBaseUrl}/documents/${parsedSummary.document_id}`);
      const detailPayload = await parseJsonSafely(detailResponse);
      if (!detailResponse.ok) {
        throw new Error(
          getApiErrorMessage(detailPayload) ?? "파싱 결과 조회 중 오류가 발생했습니다."
        );
      }
      if (!isDocumentDetail(detailPayload)) {
        throw new Error("상세 응답을 해석할 수 없습니다.");
      }

      startTransition(() => {
        setDocumentDetail(detailPayload);
      });
    } catch (error) {
      setErrorMessage(
        error instanceof Error ? error.message : "알 수 없는 오류가 발생했습니다."
      );
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <section className="rounded-[2rem] border border-slate-200 bg-white/80 p-6 shadow-[0_24px_80px_rgba(15,23,42,0.06)] backdrop-blur">
      <div className="flex flex-wrap items-start justify-between gap-4">
        <div>
          <p className="text-sm font-medium uppercase tracking-[0.2em] text-slate-500">
            Phase 1 Demo
          </p>
          <h2 className="mt-3 text-2xl font-semibold text-slate-950">
            Upload And Parse A PDF
          </h2>
          <p className="mt-2 max-w-2xl text-sm leading-6 text-slate-600">
            현재 단계에서는 PDF 업로드, 로컬 저장, 페이지별 텍스트 추출, 결과 확인까지를
            하나의 vertical slice로 구현합니다.
          </p>
        </div>
        <div className="rounded-full border border-slate-300 bg-slate-50 px-4 py-2 text-sm text-slate-700">
          Backend contract aligned
        </div>
      </div>

      <form
        className="mt-6 grid gap-4 rounded-3xl border border-slate-200 bg-slate-50 p-5"
        onSubmit={handleSubmit}
      >
        <label className="grid gap-2 text-sm font-medium text-slate-700">
          PDF file
          <input
            accept="application/pdf"
            className="rounded-2xl border border-slate-300 bg-white px-4 py-3 text-sm text-slate-900 outline-none transition focus:border-slate-500"
            onChange={(event) => {
              const nextFile = event.target.files?.[0] ?? null;
              setSelectedFile(nextFile);
            }}
            type="file"
          />
        </label>

        <div className="flex flex-wrap items-center justify-between gap-3">
          <p className="text-sm text-slate-500">
            {selectedFile ? `${selectedFile.name} 선택됨` : "아직 선택된 파일이 없습니다."}
          </p>
          <button
            className="rounded-full bg-slate-950 px-5 py-3 text-sm font-medium text-white transition hover:bg-slate-800 disabled:cursor-not-allowed disabled:bg-slate-400"
            disabled={isSubmitting}
            type="submit"
          >
            {isSubmitting ? "Parsing..." : "Upload PDF"}
          </button>
        </div>

        {errorMessage ? (
          <div className="rounded-2xl border border-rose-200 bg-rose-50 px-4 py-3 text-sm text-rose-700">
            {errorMessage}
          </div>
        ) : null}
      </form>

      {uploadResult ? (
        <div className="mt-6 rounded-3xl bg-slate-950 p-5 text-slate-50">
          <p className="text-sm uppercase tracking-[0.2em] text-slate-300">Upload summary</p>
          <div className="mt-4 grid gap-3 md:grid-cols-3">
            <div className="rounded-2xl bg-white/10 px-4 py-4">
              <p className="text-xs uppercase tracking-[0.2em] text-slate-300">Filename</p>
              <p className="mt-2 text-sm font-medium text-white">{uploadResult.filename}</p>
            </div>
            <div className="rounded-2xl bg-white/10 px-4 py-4">
              <p className="text-xs uppercase tracking-[0.2em] text-slate-300">Status</p>
              <p className="mt-2 text-sm font-medium text-white">{uploadResult.status}</p>
            </div>
            <div className="rounded-2xl bg-white/10 px-4 py-4">
              <p className="text-xs uppercase tracking-[0.2em] text-slate-300">Pages</p>
              <p className="mt-2 text-sm font-medium text-white">{uploadResult.page_count}</p>
            </div>
          </div>
        </div>
      ) : null}

      {documentDetail ? (
        <div className="mt-6 grid gap-4">
          {documentDetail.pages.map((page) => (
            <article
              key={`${documentDetail.document_id}-${page.page_number}`}
              className="rounded-3xl border border-slate-200 bg-white px-5 py-5 shadow-sm"
            >
              <div className="flex items-center justify-between gap-3">
                <p className="text-sm font-semibold text-slate-900">Page {page.page_number}</p>
                <span className="rounded-full bg-slate-100 px-3 py-1 text-xs text-slate-600">
                  {page.char_count} chars
                </span>
              </div>
              <p className="mt-3 text-xs uppercase tracking-[0.2em] text-slate-400">
                Preview
              </p>
              <p className="mt-2 rounded-2xl bg-amber-50 px-4 py-3 text-sm leading-6 text-slate-700">
                {truncateText(page.text, 220)}
              </p>
              <p className="mt-4 text-xs uppercase tracking-[0.2em] text-slate-400">
                Full page text
              </p>
              <p className="mt-2 whitespace-pre-wrap text-sm leading-6 text-slate-700">
                {page.text || "이 페이지에서는 추출된 텍스트가 없습니다."}
              </p>
            </article>
          ))}
        </div>
      ) : null}
    </section>
  );
}
