import Layout from "../components/Layout";

export default function Dashboard() {
  return (
    <Layout title="Dashboard">
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">

        <a href="/upload" className="bg-white border rounded-lg p-6 hover:shadow-sm">
          <h3 className="font-semibold mb-2">Upload Documents</h3>
          <p className="text-sm text-slate-600">
            Securely upload and index documents.
          </p>
        </a>

        <a href="/query" className="bg-white border rounded-lg p-6 hover:shadow-sm">
          <h3 className="font-semibold mb-2">Query Knowledge</h3>
          <p className="text-sm text-slate-600">
            Ask questions over your documents.
          </p>
        </a>

        <a href="/documents" className="bg-white border rounded-lg p-6 hover:shadow-sm">
          <h3 className="font-semibold mb-2">Documents</h3>
          <p className="text-sm text-slate-600">
            View uploaded documents.
          </p>
        </a>

      </div>
    </Layout>
  );
}
