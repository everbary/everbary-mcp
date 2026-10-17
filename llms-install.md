# Installing the eVerbary MCP server

The server is hosted; there is nothing to build.

1. If the client supports remote MCP servers over Streamable HTTP with OAuth, add `https://orders.everbary.com/mcp`. The user signs in to their eVerbary account in the browser.
2. Otherwise, add a stdio server that runs `npx -y everbary-mcp`. On first use it opens the browser for the same sign-in.
3. Optional: if the user has an eVerbary API key (`ev_live_...`), set it as `EVERBARY_API_KEY` in the server's environment and no browser sign-in is needed. A test key (`ev_test_...`) runs the same tools against a sandbox: pretend orders, nothing charged.

Example for clients that use an `mcpServers` JSON block:

```json
{
  "mcpServers": {
    "everbary": {
      "command": "npx",
      "args": ["-y", "everbary-mcp"]
    }
  }
}
```

Check it works by asking for the languages eVerbary translates (`list_languages`).
