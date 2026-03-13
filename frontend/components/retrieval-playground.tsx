"use client";

import { useEffect, useState } from "react";

import { getApiBaseUrl, getApiErrorMessage, parseJsonSafely } from "@/lib/api";
import {
  DocumentChunksResponse,
  isDocumentChunksResponse,
  isRetrievalSearchResponse,
  RetrievalSearchResponse
} from "@/lib/document-ai";

type RetrievalPlaygroundProps = {
  documentId: string;
  filename: string;
};

export function RetrievalPlayground({
  documentId,
  filename
}: RetrievalPlaygroundProps) {
  const [query, setQuery] = useState("terminate notice");
  const [chunkPayload, setChunkPayload] = useState<DocumentChunksResponse | null>(null);
  const [searchPayload, setSearchPayload] = useState<RetrievalSearchResponse | null>(null);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [isLoadingChunks, setIsLoadingChunks] = useState(false);
  const [isSearching, setIsSearching] = useState(false);

  useEffect(() => {
    let ignore = false;

    async function loadChunks() {
      setIsLoadingChunks(true);
      setErrorMessage(null);
      setChunkPayload(null);
      setSearchPayload(null);

      try {
        const apiBaseUrl = getApiBaseUrl();
        const response = await fetch(`${apiBaseUrl}/documents/${documentId}/chunks`);
        const payload = await parseJsonSafely(response);

        if (!response.ok) {
          throw new Error(getApiErrorMessage(payload) ?? "chunk 목록 조회 중 오류가 발생했습니다.");
        }
        if (!isDocumentChunksResponse(payload)) {
          throw new Error("chunk 응답을 해석할 수 없습니다.");
        }

        if (!ignore) {
          setChunkPayload(payload);
        }
      } catch (error) {
        if (!ignore) {
          setErrorMessage(
            error instanceof Error ? error.message : "chunk 조회 중 알 수 없는 오류가 발생했습니다."
          );
        }
      } finally {
        if (!ignore) {
          setIsLoadingChunks(false);
        }
      }
    }

    void loadChunks();

    return () => {
      ignore = true;
    };
  }, [documentId]);

  async function handleSearch(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setIsSearching(true);
    setErrorMessage(null);

    try {
      const apiBaseUrl = getApiBaseUrl();
      const response = await fetch(`${apiBaseUrl}/retrieval/search`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          document_id: documentId,
          query,
          top_k: 3
        })
      });

      const payload = await parseJsonSafely(response);
      if (!response.ok) {
        throw new Error(getApiErrorMessage(payload) ?? "retrieval 검색 중 오류가 발생했습니다.");
      }
      if (!isRetrievalSearchResponse(payload)) {
        throw new Error("retrieval 응답을 해석할 수 없습니다.");
      }

      setSearchPayload(payload);
    } catch (error) {
      setErrorMessage(
        error instanceof Error ? error.message : "retrieval 검색 중 알 수 없는 오류가 발생했습니다."
      );
    } finally {
      setIsSearching(false);
    }
  }

  return (
    <section className="mt-6 rounded-[2rem] border border-slate-200 bg-white/85 p-6 shadow-[0_24px_80px_rgba(15,23,42,0.06)] backdrop-blur">
      <div className="flex flex-wrap items-start justify-between gap-4">
        <div>
          <p className="text-sm font-medium uppercase tracking-[0.2em] text-slate-500">
            Phase 2 Retrieval
          </p>
          <h3 className="mt-3 text-2xl font-semibold text-slate-950">
            Chunking And Search Playground
          </h3>
          <p className="mt-2 max-w-2xl text-sm leading-6 text-slate-600">
            업로드된 문서를 chunk 단위로 나누고, 질문에 대해 가장 관련성이 높은 chunk를
            찾는 baseline retrieval 흐름입니다.
          </p>
        </div>
        <div className="rounded-full border border-emerald-200 bg-emerald-50 px-4 py-2 text-sm text-emerald-700">
          {filename}
        </div>
      </div>

      <form
        className="mt-6 grid gap-4 rounded-3xl border border-slate-200 bg-slate-50 p-5"
        onSubmit={handleSearch}
      >
        <label className="grid gap-2 text-sm font-medium text-slate-700">
          Search query
          <input
            className="rounded-2xl border border-slate-300 bg-white px-4 py-3 text-sm text-slate-900 outline-none transition focus:border-slate-500"
            onChange={(event) => {
              setQuery(event.target.value);
            }}
            placeholder="예: terminate notice"
            value={query}
          />
        </label>

        <div className="flex flex-wrap items-center justify-between gap-3">
          <p className="text-sm text-slate-500">
            {chunkPayload ? `${chunkPayload.chunk_count}개 chunk가 준비됨` : "chunk 로딩 중"}
          </p>
          <button
            className="rounded-full bg-emerald-600 px-5 py-3 text-sm font-medium text-white transition hover:bg-emerald-500 disabled:cursor-not-allowed disabled:bg-emerald-300"
            disabled={isSearching || isLoadingChunks}
            type="submit"
          >
            {isSearching ? "Searching..." : "Run Retrieval"}
          </button>
        </div>

        {errorMessage ? (
          <div className="rounded-2xl border border-rose-200 bg-rose-50 px-4 py-3 text-sm text-rose-700">
            {errorMessage}
          </div>
        ) : null}
      </form>

      <div className="mt-6 grid gap-6 xl:grid-cols-[0.95fr_1.05fr]">
        <div className="rounded-3xl border border-slate-200 bg-slate-50 p-5">
          <div className="flex items-center justify-between gap-3">
            <p className="text-sm font-medium uppercase tracking-[0.2em] text-slate-500">
              Chunk preview
            </p>
            <span className="rounded-full bg-white px-3 py-1 text-xs text-slate-600">
              {isLoadingChunks ? "Loading..." : chunkPayload?.chunk_count ?? 0}
            </span>
          </div>

          <div className="mt-4 grid gap-3">
            {chunkPayload?.chunks.map((chunk) => (
              <article
                key={chunk.chunk_id}
                className="rounded-2xl border border-slate-200 bg-white px-4 py-4"
              >
                <div className="flex flex-wrap items-center justify-between gap-2">
                  <p className="text-sm font-semibold text-slate-900">
                    Page {chunk.page_number} / Chunk {chunk.chunk_index + 1}
                  </p>
                  <span className="rounded-full bg-slate-100 px-3 py-1 text-xs text-slate-600">
                    {chunk.word_count} words
                  </span>
                </div>
                <p className="mt-3 text-sm leading-6 text-slate-600">{chunk.text_preview}</p>
              </article>
            ))}
          </div>
        </div>

        <div className="rounded-3xl border border-slate-200 bg-slate-950 p-5 text-slate-50">
          <div className="flex items-center justify-between gap-3">
            <p className="text-sm font-medium uppercase tracking-[0.2em] text-slate-300">
              Top-k results
            </p>
            <span className="rounded-full bg-white/10 px-3 py-1 text-xs text-slate-200">
              {searchPayload?.results.length ?? 0} results
            </span>
          </div>

          <div className="mt-4 grid gap-3">
            {searchPayload?.results.map((result) => (
              <article
                key={result.chunk_id}
                className="rounded-2xl bg-white/10 px-4 py-4"
              >
                <div className="flex flex-wrap items-center justify-between gap-2">
                  <p className="text-sm font-semibold text-white">
                    Page {result.page_number} / Chunk {result.chunk_index + 1}
                  </p>
                  <span className="rounded-full bg-white/15 px-3 py-1 text-xs text-slate-200">
                    score {result.score.toFixed(4)}
                  </span>
                </div>
                <p className="mt-3 whitespace-pre-wrap text-sm leading-6 text-slate-100">
                  {result.text}
                </p>
              </article>
            ))}

            {!searchPayload ? (
              <div className="rounded-2xl border border-dashed border-white/20 px-4 py-8 text-sm text-slate-300">
                쿼리를 입력하고 retrieval 결과를 확인하세요.
              </div>
            ) : null}
          </div>
        </div>
      </div>
    </section>
  );
}
