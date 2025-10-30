import pytest
from pydantic import ValidationError
from app.models.user import UserBase, UserCreate, UserResponse


def test_user_base_model():
    """
    Test para ver si UserBase funciona correctamente.
    """
    user = UserBase(
        username="testuser",
        email="testuser@example.com",
        is_active=True
    )
    assert user.username == "testuser"
    assert user.email == "testuser@example.com"
    assert user.is_active is True


def test_user_base_invalid_email():
    """
    Test para verificar email inválido
    """

    with pytest.raises(ValidationError):
        UserBase(
            username="testuser",
            email="invalid-email",
            is_active=True
        )


def test_user_create_valid():
    """
    Test para creación de usuario válida
    """

    user = UserCreate(
        username="testuser",
        email="test@example.com",
        password="securepass123"
    )
    assert user.password == "securepass123"
    assert len(user.password) >= 8


def test_user_create_short_password():
    """
    Test para verificar si la contraseña es demasiado corta
    """

    with pytest.raises(ValidationError):
        UserCreate(
            username="testuser",
            email="test@example.com",
            password="short"
        )
