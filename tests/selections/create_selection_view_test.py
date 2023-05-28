import pytest

from tests.factories import AdFactory


class TestCreateSelectionView:
    @pytest.mark.django_db
    def test_create_selection_view(self, client, user_token):
        ads = AdFactory.create_batch(5)

        excepted_keys = {'name', 'owner', 'items', 'id'}

        data = {
            "name": "test_name",
            'items': [ad.id for ad in ads]
        }

        response = client.post(
            '/selections/',
            data,
            content_type='application/json',
            HTTP_AUTHORIZATION=user_token['token']
        )

        code = 200
        assert response.status_code == code, f'Возвращается код {response.status_code} вместо {code}'
        assert set(response.data.keys()) == excepted_keys, 'Ключи не совпадают'
        assert response.data['name'] == data['name'], f'Переданное значение "name" не совпадает'
        assert response.data['items'] == data['items'], f'Переданное значение "items" не совпадает'
        assert response.data['owner'] == user_token['user'].username, f'Переданное значение user через токен не совпадает'

    @pytest.mark.django_db
    def test_create_selection_view_error(self, client, user_token):
        ads = AdFactory.create_batch(5)

        # Обращение без токена
        data_1 = {
            "name": "test_name",
            'items': [ad.id for ad in ads]
        }

        response_1 = client.post(
            '/selections/',
            data_1,
            content_type='application/json',
        )

        code_1 = 401
        assert response_1.status_code == code_1, f'Возвращается код {response_1.status_code} вместо {code_1}'

        # Обращение без данных
        data_2 = {}

        response_2 = client.post(
            '/selections/',
            data_2,
            content_type='application/json',
        )

        code_2 = 401
        assert response_2.status_code == code_2, f'Возвращается код {response_2.status_code} вместо {code_2}'

        # Обращение с несуществующим объявлением
        data_3 = {
            "name": "test_name",
            'items': list(range(100))
        }

        response_3 = client.post(
            '/selections/',
            data_3,
            content_type='application/json',
        )

        code_3 = 401
        assert response_3.status_code == code_3, f'Возвращается код {response_3.status_code} вместо {code_3}'
