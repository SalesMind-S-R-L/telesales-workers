import { Hono } from "hono";
import { cors } from "hono/cors";
import type { Env } from "./types";
import type { ScheduledEvent } from "@cloudflare/workers-types";
import { healthHandler } from "./handlers/health";
import { batchesHandler, processHandler } from "./handlers/batches";
import { statsHandler } from "./handlers/stats";
import { cronHandler, getCronExecutor } from "./handlers/cron";

const app = new Hono<{ Bindings: Env }>();

// Middleware
app.use("*", cors());

// Health check
app.get("/health", healthHandler);

// Batches
app.get("/batches", batchesHandler);
app.post("/process/:batch_id", processHandler);

// Stats
app.get("/stats", statsHandler);

// Recruiting: serve i dati della Talent Tower da KV (sola lettura, per il frontend Tower)
app.get("/recruiting/candidates", async (c) => {
  const data = await c.env.KV.get("recruiting_candidates");
  return c.body(data || "[]", 200, {
    "content-type": "application/json; charset=utf-8",
    "cache-control": "no-store",
  });
});

// Cron (internal)
app.post("/internal/check", cronHandler);

// Fallback
app.all("*", (c) => {
  return c.json({ error: "Not Found" }, 404);
});

// Export for Cloudflare Workers
export default {
  fetch: app.fetch,
  async scheduled(event: ScheduledEvent, env: Env) {
    try {
      const executor = getCronExecutor(env);
      const result = await executor();
      console.log("Cron executed:", result);
    } catch (error) {
      console.error("Cron error:", error);
    }
  },
};

// Export types
export type { Env };
