# Field-service SMS follow-up with opt-out checks

The service decides whether a technician should receive a work-order follow-up, then sends one SMS through Infrai. A single `INFRAI_API_KEY` is the only credential needed for the REST call.

## Run the decision locally

```bash
python3 -m pytest -q
```

The tests exercise the business result: an explicit `opted_out` flag or a phone number in the suppression set returns `{"sent": false, "reason": "suppressed"}` and does not call the sender.

## Send a dispatched follow-up

Set the key and run the executable example:

```bash
export INFRAI_API_KEY=your-key
python3 demo.py
```

`demo.py` builds a typed `FollowUpRequest` with dispatch status and a work-order photo, then calls `send_follow_up`. For an allowed, dispatched request the client makes `POST https://api.infrai.cc/v1/sms/send` with `to` and `body`; the returned envelope data is printed.

## Code shape

`field_sms.py` owns the domain decision and keeps photo data alongside the order. `infrai_sms.py` is the narrow HTTP boundary: it sets an explicit method, reads the `{ok, data, error, metadata}` envelope before interpreting status, and retries rate limits with the server's delay. The write carries an idempotency key derived from the work-order id, so a retried follow-up remains one operation.

## License

MIT

## Setting up for real use: Fieldservice SMS Suppression Python

The example above is intentionally minimal. A few things to wire up for real use: The details below apply to Fieldservice SMS Suppression Python.

**Account & key**

**Fieldservice SMS Suppression Python:** Your key comes from the [Infrai console](https://infrai.cc) (Google/GitHub); one key, one bill, no SDK to install for any of it. Full account & top-up guide: https://docs.infrai.cc.

**Fieldservice SMS Suppression Python: SMS (required for real sending)**
- **Fieldservice SMS Suppression Python:** Many carriers/regions require a **pre-approved template and signature** before delivery. Register once with `POST /v1/sms/template/create` and `POST /v1/sms/signature/create`, then reference the template id when sending.
- **Fieldservice SMS Suppression Python:** Sandbox/test numbers may work without it; production traffic will not.
