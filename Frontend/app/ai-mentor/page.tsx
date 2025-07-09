"use client";

import { useState } from "react";

export default function AiMentorPage() {
  const [query, setQuery] = useState("");
  const [response, setResponse] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim()) return;

    setLoading(true);
    setError("");
    setResponse("");

    try {
      const token = localStorage.getItem("access_token"); 
      const res = await fetch("http://127.0.0.1:8000/api/mentor/mentor-chatbot/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${token}`,
        },
        body: JSON.stringify({ query }),
      });

      if (!res.ok) {
        const errData = await res.json();
        throw new Error(errData.error || "Something went wrong.");
      }

      const data = await res.json();
      setResponse(data.response);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-3xl mx-auto p-6">
      <h1 className="text-3xl font-bold text-purple-700 mb-4">AI Business Mentor</h1>
      <p className="text-gray-700 mb-6">
        Describe your business idea in any language. Get feasibility, scheme suggestions, and a startup plan from our AI Mentor.
      </p>

      <form onSubmit={handleSubmit} className="space-y-4">
        <textarea
          className="w-full p-4 border rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-purple-500"
          rows={6}
          placeholder="Eg: मैं दिल्ली में महिलाओं के लिए बुटीक खोलना चाहती हूँ।"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          required
        />
        <button
          type="submit"
          disabled={loading}
          className="bg-purple-600 text-white px-6 py-2 rounded-md hover:bg-purple-700 disabled:opacity-50"
        >
          {loading ? "Processing..." : "Talk to AI Mentor"}
        </button>
      </form>

      {error && <p className="text-red-600 mt-4">{error}</p>}

      {response && (
      <div className="mt-6 bg-white text-black dark:bg-gray-900 dark:text-white p-4 rounded-md shadow-md whitespace-pre-wrap font-mono text-sm">
        {response}
      </div>
    )}
    </div>
  );
}
