import pytest

from tests.factories import UserFactory, ModeratorFactory


@pytest.fixture
@pytest.mark.django_db
def user_token(db, client):
    user = UserFactory.create()

    data = {
        'username': user.username,
        'password': 'test_password',
    }

    response = client.post(
        '/users/token/',
        data,
        format='json',
    )

    token = response.data['access']
    data = {
        'user': user,
        'token': f'Bearer {token}'
    }

    return data


@pytest.fixture
@pytest.mark.django_db
def moderator_token(db, client):
    user = ModeratorFactory.create()

    data = {
        'username': user.username,
        'password': 'test_password',
    }

    response = client.post(
        '/users/token/',
        data,
        format='json',
    )

    token = response.data['access']

    return f'Bearer {token}'
