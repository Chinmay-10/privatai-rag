import { useState } from "react";
import Layout from "../components/Layout";
import api from "../api";

export default function Query() {
  const [q, setQ] = useState("");
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(false);

  const ask = async () => {
    setLoading(true);
    const res = await api.post("/query/", { question: q, top_k: 10 });
    setAnswer(res.data.answer);
    setLoading(false);
  };

  return (
    <Layout title="Query Knowledge">
      <div className="bg-white border rounded-lg p-6 mb-6">
        <textarea
          rows="4"
          className="w-full border rounded p-3 mb-4"
          placeholder="Ask a question..."
          onChange={e => setQ(e.target.value)}
        />

        <button
          onClick={ask}
          disabled={loading}
          className="bg-indigo-600 text-white px-4 py-2 rounded hover:bg-indigo-700"
        >
          {loading ? "Thinking..." : "Ask"}
        </button>
      </div>

      {answer && (
        <div className="bg-white border rounded-lg p-6 relative">
          <button
            onClick={() => navigator.clipboard.writeText(answer)}
            className="absolute top-4 right-4 text-sm text-indigo-600"
          >
            Copy
          </button>
          <p className="whitespace-pre-wrap">{answer}</p>
        </div>
      )}
    </Layout>
  );
}
