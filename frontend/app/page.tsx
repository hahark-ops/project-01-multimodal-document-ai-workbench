import { DocumentUploader } from "@/components/document-uploader";

const deliverables = [
  "PDF upload",
  "Local file storage",
  "Page-by-page text extraction",
  "Chunk metadata generation",
  "Top-k retrieval playground"
];

const nextPhases = [
  "Grounded answer with citation",
  "Summary and evaluation"
];

export default function HomePage() {
  return (
    <main className="min-h-screen bg-[radial-gradient(circle_at_top_left,_#ffe2b8,_transparent_28%),radial-gradient(circle_at_top_right,_#d8eef9,_transparent_28%),linear-gradient(180deg,_#fffdf8,_#f3f7fb)] text-slate-900">
      <section className="mx-auto flex min-h-screen max-w-7xl flex-col gap-8 px-6 py-10 md:px-10">
        <div className="flex flex-wrap items-start justify-between gap-4">
          <div>
            <p className="text-sm font-medium uppercase tracking-[0.3em] text-slate-500">
              AWS AI School Portfolio
            </p>
            <h1 className="mt-3 max-w-4xl text-4xl font-semibold tracking-tight text-slate-950 md:text-6xl">
              Multimodal Document AI Workbench
            </h1>
            <p className="mt-4 max-w-3xl text-base leading-7 text-slate-600 md:text-lg">
              텍스트, 표, 이미지가 섞인 PDF 문서를 대상으로 근거 기반 검색과 응답을 만드는
              프로젝트입니다. 지금은 Phase 2로 chunking과 retrieval foundation까지 연결한
              상태입니다.
            </p>
          </div>
          <div className="rounded-full border border-slate-300/80 bg-white/70 px-4 py-2 text-sm text-slate-700 shadow-sm backdrop-blur">
            Phase 2: Retrieval foundation
          </div>
        </div>

        <div className="grid gap-6 xl:grid-cols-[1.15fr_0.85fr]">
          <DocumentUploader />

          <div className="space-y-6">
            <section className="rounded-[2rem] border border-slate-200 bg-white/80 p-6 shadow-[0_24px_80px_rgba(15,23,42,0.06)] backdrop-blur">
              <p className="text-sm font-medium uppercase tracking-[0.2em] text-slate-500">
                Current deliverables
              </p>
              <ul className="mt-5 space-y-3">
                {deliverables.map((item) => (
                  <li
                    key={item}
                    className="rounded-2xl border border-slate-200 bg-slate-50 px-4 py-4 text-sm font-medium text-slate-700"
                  >
                    {item}
                  </li>
                ))}
              </ul>
            </section>

            <section className="rounded-[2rem] border border-slate-200 bg-slate-950 p-6 text-slate-50 shadow-[0_24px_80px_rgba(15,23,42,0.09)]">
              <p className="text-sm font-medium uppercase tracking-[0.2em] text-slate-300">
                Next phases
              </p>
              <ol className="mt-5 space-y-3">
                {nextPhases.map((item, index) => (
                  <li key={item} className="flex items-center gap-4 rounded-2xl bg-white/10 px-4 py-4">
                    <span className="flex h-9 w-9 items-center justify-center rounded-full bg-white text-sm font-semibold text-slate-950">
                      {index + 3}
                    </span>
                    <span className="text-sm text-slate-100">{item}</span>
                  </li>
                ))}
              </ol>
            </section>
          </div>
        </div>
      </section>
    </main>
  );
}
