#!/usr/bin/env bash
# Place a sandbox order with a test key, then move it along without waiting.
set -euo pipefail
: "${EVERBARY_API_KEY:?set EVERBARY_API_KEY to an ev_test_ key}"
API=https://orders.everbary.com

curl -s "$API/v1/orders" \
  -H "Authorization: Bearer $EVERBARY_API_KEY" \
  -H "Idempotency-Key: $(uuidgen)" \
  -F email=paralegal@example.com -F first_name=Ana -F last_name=Ruiz \
  -F language_from=spanish -F language_to=english -F pages=1 \
  -F case_number=2026-114 \
  -F files=@birth-certificate.pdf

# then: curl -s -X POST "$API/v1/sandbox/orders/<orderNumber>/advance" -H "Authorization: Bearer $EVERBARY_API_KEY"
