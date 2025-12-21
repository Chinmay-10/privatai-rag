import { useEffect, useState } from "react";
import api from "../api";

export default function Audit() {
  const [logs, setLogs] = useState([]);

  useEffect(() => {
    api.get("/audit/").then(res => setLogs(res.data));
  }, []);

  return (
    <div className="p-6">
      <h2 className="text-xl font-semibold mb-4">Audit Logs</h2>

      {logs.length === 0 && <p>No audit logs.</p>}

      <table className="border w-full">
        <thead>
          <tr className="border-b">
            <th className="p-2 text-left">Action</th>
            <th className="p-2 text-left">Resource</th>
            <th className="p-2 text-left">Detail</th>
          </tr>
        </thead>
        <tbody>
          {logs.map(log => (
            <tr key={log.id} className="border-b">
              <td className="p-2">{log.action}</td>
              <td className="p-2">{log.resource}</td>
              <td className="p-2">{log.detail}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
