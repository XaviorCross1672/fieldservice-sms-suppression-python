import json

from field_sms import DispatchStatus, FollowUpRequest, WorkOrderPhoto, send_follow_up


request = FollowUpRequest(
    work_order_id="WO-1042",
    technician_phone="+15551234567",
    status=DispatchStatus(state="dispatched", technician="Mina"),
    photos=(WorkOrderPhoto(uri="https://example.com/wo-1042-before.jpg", caption="Panel"),),
)
result = send_follow_up(request, suppressed_numbers=set())
print(json.dumps(result, indent=2))
