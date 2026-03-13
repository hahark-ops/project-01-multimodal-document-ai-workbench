"use client";

import { startTransition, useState } from "react";

type DocumentPage = {
  page_number: number;
  text: string;
  char_count: number;
};

type DocumentDetail = {
  id: string;
  filename: string;
  status: string;
  created_at: string;
  page_count: number;
  extracted_char_count: number;
  pages: DocumentPage[];
};

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";

function truncateText(text: string, maxLength: number) {
  if (text.length <= maxLength) {
    return text;
  }
  return `${text.slice(0, maxLength)}...`;
}

export function DocumentUploader() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [document, setDocument] = useState<DocumentDetail | null>(null);

  async function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();

    if (!selectedFile) {
      setErrorMessage("먼저 PDF 파일을 선택해 주세요.");
      return;
    }

    setIsSubmitting(true);
    setErrorMessage(null);

    const formData = new FormData();
    formData.append("file", selectedFile);

    try {
      const response = await fetch(`${API_BASE_URL}/documents/upload`, {
        method: "POST",
        body: formData
      });
      const payload = (await response.json()) as { detail?: string; document?: DocumentDetail };

      if (!response.ok || !payload.document) {
        throw new Error(payload.detail ?? "업로드 중 오류가 발생했습니다.");
      }

      const parsedDocument = payload.document;

      startTransition(() => {
        setDocument(parsedDocument);
      });
    } catch (error) {
      setDocument(null);
      setErrorMessage(error instanceof Error ? error.message : "알 수 없는 오류가 발생했습니다.");
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <section className="rounded-[2rem] border border-slate-200 bg-white/85 p-6 shadow-[0_24px_80px_rgba(15,23,42,0.05)] backdrop-blur">
      <div className="flex flex-wrap items-start justify-between gap-4">
        <div>
          <p className="text-sm font-medium uppercase tracking-[0.2em] text-slate-500">
            Live demo
          </p>
          <h2 className="mt-3 text-2xl font-semibold text-slate-950">PDF Upload And Parse</h2>
          <p className="mt-2 max-w-2xl text-sm leading-6 text-slate-600">
            현재 단계에서는 PDF를 업로드하면 백엔드가 파일을 저장하고, 페이지별 텍스트를
            추출해서 바로 반환합니다.
          </p>
        </div>
        <div className="rounded-full border border-emerald-200 bg-emerald-50 px-4 py-2 text-sm text-emerald-700">
          Backend connected
        </div>
      </div>

      <form className="mt-6 grid gap-4 rounded-3xl border border-slate-200 bg-slate-50 p-5" onSubmit={handleSubmit}>
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
            {isSubmitting ? "Uploading..." : "Upload PDF"}
          </button>
        </div>

        {errorMessage ? (
          <div className="rounded-2xl border border-rose-200 bg-rose-50 px-4 py-3 text-sm text-rose-700">
            {errorMessage}
          </div>
        ) : null}
      </form>

      {document ? (
        <div className="mt-6 grid gap-4">
          <div className="rounded-3xl border border-slate-200 bg-slate-950 p-5 text-slate-50">
            <p className="text-sm uppercase tracking-[0.2em] text-slate-300">Parsed result</p>
            <div className="mt-4 grid gap-3 md:grid-cols-3">
              <div className="rounded-2xl bg-white/10 px-4 py-4">
                <p className="text-xs uppercase tracking-[0.2em] text-slate-300">Filename</p>
                <p className="mt-2 text-sm font-medium text-white">{document.filename}</p>
              </div>
              <div className="rounded-2xl bg-white/10 px-4 py-4">
                <p className="text-xs uppercase tracking-[0.2em] text-slate-300">Pages</p>
                <p className="mt-2 text-sm font-medium text-white">{document.page_count}</p>
              </div>
              <div className="rounded-2xl bg-white/10 px-4 py-4">
                <p className="text-xs uppercase tracking-[0.2em] text-slate-300">Extracted chars</p>
                <p className="mt-2 text-sm font-medium text-white">{document.extracted_char_count}</p>
              </div>
            </div>
          </div>

          <div className="grid gap-4">
            {document.pages.map((page) => (
              <article
                key={`${document.id}-${page.page_number}`}
                className="rounded-3xl border border-slate-200 bg-white px-5 py-5 shadow-sm"
              >
                <div className="flex items-center justify-between gap-3">
                  <p className="text-sm font-semibold text-slate-900">Page {page.page_number}</p>
                  <span className="rounded-full bg-slate-100 px-3 py-1 text-xs text-slate-600">
                    {page.char_count} chars
                  </span>
                </div>
                <p className="mt-3 whitespace-pre-wrap text-sm leading-6 text-slate-700">
                  {page.text ? truncateText(page.text, 600) : "이 페이지에서는 추출된 텍스트가 없습니다."}
                </p>
              </article>
            ))}
          </div>
        </div>
      ) : null}
    </section>
  );
}
