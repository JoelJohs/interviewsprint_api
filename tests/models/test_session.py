import pytest
from datetime import datetime
from pydantic import ValidationError
from app.models.session import SessionRequest, SessionItem, SessionResponse


def test_session_request_valid():
    """
    Test para ver si SessionRequest funciona correctamente.
    """
    session_req = SessionRequest(
        user_id="user123",
        topic_ids=["js-closures", "py-decoradores", "sql-joins"]
    )
    assert session_req.user_id == "user123"
    assert len(session_req.topic_ids) == 3
    assert "js-closures" in session_req.topic_ids


def test_session_request_empty_topic_ids():
    """
    Test para verificar SessionRequest con topic_ids vacío
    """
    session_req = SessionRequest(
        user_id="user123",
        topic_ids=[]
    )
    assert len(session_req.topic_ids) == 0


def test_session_request_missing_user_id():
    """
    Test para verificar que user_id es requerido
    """
    with pytest.raises(ValidationError):
        SessionRequest(
            topic_ids=["js-closures"]
            # Falta user_id
        )


def test_session_item_valid():
    """
    Test para SessionItem válido
    """
    item = SessionItem(
        topic_id="js-closures",
        title="Closures en JavaScript",
        category_id="js-react",
        details=["Una función interna tiene acceso al scope externo"]
    )
    assert item.topic_id == "js-closures"
    assert item.title == "Closures en JavaScript"
    assert item.category_id == "js-react"
    assert len(item.details) == 1


def test_session_item_empty_details():
    """
    Test para SessionItem con details vacío (permitido con default_factory)
    """
    item = SessionItem(
        topic_id="js-closures",
        title="Closures",
        category_id="js-react"
    )
    assert item.details == []


def test_session_response_valid():
    """
    Test para SessionResponse completo
    """
    now = datetime.now()
    item1 = SessionItem(
        topic_id="js-closures",
        title="Closures",
        category_id="js-react",
        details=["Detalle 1"]
    )
    item2 = SessionItem(
        topic_id="py-decoradores",
        title="Decoradores",
        category_id="python",
        details=["Detalle 2"]
    )

    session = SessionResponse(
        session_id="session123",
        user_id="user456",
        created_at=now,
        topics=[item1, item2]
    )
    assert session.session_id == "session123"
    assert session.user_id == "user456"
    assert session.created_at == now
    assert len(session.topics) == 2


def test_session_response_empty_topics():
    """
    Test para SessionResponse con lista de topics vacía
    """
    now = datetime.now()
    session = SessionResponse(
        session_id="session456",
        user_id="user789",
        created_at=now
    )
    assert session.topics == []


def test_session_response_missing_required_fields():
    """
    Test para verificar que faltan campos requeridos
    """
    with pytest.raises(ValidationError):
        SessionResponse(
            session_id="session123"
            # Faltan user_id y created_at
        )


def test_session_item_title_too_long():
    """
    Test para verificar que title no exceda max_length
    """
    with pytest.raises(ValidationError):
        SessionItem(
            topic_id="topic123",
            title="a" * 201,  # Más de 200 caracteres
            category_id="category"
        )


def test_session_request_user_id_too_long():
    """
    Test para verificar que user_id no exceda max_length
    """
    with pytest.raises(ValidationError):
        SessionRequest(
            user_id="a" * 101,  # Más de 100 caracteres
            topic_ids=["topic1"]
        )
