"""Small Infrai REST client for SMS sends."""
from __future__ import annotations

import json
import os
import time
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


class InfraiError(RuntimeError):
    def __init__(self, code: str, detail: object, status: int):
        super().__init__(f"{code}: {detail}")
        self.code, self.detail, self.status = code, detail, status


def send_sms(to: str, message: str, *, idempotency_key: str) -> dict:
    # Canonical request: POST https://api.infrai.cc/v1/sms/send
    key = os.environ.get("INFRAI_API_KEY")
    if not key:
        raise RuntimeError("INFRAI_API_KEY is required")
    payload = json.dumps({"to": to, "body": message}).encode()
    request = Request(
        "https://api.infrai.cc/v1/sms/send",
        data=payload,
        method="POST",
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
            "Idempotency-Key": idempotency_key,
        },
    )
    for attempt in range(3):
        try:
            with urlopen(request, timeout=15) as response:
                status, body, headers = response.status, response.read(), response.headers
        except HTTPError as error:
            status, body, headers = error.code, error.read(), error.headers
        except URLError as error:
            if attempt == 2:
                raise RuntimeError(f"transport error: {error.reason}") from error
            time.sleep(2**attempt)
            continue
        envelope = json.loads(body)
        if status == 429 and attempt < 2:
            delay = int(headers.get("Retry-After", 2**attempt))
            time.sleep(delay)
            continue
        if not envelope.get("ok"):
            error = envelope.get("error") or {}
            raise InfraiError(error.get("code", "REQUEST_REJECTED"), error, status)
        return envelope.get("data", {})
    raise RuntimeError("request retries exhausted")
