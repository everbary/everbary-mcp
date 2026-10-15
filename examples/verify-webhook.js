// Verify an eVerbary webhook delivery (Node 18+, no dependencies).
// Header: X-Everbary-Signature: t=<unix>,v1=<hex>  (HMAC-SHA256 over "<t>.<raw body>")
const crypto = require("node:crypto");

function verifyEverbaryWebhook(rawBody, header, secret, toleranceSec = 300) {
  const parts = Object.fromEntries(String(header).split(",").map((p) => p.split("=", 2)));
  const t = Number(parts.t);
  if (!t || !parts.v1 || Math.abs(Date.now() / 1000 - t) > toleranceSec) return false;
  const expected = crypto.createHmac("sha256", secret).update(`${t}.`).update(rawBody).digest("hex");
  const a = Buffer.from(expected, "hex");
  const b = Buffer.from(parts.v1, "hex");
  return a.length === b.length && crypto.timingSafeEqual(a, b);
}

module.exports = { verifyEverbaryWebhook };
