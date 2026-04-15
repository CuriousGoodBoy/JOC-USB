from state.session import SessionState


def test_session_state_defaults():
    session = SessionState(run_id="test")
    assert session.run_id == "test"
    assert isinstance(session.issues, list)
