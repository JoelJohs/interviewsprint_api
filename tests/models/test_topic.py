import pytest
from pydantic import ValidationError
from app.models.topic import TopicBase, TopicCreate, TopicResponse


def test_topic_base_valid():
    """
    Test para ver si TopicBase funciona correctamente.
    """
    topic = TopicBase(
        title="Tipos de datos en JavaScript",
        category_id="js-react",
        details=["Primitivos: String, Number, Boolean",
                 "Objeto: null, Object, Array"]
    )
    assert topic.title == "Tipos de datos en JavaScript"
    assert topic.category_id == "js-react"
    assert len(topic.details) == 2


def test_topic_base_invalid_category_id():
    """
    Test para verificar category_id con formato inválido
    """
    with pytest.raises(ValidationError):
        TopicBase(
            title="Test Topic",
            category_id="JS React",  # Espacios no permitidos
            details=["Detail 1"]
        )


def test_topic_base_empty_details():
    """
    Test para verificar que details no puede estar vacío
    """
    with pytest.raises(ValidationError):
        TopicBase(
            title="Test Topic",
            category_id="js-react",
            details=[]
        )


def test_topic_base_details_with_empty_strings():
    """
    Test para verificar que details no puede tener solo strings vacíos
    """
    with pytest.raises(ValidationError):
        TopicBase(
            title="Test Topic",
            category_id="js-react",
            details=["   ", ""]
        )


def test_topic_create_valid():
    """
    Test para creación de TopicCreate válido
    """
    topic = TopicCreate(
        title="Closures en JavaScript",
        category_id="js-react",
        details=["Una función interna tiene acceso al scope de la función externa"]
    )
    assert topic.title == "Closures en JavaScript"
    assert topic.category_id == "js-react"
    assert len(topic.details) == 1


def test_topic_response_valid():
    """
    Test para TopicResponse con id
    """
    topic = TopicResponse(
        id="js-closures",
        title="Closures en JavaScript",
        category_id="js-react",
        details=["Detalle sobre closures"]
    )
    assert topic.id == "js-closures"
    assert topic.title == "Closures en JavaScript"


def test_topic_base_title_too_long():
    """
    Test para verificar que title no exceda max_length
    """
    with pytest.raises(ValidationError):
        TopicBase(
            title="a" * 101,  # Más de 100 caracteres
            category_id="js-react",
            details=["Detail"]
        )


def test_topic_base_category_id_valid_pattern():
    """
    Test para verificar que category_id acepta patrones válidos
    """
    topic = TopicBase(
        title="Test Topic",
        category_id="js-react-2024",
        details=["Detail"]
    )
    assert topic.category_id == "js-react-2024"
