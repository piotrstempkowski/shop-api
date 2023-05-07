import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from accounts.factories import BaseUserFactory

@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def admin():
    admin = BaseUserFactory.create()
    admin.is_staff = True
    admin.save()
    return admin

@pytest.fixture
def post_data():
    new_user = BaseUserFactory.build()
    data = {
        "username": new_user.username,
        "email": "AdamJęcioł@email.com",
        "first_name": new_user.first_name,
        "last_name": new_user.last_name,
        "password": "testpassword123"
    }
    return data

@pytest.fixture
def invalid_post_data(user):
    data = {
        "username": user.username,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "password": user.password
    }
    return data

@pytest.fixture
def valid_put_data(user):
    new_user = BaseUserFactory.build()
    data = {
        "username": user.username,
        "email": "AdamJęcioł@example.com",
        "first_name": new_user.first_name,
        "last_name": new_user.last_name,
        "password": new_user.password,
    }
    return data

@pytest.fixture
def invalid_put_data(user):
    data = {
        "username": user.username,
        "email":user.email,
        "first_name": user.first_name,

    }
    return data

@pytest.fixture
def valid_patch_data():
    new_user = BaseUserFactory.build()
    data = {
        "first_name": new_user.first_name,
        "last_name": new_user.last_name,
        "email": new_user.email
    }
    return data

@pytest.fixture
def invalid_patch_data(users):
    other_user_data =users[3]
    data = {
        "first_name": other_user_data.first_name,
        "last_name": other_user_data.last_name,
        "email": other_user_data.email
    }
    return data

@pytest.fixture
def users():
    return BaseUserFactory.create_batch(10)

@pytest.fixture
def user(users):
    return users[0]

@pytest.fixture
def admin_token(admin):
    return Token.objects.create(user=admin)

@pytest.fixture
def url():
    return reverse("user-list")

@pytest.fixture
def detail_url(user):
    return reverse("user-detail", kwargs={"pk": user.id})