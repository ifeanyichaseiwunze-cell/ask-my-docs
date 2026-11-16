"use client";

import { useState } from "react";

type AskRespone = {
  question: string;
  answer: string;
  cached: boolean;
  sources?: string[];
};

const API_URL = "http://127.0.0.1:8000";

export default function Home() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [cached, setCached] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [sources, setSources] = useState<string[]>([]);

  async function handleAsk() {
    if (!question.trim()) return;

    setLoading(true);
    setError("");
    setAnswer("");
    setSources([]);

    try {
      const res = await fetch(`${API_URL}/ask`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question }),
      });
      if (!res.ok) throw new Error();
      const data: AskRespone = await res.json();
      setAnswer(data.answer);
      setCached(data.cached);
      setSources(data.sources ?? []);
    } catch {
      setError("Couldn't reach the backend. Is uvicorn running?");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="mx-auto max-w-2xl p-8">
      <h1 className="mb-6 text-3xl font-bold">Ask My Docs</h1>
      <textarea
        className="w-full rounded border bg-white p-3 text-black"
        rows={3}
        placeholder="Ask a question..."
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
      />

      <button
        className="mt-3 rounded bg-blue-600 px-5 py-2 text-white disabled:opacity-50"
        onClick={handleAsk}
        disabled={loading}
      >
        {loading ? "Thinking..." : "Ask"}
      </button>

      {error && <p className="mt-4 text-red-500">{error}</p>}

      {answer && (
        <div className="mt-6 rounded border p-4">
          <p className="whitespace-pre-wrap">{answer}</p>
          <p className="mt-2 text-sm text-gray-500">
            {cached ? "This was loaded from the memory in our chats" : "This is an answer not from our chats."}
          </p>
          {sources.length > 0 && (
            <p className="mt-1 text-sm text-gray-500">Sources: {sources.join(", ")}</p>
          )}
        </div>
      )}
    </main>
  );
}