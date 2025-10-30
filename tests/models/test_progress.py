import pytest
from datetime import datetime
from pydantic import ValidationError
from app.models.progress import ProgressBase, ProgressCreate, ProgressUpdate, ProgressResponse


def test_progress_base_valid():
    """
    Test para ver si ProgressBase funciona correctamente.
    """
    progress = ProgressBase(
        user_id="user123",
        topic_id="js-closures",
        status="in-progress",
        notes="Estudiando closures"
    )
    assert progress.user_id == "user123"
    assert progress.topic_id == "js-closures"
    assert progress.status == "in-progress"
    assert progress.notes == "Estudiando closures"


def test_progress_base_default_notes():
    """
    Test para verificar que notes tiene valor default vacío
    """
    progress = ProgressBase(
        user_id="user123",
        topic_id="js-closures",
        status="not-started"
    )
    assert progress.notes == ""


def test_progress_create_valid():
    """
    Test para creación de ProgressCreate válido
    """
    progress = ProgressCreate(
        user_id="user456",
        topic_id="py-decoradores",
        status="completed",
        notes="Completado exitosamente"
    )
    assert progress.user_id == "user456"
    assert progress.status == "completed"


def test_progress_update_partial():
    """
    Test para actualización parcial de progreso
    """
    progress = ProgressUpdate(
        status="completed"
    )
    assert progress.status == "completed"
    assert progress.notes is None


def test_progress_update_only_notes():
    """
    Test para actualizar solo las notas
    """
    progress = ProgressUpdate(
        notes="Añadiendo más información"
    )
    assert progress.status is None
    assert progress.notes == "Añadiendo más información"


def test_progress_update_all_fields():
    """
    Test para actualizar todos los campos
    """
    progress = ProgressUpdate(
        status="in-progress",
        notes="Continuando con el estudio"
    )
    assert progress.status == "in-progress"
    assert progress.notes == "Continuando con el estudio"


def test_progress_response_valid():
    """
    Test para ProgressResponse con todos los campos
    """
    now = datetime.now()
    progress = ProgressResponse(
        id="progress123",
        user_id="user789",
        topic_id="sql-joins",
        status="completed",
        notes="Entendido perfectamente",
        created_at=now,
        updated_at=now
    )
    assert progress.id == "progress123"
    assert progress.user_id == "user789"
    assert progress.created_at == now
    assert progress.updated_at == now


def test_progress_base_missing_required_fields():
    """
    Test para verificar que faltan campos requeridos
    """
    with pytest.raises(ValidationError):
        ProgressBase(
            user_id="user123"
            # Faltan topic_id y status
        )


def test_progress_base_status_too_long():
    """
    Test para verificar que status no exceda max_length
    """
    with pytest.raises(ValidationError):
        ProgressBase(
            user_id="user123",
            topic_id="topic123",
            status="a" * 51  # Más de 50 caracteres
        )


def test_progress_base_notes_too_long():
    """
    Test para verificar que notes no exceda max_length
    """
    with pytest.raises(ValidationError):
        ProgressBase(
            user_id="user123",
            topic_id="topic123",
            status="completed",
            notes="a" * 501  # Más de 500 caracteres
        )
