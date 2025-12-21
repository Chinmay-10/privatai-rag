import { useState } from "react";
import api from "../api";

export default function Signup() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const submit = async () => {
    try {
      await api.post("/auth/signup", {
        username,
        password,
        tenant_id: "default",
      });

      alert("Signup successful. Please login.");
      window.location.href = "/login";
    } catch (err) {
      alert("Signup failed");
      console.error(err);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center">
      <div className="bg-white w-96 p-8 rounded-lg shadow-sm border">
        <h1 className="text-2xl font-semibold mb-6 text-center">Create account</h1>

        <input
          className="w-full border rounded px-3 py-2 mb-4"
          placeholder="Username"
          onChange={e => setUsername(e.target.value)}
        />

        <input
          className="w-full border rounded px-3 py-2 mb-6"
          type="password"
          placeholder="Password"
          onChange={e => setPassword(e.target.value)}
        />

        <button
          type="button"   // ✅ CRITICAL FIX
          onClick={submit}
          className="w-full bg-indigo-600 text-white py-2 rounded hover:bg-indigo-700"
        >
          Sign up
        </button>
      </div>
    </div>
  );
}
