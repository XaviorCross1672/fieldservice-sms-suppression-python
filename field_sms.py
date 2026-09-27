from __future__ import annotations

from dataclasses import dataclass, field

from infrai_sms import send_sms


@dataclass(frozen=True)
class WorkOrderPhoto:
    uri: str
    caption: str = ""


@dataclass(frozen=True)
class DispatchStatus:
    state: str
    technician: str


@dataclass(frozen=True)
class FollowUpRequest:
    work_order_id: str
    technician_phone: str
    status: DispatchStatus
    photos: tuple[WorkOrderPhoto, ...] = field(default_factory=tuple)
    opted_out: bool = False


def send_follow_up(request: FollowUpRequest, suppressed_numbers: set[str]) -> dict:
    """Send only when the technician is reachable and the order is dispatched."""
    if request.opted_out or request.technician_phone in suppressed_numbers:
        return {"sent": False, "reason": "suppressed"}
    if request.status.state != "dispatched":
        return {"sent": False, "reason": "not_dispatched"}
    text = f"Work order {request.work_order_id} is dispatched. Reply with an update when complete."
    result = send_sms(
        request.technician_phone,
        text,
        idempotency_key=f"work-order:{request.work_order_id}:follow-up",
    )
    return {"sent": True, "message": result}
