import hashlib
import hmac
import os
import time
import uuid
from typing import Any, Dict, Iterable, Optional, Union

import requests

DEFAULT_BASE_URL = "https://orders.everbary.com"
FileArg = Union[str, "os.PathLike[str]", tuple]


class EverbaryError(Exception):
    """An API call answered with an error status."""

    def __init__(self, status: int, detail: Any):
        super().__init__(f"{status}: {detail}")
        self.status = status
        self.detail = detail


class Client:
    """A thin wrapper over https://orders.everbary.com/v1.

    Keys that start with ``ev_test_`` use the sandbox: orders are pretend, move
    on their own (new -> in-progress -> completed) and fire your webhook, so you
    can build the whole flow before going live.
    """

    def __init__(self, api_key: Optional[str] = None, base_url: str = DEFAULT_BASE_URL, timeout: float = 60):
        self.api_key = api_key or os.environ.get("EVERBARY_API_KEY", "")
        if not self.api_key:
            raise ValueError("Pass an API key or set EVERBARY_API_KEY.")
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.api_key}",
            "User-Agent": "everbary-python/1.0.0",
        })

    @property
    def is_test(self) -> bool:
        return self.api_key.startswith("ev_test_")

    def _request(self, method: str, path: str, **kw) -> Any:
        r = self.session.request(method, self.base_url + path, timeout=self.timeout, **kw)
        try:
            body = r.json()
        except ValueError:
            body = r.text
        if r.status_code >= 400:
            detail = body.get("detail", body) if isinstance(body, dict) else body
            raise EverbaryError(r.status_code, detail)
        return body

    # Account and catalog
    def me(self) -> Dict[str, Any]:
        return self._request("GET", "/v1/me")

    def languages(self) -> list:
        return self._request("GET", "/v1/languages")["languages"]

    def turnaround(self, pages: int = 1) -> Dict[str, Any]:
        return self._request("GET", "/v1/turnaround", params={"pages": pages})

    def expedited_plus(self, language_from: str, language_to: str = "english") -> Dict[str, Any]:
        return self._request("GET", "/v1/expedited-plus",
                             params={"language_from": language_from, "language_to": language_to})

    # Orders
    def create_order(self, *, email: str, first_name: str, last_name: str, language_from: str,
                     pages: int, files: Iterable[FileArg], language_to: str = "english",
                     reference: Optional[str] = None, note: Optional[str] = None,
                     case_number: Optional[str] = None, client_first_name: Optional[str] = None,
                     client_last_name: Optional[str] = None, expedited: bool = False,
                     expedited_plus: bool = False, notarization: bool = False,
                     source: Optional[str] = None, idempotency_key: Optional[str] = None) -> Dict[str, Any]:
        """Place an order. ``files`` are paths or ``(filename, bytes_or_fileobj)`` tuples.

        A retried call with the same ``idempotency_key`` returns the first order
        instead of placing a second one; one is generated if you do not pass it.
        """
        data = {
            "email": email, "first_name": first_name, "last_name": last_name,
            "language_from": language_from, "language_to": language_to, "pages": str(pages),
            "expedited": str(expedited).lower(), "expedited_plus": str(expedited_plus).lower(),
            "notarization": str(notarization).lower(),
        }
        for k, v in (("reference", reference), ("note", note), ("case_number", case_number),
                     ("client_first_name", client_first_name), ("client_last_name", client_last_name),
                     ("source", source)):
            if v:
                data[k] = v
        opened, parts = [], []
        try:
            for f in files:
                if isinstance(f, tuple):
                    parts.append(("files", f))
                else:
                    fh = open(f, "rb")
                    opened.append(fh)
                    parts.append(("files", (os.path.basename(str(f)), fh)))
            headers = {"Idempotency-Key": idempotency_key or str(uuid.uuid4())}
            return self._request("POST", "/v1/orders", data=data, files=parts, headers=headers)
        finally:
            for fh in opened:
                fh.close()

    def get_order(self, order_number: Union[int, str]) -> Dict[str, Any]:
        return self._request("GET", f"/v1/orders/{order_number}")

    def list_orders(self, limit: int = 20, status: Optional[str] = None) -> Dict[str, Any]:
        params: Dict[str, Any] = {"limit": limit}
        if status:
            params["status"] = status
        return self._request("GET", "/v1/orders", params=params)

    # Webhooks
    def set_webhook(self, url: str) -> Dict[str, Any]:
        """Register the https endpoint for status changes. The signing secret is returned once."""
        return self._request("PUT", "/v1/webhook", data={"url": url})

    def get_webhook(self) -> Dict[str, Any]:
        return self._request("GET", "/v1/webhook")

    # Embedded checkout
    def create_checkout_session(self, **session: Any) -> Dict[str, Any]:
        """Open a hosted checkout page with the documents attached (see docs/checkout)."""
        return self._request("POST", "/v1/checkout/sessions", json=session)

    def get_checkout_session(self, session_id: str) -> Dict[str, Any]:
        return self._request("GET", f"/v1/checkout/sessions/{session_id}")

    # Sandbox only
    def sandbox_advance(self, order_number: Union[int, str], to: str = "") -> Dict[str, Any]:
        """Move a test order to its next status now (or to ``in-progress``, ``completed``, ``cancelled``)."""
        return self._request("POST", f"/v1/sandbox/orders/{order_number}/advance", data={"to": to})


def verify_webhook(raw_body: bytes, signature_header: str, secret: str, tolerance: int = 300) -> bool:
    """Check ``X-Everbary-Signature: t=<unix>,v1=<hex>`` (HMAC-SHA256 over ``"<t>.<raw body>"``)."""
    try:
        parts = dict(p.split("=", 1) for p in signature_header.split(","))
        ts, sig = int(parts["t"]), parts["v1"]
    except (KeyError, ValueError):
        return False
    if abs(time.time() - ts) > tolerance:
        return False
    expected = hmac.new(secret.encode(), f"{ts}.".encode() + raw_body, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, sig)
