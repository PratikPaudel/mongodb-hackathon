"use client";

import { useEffect, useRef } from "react";

/**
 * Custom hook to keep the backend alive by pinging the health check endpoint
 * every 14 minutes. This prevents free tier services (like Render) from going to sleep.
 *
 * @param backendUrl - The base URL of the backend (e.g., "http://localhost:8000" or "https://your-app.onrender.com")
 * @param enabled - Whether to enable the keep-alive pings (default: true)
 * @param intervalMinutes - How often to ping in minutes (default: 14)
 */
export function useKeepAlive(
  backendUrl: string,
  enabled: boolean = true,
  intervalMinutes: number = 14
) {
  const intervalRef = useRef<NodeJS.Timeout | null>(null);

  useEffect(() => {
    if (!enabled || !backendUrl) {
      return;
    }

    const pingHealthCheck = async () => {
      try {
        const response = await fetch(`${backendUrl}/api/health`, {
          method: "GET",
          cache: "no-store",
        });

        if (response.ok) {
          const data = await response.json();
          console.log(
            `[Keep-Alive] Health check successful at ${new Date().toLocaleTimeString()}:`,
            data
          );
        } else {
          console.warn(
            `[Keep-Alive] Health check returned status ${response.status}`
          );
        }
      } catch (error) {
        console.error("[Keep-Alive] Error pinging health check:", error);
      }
    };

    // Ping immediately on mount
    pingHealthCheck();

    // Set up interval to ping every N minutes
    const intervalMs = intervalMinutes * 60 * 1000;
    intervalRef.current = setInterval(pingHealthCheck, intervalMs);

    console.log(
      `[Keep-Alive] Started pinging ${backendUrl} every ${intervalMinutes} minutes`
    );

    // Cleanup on unmount
    return () => {
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
        console.log("[Keep-Alive] Stopped pinging");
      }
    };
  }, [backendUrl, enabled, intervalMinutes]);
}
