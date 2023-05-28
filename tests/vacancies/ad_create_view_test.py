import pytest


class TestCreateAdView:
    @pytest.mark.django_db
    def test_create_ad_view_test(self, client, user_token, category):
        data = {
            "category_id": category.id,
            "name": "test_name1",
            "price": 2000,
            "description": "Продаю сибирских котят",
        }
        expected_keys = {"id", "image", "author", "category", "name", "price", "description", "is_published"}

        response = client.post(
            '/ads/',
            data,
            content_type='application/json',
            HTTP_AUTHORIZATION=user_token['token']
        )
        code = 201
        assert response.status_code == code, f'Возвращается код {response.status_code} вместо {code}'
        assert set(response.data.keys()) == expected_keys, 'Ключи не совпадают'
        assert response.data["author"] == user_token['user'].username, f'Переданные данные "user" через токен не совпадают'
        assert response.data["category"] == category.name, f'Переданные данные "category" не совпадают'
        assert response.data["name"] == data["name"], f'Переданные данные "name" не совпадают'
        assert response.data["price"] == data["price"], f'Переданные данные "price" не совпадают'
        assert response.data["description"] == data["description"], f'Переданные данные "description" не совпадают'

    @pytest.mark.django_db
    def test_create_ad_view_error_test(self, client, user_token, category):
        # Обращение без токена:
        data_1 = {
            "category_id": category.id,
            "name": "test_name1",
            "price": 2000,
            "description": "Продаю сибирских котят",
        }
        response_1 = client.post(
            '/ads/',
            data_1,
            content_type='application/json',
        )
        code_1 = 401
        assert response_1.status_code == code_1, f'Возвращается код {response_1.status_code} вместо {code_1}'

        # Обращение без данных
        response_2 = client.post(
            '/ads/',
            content_type='application/json',
            HTTP_AUTHORIZATION=user_token['token']
        )
        code_2 = 400
        assert response_2.status_code == code_2, f'Возвращается код {response_2.status_code} вместо {code_2}'

        # Обращение с отрицательной ценой:
        data_3 = {
            "category_id": category.id,
            "name": "test_name1",
            "price": -2000,
            "description": "Продаю сибирских котят",
        }
        response_3 = client.post(
            '/ads/',
            data_3,
            content_type='application/json',
            HTTP_AUTHORIZATION=user_token['token']
        )
        code_3 = 400
        assert response_3.status_code == code_3, f'Возвращается код {response_3.status_code} вместо {code_3}'

        # Обращение с коротким именем:
        data_4 = {
            "category_id": category.id,
            "name": "test_name",
            "price": 2000,
            "description": "Продаю сибирских котят",
        }
        response_4 = client.post(
            '/ads/',
            data_4,
            content_type='application/json',
            HTTP_AUTHORIZATION=user_token['token']
        )
        code_4 = 400
        assert response_4.status_code == code_3, f'Возвращается код {response_4.status_code} вместо {code_4}'
