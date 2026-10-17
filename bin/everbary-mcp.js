#!/usr/bin/env node
// Local stdio bridge to the eVerbary MCP server (https://orders.everbary.com/mcp).
//
// With EVERBARY_API_KEY set, every request carries it as a Bearer token: a live
// key (ev_live_) works on the account, a test key (ev_test_) on the sandbox.
// Without it, the first run opens the browser to sign in to eVerbary (OAuth),
// and the token is cached by mcp-remote under ~/.mcp-auth.
"use strict";

const { spawn } = require("node:child_process");
const path = require("node:path");

const url = process.env.EVERBARY_MCP_URL || "https://orders.everbary.com/mcp";
const key = (process.env.EVERBARY_API_KEY || "").trim();

const proxy = path.join(path.dirname(require.resolve("mcp-remote/package.json")), "dist", "proxy.js");
const args = [proxy, url, ...process.argv.slice(2)];
if (key) args.push("--header", `Authorization:Bearer ${key}`);

const child = spawn(process.execPath, args, { stdio: "inherit" });
child.on("exit", (code, signal) => {
  if (signal) process.kill(process.pid, signal);
  else process.exit(code ?? 0);
});
for (const sig of ["SIGINT", "SIGTERM"]) process.on(sig, () => child.kill(sig));
