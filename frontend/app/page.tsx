import { DocumentUploader } from "@/components/document-uploader";

const pipelineSteps = [
  "Document upload",
  "PDF parsing / OCR",
  "Chunking and metadata",
  "Vector retrieval",
  "Grounded answer with citations"
];

const currentTasks = [
  "Upload API wiring",
  "PyMuPDF parser implementation",
  "Citation-aware answer response",
  "Sample evaluation dataset"
];

export default function HomePage() {
  return (
    <main className="min-h-screen bg-[radial-gradient(circle_at_top_left,_#ffe4ba,_transparent_30%),radial-gradient(circle_at_top_right,_#d9eefc,_transparent_32%),linear-gradient(180deg,_#fffdf7,_#f4f7fb)] text-slate-900">
      <section className="mx-auto flex min-h-screen max-w-6xl flex-col gap-10 px-6 py-10 md:px-10">
        <div className="flex flex-wrap items-center justify-between gap-4">
          <div>
            <p className="text-sm font-medium uppercase tracking-[0.3em] text-slate-500">
              AWS AI School Portfolio
            </p>
            <h1 className="mt-3 max-w-3xl text-4xl font-semibold tracking-tight text-slate-950 md:text-6xl">
              Multimodal Document AI Workbench
            </h1>
          </div>
          <div className="rounded-full border border-slate-300/80 bg-white/70 px-4 py-2 text-sm text-slate-700 shadow-sm backdrop-blur">
            Phase 0.5: Project skeleton
          </div>
        </div>

        <div className="grid gap-6 lg:grid-cols-[1.5fr_1fr]">
          <article className="rounded-[2rem] border border-white/70 bg-white/70 p-8 shadow-[0_24px_80px_rgba(15,23,42,0.08)] backdrop-blur">
            <p className="max-w-2xl text-lg leading-8 text-slate-700">
              계약서, 취업공고, 사내 문서처럼 텍스트와 표, 이미지가 섞인 문서를 업로드하면
              내용을 파싱하고, 근거를 함께 제시하는 질문응답과 요약을 제공하는 문서 AI
              시스템을 만드는 프로젝트입니다.
            </p>

            <div className="mt-8 grid gap-4 md:grid-cols-2">
              <div className="rounded-3xl bg-slate-950 p-5 text-slate-50">
                <p className="text-sm uppercase tracking-[0.2em] text-slate-300">Current focus</p>
                <p className="mt-3 text-2xl font-semibold">Grounded retrieval first</p>
                <p className="mt-2 text-sm leading-6 text-slate-300">
                  답을 잘 생성하는 것보다, 올바른 문단과 페이지를 정확히 찾는 구조를 먼저
                  완성합니다.
                </p>
              </div>
              <div className="rounded-3xl bg-amber-100 p-5 text-amber-950">
                <p className="text-sm uppercase tracking-[0.2em] text-amber-700">Initial stack</p>
                <p className="mt-3 text-2xl font-semibold">Next.js + FastAPI + Qdrant</p>
                <p className="mt-2 text-sm leading-6 text-amber-900/80">
                  구현 가능성과 포트폴리오 설명력을 같이 고려한 시작 조합입니다.
                </p>
              </div>
            </div>
          </article>

          <aside className="rounded-[2rem] border border-slate-200 bg-slate-50/90 p-6 shadow-[0_24px_80px_rgba(15,23,42,0.06)]">
            <p className="text-sm font-medium uppercase tracking-[0.2em] text-slate-500">
              Current tasks
            </p>
            <ul className="mt-4 space-y-3 text-sm text-slate-700">
              {currentTasks.map((task) => (
                <li
                  key={task}
                  className="rounded-2xl border border-slate-200 bg-white px-4 py-3 shadow-sm"
                >
                  {task}
                </li>
              ))}
            </ul>
          </aside>
        </div>

        <section className="grid gap-6 xl:grid-cols-[1.1fr_0.9fr]">
          <div className="space-y-6">
            <DocumentUploader />
          </div>

          <div className="space-y-6">
            <div className="rounded-[2rem] border border-slate-200 bg-white/75 p-6 shadow-[0_24px_80px_rgba(15,23,42,0.05)] backdrop-blur">
              <p className="text-sm font-medium uppercase tracking-[0.2em] text-slate-500">
                Pipeline
              </p>
              <ol className="mt-5 space-y-3">
                {pipelineSteps.map((step, index) => (
                  <li
                    key={step}
                    className="flex items-center gap-4 rounded-2xl border border-slate-200 px-4 py-4"
                  >
                    <span className="flex h-10 w-10 items-center justify-center rounded-full bg-slate-950 text-sm font-semibold text-white">
                      {index + 1}
                    </span>
                    <span className="text-base font-medium text-slate-800">{step}</span>
                  </li>
                ))}
              </ol>
            </div>

            <div className="rounded-[2rem] border border-slate-200 bg-white/75 p-6 shadow-[0_24px_80px_rgba(15,23,42,0.05)] backdrop-blur">
              <p className="text-sm font-medium uppercase tracking-[0.2em] text-slate-500">
                MVP outputs
              </p>
              <div className="mt-5 grid gap-4">
                <div className="rounded-3xl bg-sky-50 p-5">
                  <p className="text-sm text-sky-700">Document summary</p>
                  <p className="mt-2 text-lg font-semibold text-sky-950">
                    핵심 내용을 빠르게 파악할 수 있는 요약
                  </p>
                </div>
                <div className="rounded-3xl bg-emerald-50 p-5">
                  <p className="text-sm text-emerald-700">Evidence-based Q&amp;A</p>
                  <p className="mt-2 text-lg font-semibold text-emerald-950">
                    답변과 함께 근거 문단, 페이지 번호 제공
                  </p>
                </div>
                <div className="rounded-3xl bg-rose-50 p-5">
                  <p className="text-sm text-rose-700">Evaluation logs</p>
                  <p className="mt-2 text-lg font-semibold text-rose-950">
                    retrieval 정확도와 grounded answer 품질 기록
                  </p>
                </div>
              </div>
            </div>
          </div>
        </section>
      </section>
    </main>
  );
}
