# eVerbary MCP server

Order certified translations of official documents (birth and marriage certificates, diplomas, transcripts, court records) from Claude, ChatGPT, Cursor or any MCP client. Translations are done by human translators in the US and come with a signed certificate of accuracy accepted by USCIS, courts and universities.

[eVerbary](https://www.everbary.com) works with 1,250+ law firms and translators in the US. This repository holds:

- the connection details for the hosted MCP server, `https://orders.everbary.com/mcp`
- `everbary-mcp`, a small npm package that bridges the hosted server to clients that only speak stdio
- `everbary`, a Python client for the REST API ([`python/`](python/))
- a Postman collection for the REST API ([`postman/`](postman/))

## What the assistant can do

| Tool | What it does |
|---|---|
| `list_languages` | Languages and per-page prices |
| `list_document_types` | Common document types and what each needs |
| `get_quote` | Price and delivery time for this account (team discounts included) |
| `upload_document` | Send a source document (PDF, image, Word) |
| `create_order` | Place the order with the uploaded files |
| `pay_order` | Pay with the account's prepaid balance or saved card, within spending limits |
| `order_status` | Progress, expected delivery and payment state |
| `list_my_orders` | Recent orders |
| `get_payment_link` | A link anyone can use to pay an unpaid order |

Every tool carries MCP annotations (`readOnlyHint` / `destructiveHint`), so clients can ask before anything that places or pays an order. By default an order is capped at $500 and an account at $1,000 a day.

## Connect

### Claude (claude.ai, Desktop)

Settings → Connectors → Add custom connector → URL `https://orders.everbary.com/mcp`. Sign in with your eVerbary account when asked.

### Claude Code

```bash
claude mcp add --transport http everbary https://orders.everbary.com/mcp
```

### ChatGPT

Use the eVerbary app from the ChatGPT apps directory, or add `https://orders.everbary.com/mcp` as a connector in developer mode.

### Cursor, VS Code, Windsurf and other stdio clients

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

The first run opens your browser to sign in to eVerbary. To skip the sign-in, put an API key in the environment:

```json
{
  "mcpServers": {
    "everbary": {
      "command": "npx",
      "args": ["-y", "everbary-mcp"],
      "env": { "EVERBARY_API_KEY": "ev_live_..." }
    }
  }
}
```

The bridge is a thin wrapper around [mcp-remote](https://github.com/geelen/mcp-remote): nothing runs locally except the connection.

## REST API

If you are building your own integration (case management software, intake forms, a firm's internal tools), use the REST API directly:

- Reference: https://orders.everbary.com/v1/docs
- Overview and keys: https://www.everbary.com/integrations/api
- Python: `pip install everbary` ([`python/`](python/))
- Postman: import [`postman/everbary.postman_collection.json`](postman/everbary.postman_collection.json) and set `apiKey`

Test keys (`ev_test_...`) work on every REST endpoint against a sandbox: orders are pretend, nothing is charged or sent to a translator, and each order moves `new` → `in-progress` → `completed` on its own with a sample translation, firing your webhook at every step. Ask support@everbary.com for a test key.

Case management software can also open a hosted checkout with the documents already attached (`POST /v1/checkout/sessions`). Try the demo: https://orders.everbary.com/checkout/demo

## Pricing

From $24.95 per page. Rush options and notarization are extra. Current prices: https://www.everbary.com/pricing

## Links

- MCP setup guide: https://www.everbary.com/integrations/ai-assistants
- Official MCP Registry: `com.everbary.www/orders`
- Security: https://www.everbary.com/security
- Privacy: https://www.everbary.com/privacy
- Support: support@everbary.com

## License

MIT
