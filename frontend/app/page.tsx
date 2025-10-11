"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { useKeepAlive } from "@/lib/use-keep-alive";

// Hardcoded backend URLs - production | local
const BACKEND_URL =
  typeof window !== "undefined" && window.location.hostname !== "localhost"
    ? "https://mongodb-hackathon.onrender.com"
    : "http://localhost:8000";

export default function Home() {
  const [apiResponse, setApiResponse] = useState<string>("");
  const [data, setData] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);

  // Keep the backend alive by pinging every 14 minutes
  useKeepAlive(BACKEND_URL, true, 14);

  const testConnection = async () => {
    setLoading(true);
    try {
      const response = await fetch(`${BACKEND_URL}/api/health`);
      const json = await response.json();
      setApiResponse(JSON.stringify(json, null, 2));
    } catch (error) {
      setApiResponse(`Error: ${error}`);
    } finally {
      setLoading(false);
    }
  };

  const fetchData = async () => {
    setLoading(true);
    try {
      const response = await fetch(`${BACKEND_URL}/api/data`);
      const json = await response.json();
      setData(json.data);
    } catch (error) {
      setApiResponse(`Error: ${error}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen p-8 pb-20 sm:p-20">
      <main className="max-w-4xl mx-auto space-y-8">
        <div className="space-y-4">
          <h1 className="text-4xl font-bold">Next.js + FastAPI</h1>
          <p className="text-muted-foreground">
            Demo application with Tailwind CSS and shadcn/ui
          </p>
          <p className="text-xs text-muted-foreground">
            Backend: {BACKEND_URL}
          </p>
        </div>

        <div className="space-y-4">
          <h2 className="text-2xl font-semibold">API Connection Test</h2>
          <div className="flex gap-4">
            <Button onClick={testConnection} disabled={loading}>
              Test Backend Connection
            </Button>
            <Button onClick={fetchData} disabled={loading} variant="secondary">
              Fetch Sample Data
            </Button>
          </div>

          {apiResponse && (
            <div className="rounded-lg border bg-muted p-4">
              <h3 className="font-semibold mb-2">API Response:</h3>
              <pre className="text-sm overflow-auto">{apiResponse}</pre>
            </div>
          )}

          {data.length > 0 && (
            <div className="space-y-2">
              <h3 className="font-semibold">Data from Backend:</h3>
              <div className="grid gap-4 md:grid-cols-3">
                {data.map((item) => (
                  <div
                    key={item.id}
                    className="rounded-lg border p-4 hover:bg-accent transition-colors"
                  >
                    <h4 className="font-semibold">{item.name}</h4>
                    <p className="text-sm text-muted-foreground">
                      {item.description}
                    </p>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>

        <div className="rounded-lg border p-6 bg-card">
          <h2 className="text-xl font-semibold mb-4">Setup Instructions</h2>
          <ol className="list-decimal list-inside space-y-2 text-sm">
            <li>
              Start the backend:{" "}
              <code className="bg-muted px-2 py-1 rounded">
                cd backend && source venv/bin/activate && uvicorn main:app --reload
              </code>
            </li>
            <li>
              Start the frontend:{" "}
              <code className="bg-muted px-2 py-1 rounded">
                cd frontend && npm run dev
              </code>
            </li>
            <li>Click the buttons above to test the API connection</li>
          </ol>
        </div>
      </main>
    </div>
  );
}
