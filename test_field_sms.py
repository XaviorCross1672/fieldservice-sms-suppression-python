from field_sms import DispatchStatus, FollowUpRequest, send_follow_up


def test_opt_out_blocks_send(monkeypatch):
    def fail(*args, **kwargs):
        raise AssertionError("send_sms must not run for an opt-out")

    monkeypatch.setattr("field_sms.send_sms", fail)
    request = FollowUpRequest("WO-1", "+15550001", DispatchStatus("dispatched", "T"), opted_out=True)
    assert send_follow_up(request, set()) == {"sent": False, "reason": "suppressed"}


def test_suppression_list_blocks_send(monkeypatch):
    monkeypatch.setattr("field_sms.send_sms", lambda *args, **kwargs: {"message_id": "m-1"})
    request = FollowUpRequest("WO-2", "+15550002", DispatchStatus("dispatched", "T"))
    assert send_follow_up(request, {"+15550002"})["sent"] is False
