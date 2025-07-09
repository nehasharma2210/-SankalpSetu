import { NextRequest } from "next/server";

export async function POST(req: NextRequest) {
  const data = await req.json();
  const res = await fetch("http://127.0.0.1:8000/api/login/", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      username: data.phone || data.email || data.username,
      password: data.password,
    }),
  });
  const result = await res.json();
  return new Response(JSON.stringify(result), { status: res.status });
}
