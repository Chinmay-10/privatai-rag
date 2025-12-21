import { useEffect, useState } from "react";
import api from "../api";

export default function Documents() {
  const [docs, setDocs] = useState([]);

  useEffect(() => {
    api.get("/documents/").then(res => setDocs(res.data));
  }, []);

  return (
    <div className="p-6">
      <h2 className="text-xl font-semibold mb-4">Documents</h2>

      {docs.length === 0 && <p>No documents uploaded.</p>}

      <ul className="list-disc pl-6">
        {docs.map((d, i) => (
          <li key={i}>{d}</li>
        ))}
      </ul>
    </div>
  );
}
