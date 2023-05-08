import datetime

import factory
from django.contrib.auth import get_user_model
from factory.fuzzy import FuzzyDateTime

BaseUser = get_user_model()


class BaseUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BaseUser

    first_name = factory.Faker("first_name", locale="pl_PL")
    last_name = factory.Faker("last_name", locale="pl_PL")
    username = factory.LazyAttribute(lambda o: f"{o.first_name.lower()}.{o.last_name.lower()}")
    email = factory.LazyAttribute(lambda o: f"{o.username}@example.com")
    date_joined = FuzzyDateTime(datetime.datetime(2008, 1, 1, tzinfo=datetime.UTC))
    last_login = date_joined
    password = factory.PostGenerationMethodCall("set_password", "password123")
