import pytest

from ads.serializers.ad_serializer import AdSerializer
from tests.factories import AdFactory


class TestAdsListView:
    @pytest.mark.django_db
    def test_ads_list_view(self, client, user_token):
        count = 8
        ads = AdFactory.create_batch(count)

        response_keys = {"count", "next", "previous", "results"}

        response = client.get(
            '/ads/',
        )

        code = 200
        assert response.status_code == code, f'Возвращается код {response.status_code} вместо {code}'
        assert set(response.data.keys()) == response_keys, 'Ключи не совпадают'
        assert response.data['count'] == count, 'Количество объявлений не совпадает'
        assert response.data['next'] is not None, \
            'Неверная ссылка на следующую страницу'
        assert response.data['previous'] is None, 'Неверная ссылка на предыдущую страницу'

        # Идут ли объявления в обратном порядке по цене
        ads.sort(key=lambda x: x.price, reverse=True)
        for ad_response, ad_factory in zip(response.data['results'], ads):
            assert ad_response == AdSerializer(ad_factory).data, f'Неверные данные объявления {ad_factory}'
