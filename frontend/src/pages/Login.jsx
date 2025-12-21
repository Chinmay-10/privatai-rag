import { useState } from "react";
import api from "../api";

export default function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const submit = async () => {
  try {
    const res = await api.post("/auth/login", {
      username,
      password,
    }); // JSON body — EXACTLY like Swagger

    localStorage.setItem("token", res.data.access_token);
    window.location.href = "/";
  } catch (err) {
    alert("Invalid credentials");
    console.error(err);
  }
};


  return (
    <div className="min-h-screen flex items-center justify-center">
      <div className="bg-white w-96 p-8 rounded-lg shadow-sm border">
        <h1 className="text-2xl font-semibold mb-6 text-center">Sign in</h1>

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
          Login
        </button>

        <p className="text-sm text-center mt-4">
          No account? <a href="/signup" className="text-indigo-600">Sign up</a>
        </p>
      </div>
    </div>
  );
}
