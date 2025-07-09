"use client";

import { useState } from "react";

export default function AskForHelpPage() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<string[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    try {
      const res = await fetch("http://127.0.0.1:8000/matcher/api/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ query }),
      });

      if (!res.ok) {
        const errData = await res.json();
        throw new Error(errData.error || "Something went wrong");
      }

      const data = await res.json();
      setResults(data.results || []);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const parseNGO = (ngo: string) => {
    const [name, website, services, description, score] = ngo.split("\n");
    return { name, website, services, description, score };
  };

  return (
    <div className="max-w-3xl mx-auto p-6">
      <h1 className="text-4xl font-bold mb-6 text-center text-purple-700">Find Support NGOs</h1>

      <form onSubmit={handleSubmit} className="space-y-4 bg-white shadow-md rounded-lg p-6 border">
        <textarea
          placeholder="Describe your issue or requirement..."
          className="w-full p-4 border-2 border-gray-300 rounded-md h-36 resize-none focus:outline-none focus:ring-2 focus:ring-purple-500"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          required
        />
        <button
          type="submit"
          className="w-full px-6 py-3 bg-purple-600 text-white rounded-md hover:bg-purple-700 transition-colors"
          disabled={loading}
        >
          {loading ? "Matching NGOs..." : "Find NGOs"}
        </button>
      </form>

      {error && <p className="text-red-600 mt-4 text-center">{error}</p>}

      {!loading && results.length === 0 && query && !error && (
        <p className="text-gray-600 mt-6 text-center">No NGOs matched your query. Try rephrasing or adding more details.</p>
      )}

      {loading && (
        <div className="flex justify-center mt-6">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-purple-600"></div>
        </div>
      )}

      {results.length > 0 && (
        <div className="mt-8 space-y-6">
          <h2 className="text-2xl font-semibold text-gray-800 mb-4">Top Matches</h2>
          {results.map((ngo, idx) => {
            const { name, website, services, description, score } = parseNGO(ngo);
            return (
              <div
                key={idx}
                className="bg-white border border-gray-200 shadow-md rounded-lg p-5 transition-all hover:shadow-xl"
              >
                <h3 className="text-xl font-bold text-purple-700">{name}</h3>
                <p className="text-sm text-blue-600 mb-2">{website}</p>
                <p className="text-gray-800"><strong>Services:</strong> {services.replace("Services: ", "")}</p>
                <p className="text-gray-800 mt-1"><strong>Description:</strong> {description.replace("Description: ", "")}</p>
                <p className="text-sm text-gray-500 mt-2">{score}</p>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
