from pytest_factoryboy import register

from tests.factories import UserFactory, ModeratorFactory, CategoryFactory, AdFactory

pytest_plugins = "tests.user_fixtures"

register(UserFactory)
register(ModeratorFactory)
register(CategoryFactory)
register(AdFactory)
