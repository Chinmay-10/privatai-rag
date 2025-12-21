import { logout } from "../auth";

export default function Layout({ title, children }) {
  return (
    <div className="min-h-screen">
      {/* Header */}
      <header className="bg-white border-b">
        <div className="max-w-6xl mx-auto px-6 py-4 flex justify-between items-center">
          <h1 className="font-semibold text-lg">PrivatAI RAG</h1>
          <button
            onClick={logout}
            className="text-sm text-slate-600 hover:text-black"
          >
            Logout
          </button>
        </div>

        {/* Navigation */}
        <nav className="border-t bg-slate-50">
          <div className="max-w-6xl mx-auto px-6 py-3 flex gap-6 text-sm">
            <a href="/" className="hover:text-indigo-600">Dashboard</a>
            <a href="/upload" className="hover:text-indigo-600">Upload</a>
            <a href="/query" className="hover:text-indigo-600">Query</a>
            <a href="/documents" className="hover:text-indigo-600">Documents</a>
            <a href="/audit" className="hover:text-indigo-600">Audit</a>
          </div>
        </nav>
      </header>

      {/* Page content */}
      <main className="max-w-6xl mx-auto px-6 py-8">
        <h2 className="text-2xl font-semibold mb-6">{title}</h2>
        {children}
      </main>
    </div>
  );
}
