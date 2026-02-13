import { StudioShellNav } from "@/components/studio-shell-nav";

export default function LibraryPage() {
  return (
    <main>
      <StudioShellNav />
      <section className="panel p-6">
        <h1 className="text-2xl font-black">Project Library</h1>
        <p className="mt-2 max-w-3xl text-sm text-black/70">
          This area is reserved for conversation history, saved workflow templates, and reusable
          media bundles. In the initial bootstrap phase, the canonical storage remains in backend
          workspace/conversation APIs.
        </p>
        <ul className="mt-4 list-disc space-y-1 pl-5 text-sm text-black/70">
          <li>Conversation sessions grouped by workspace</li>
          <li>Imported workflow templates from `workflows/templates`</li>
          <li>Reusable asset packs ready for injection into new projects</li>
        </ul>
      </section>
    </main>
  );
}
