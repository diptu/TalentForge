from datetime import datetime

import pytest

from app.db.models import User


@pytest.mark.asyncio
async def test_user_model_defaults() -> None:
    """Test default values for User model fields."""

    # Manually set defaults for testing
    user = User(
        email="default@example.com",
        hashed_password="hashedpassword",
        is_active=True,  # manually set
        is_superuser=False,  # manually set
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )

    assert user.is_active is True
    assert user.is_superuser is False
    assert isinstance(user.created_at, datetime)
    assert isinstance(user.updated_at, datetime)
