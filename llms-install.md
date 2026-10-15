# Installing the eVerbary MCP server

The server is hosted; there is nothing to build.

1. If the client supports remote MCP servers over Streamable HTTP with OAuth, add `https://orders.everbary.com/mcp`. The user signs in to their eVerbary account in the browser.
2. Otherwise, add a stdio server that runs `npx -y github:everbary/everbary-mcp`. On first use it opens the browser for the same sign-in.
3. Optional: if the user has an eVerbary API key (`ev_live_...`), set it as `EVERBARY_API_KEY` in the server's environment and no browser sign-in is needed. Test keys (`ev_test_...`) do not work on the MCP server.

Example for clients that use an `mcpServers` JSON block:

```json
{
  "mcpServers": {
    "everbary": {
      "command": "npx",
      "args": ["-y", "github:everbary/everbary-mcp"]
    }
  }
}
```

Check it works by asking for the languages eVerbary translates (`list_languages`).
