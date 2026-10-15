# everbary (Python)

Python client for the [eVerbary](https://www.everbary.com) Order API: place certified translation orders (USCIS, courts, universities) from your own software, follow them, and get the finished translation back by webhook.

```bash
pip install "git+https://github.com/everbary/everbary-mcp#subdirectory=python"
```

```python
from everbary import Client

eb = Client("ev_test_...")   # a test key places pretend orders in the sandbox
order = eb.create_order(
    email="paralegal@firm.com", first_name="Ana", last_name="Ruiz",
    language_from="spanish", language_to="english", pages=1,
    files=["birth-certificate.pdf"], case_number="2026-114",
)
print(order["orderNumber"], order["status"])
print(eb.get_order(order["orderNumber"]))
```

Test keys (`ev_test_...`) behave like live ones but nothing is charged or translated: the order moves to `in-progress` after about a minute and `completed` two minutes later with a sample translation, and each step is sent to your webhook. `eb.sandbox_advance(n)` skips the wait.

Verify a webhook delivery:

```python
from everbary import verify_webhook
ok = verify_webhook(request.body, request.headers["X-Everbary-Signature"], secret)
```

- API reference: https://orders.everbary.com/v1/docs
- Getting a key: https://www.everbary.com/integrations/api
- Using eVerbary from Claude, ChatGPT or Cursor (MCP): https://github.com/everbary/everbary-mcp
- Support: support@everbary.com

MIT licensed.
