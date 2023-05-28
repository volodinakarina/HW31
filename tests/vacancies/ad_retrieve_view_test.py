import pytest

from ads.serializers.ad_serializer import AdSerializer


class TestAdRetrieveView:
    @pytest.mark.django_db
    def test_ad_retrieve_view(self, client, user_token, ad):
        response = client.get(
            f'/ads/{ad.id}/',
            HTTP_AUTHORIZATION=user_token['token']
        )

        code = 200
        assert response.status_code == code, f'Возвращается код {response.status_code} вместо {code}'
        assert response.data == AdSerializer(ad).data, f'Неверные данные объявления'

    @pytest.mark.django_db
    def test_ads_retrieve_view_errors(self, client, user_token, ad):
        # Обращение без токена
        response_1 = client.get(
            f'/ads/{ad.id}/',
            content_type='application/json',
        )

        code_1 = 401
        assert response_1.status_code == code_1, f'Возвращается код {response_1.status_code} вместо {code_1}'

        # Обращение на несуществующий id
        response_1 = client.get(
            f'/ads/1000000000/',
            content_type='application/json',
            HTTP_AUTHORIZATION=user_token['token']
        )

        code_1 = 404
        assert response_1.status_code == code_1, f'Возвращается код {response_1.status_code} вместо {code_1}'

