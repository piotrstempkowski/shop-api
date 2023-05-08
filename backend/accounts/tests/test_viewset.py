import pytest
from django.contrib.auth import get_user_model
from rest_framework import status

User = get_user_model()


@pytest.mark.django_db
def test_get_users_list_as_admin(api_client, admin_token, url, users):
    api_client.credentials(HTTP_AUTHORIZATION=f"Token {admin_token}")
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == len(users)


@pytest.mark.django_db
def test_get_users_list_as_user(api_client, user, url):
    api_client.force_authenticate(user)
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1


@pytest.mark.django_db
def test_retrieve_user_as_admin(api_client, admin, admin_token, detail_url, user):
    api_client.credentials(HTTP_AUTHORIZATION=f"Token {admin_token}")
    response = api_client.get(detail_url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["username"] == user.username


@pytest.mark.django_db
def test_retrieve_user_as_user(api_client, user, detail_url):
    api_client.force_authenticate(user)
    response = api_client.get(detail_url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["email"] == user.email


@pytest.mark.django_db
def test_retrieve_user_get_404_not_found(api_client, detail_url, users):
    other_user = users[2]
    api_client.force_authenticate(other_user)
    response = api_client.get(detail_url)
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_create_user_as_admin(api_client, admin, admin_token, url, post_data):
    api_client.credentials(HTTP_AUTHORIZATION=f"Token {admin_token}")
    response = api_client.post(url, post_data)
    print(f" Content {response.content}")
    assert response.status_code == status.HTTP_201_CREATED
    assert User.objects.filter(username=post_data["username"]).exists()


@pytest.mark.django_db
def test_create_user_as_admin_validate_data(api_client, admin, admin_token, url, invalid_post_data):
    api_client.credentials(HTTP_AUTHORIZATION=f"Token {admin_token}")
    response = api_client.post(url, invalid_post_data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data["username"][0] == "A user with that username already exists."


@pytest.mark.django_db
def test_update_user_as_admin(api_client, admin, admin_token, detail_url, valid_put_data, user, valid_patch_data):
    api_client.credentials(HTTP_AUTHORIZATION=f"Token {admin_token}")
    response = api_client.put(detail_url, valid_put_data)

    assert response.status_code == status.HTTP_200_OK

    user.refresh_from_db()
    assert user.username == valid_put_data["username"]

    response = api_client.patch(detail_url, valid_patch_data)
    assert response.status_code == status.HTTP_200_OK
    user.refresh_from_db()
    assert user.username == user.username
    assert user.first_name == valid_patch_data["first_name"]
    assert user.last_name == valid_patch_data["last_name"]
    assert user.email == valid_patch_data["email"]


@pytest.mark.django_db
def test_update_user_as_user(api_client, user, detail_url, valid_put_data, valid_patch_data):
    api_client.force_authenticate(user)
    response = api_client.put(detail_url, valid_put_data)
    assert response.status_code == status.HTTP_200_OK
    user.refresh_from_db()
    assert user.username == valid_put_data["username"]

    response = api_client.patch(detail_url, valid_patch_data)
    assert response.status_code == status.HTTP_200_OK
    user.refresh_from_db()
    assert user.username == user.username
    assert user.first_name == valid_patch_data["first_name"]
    assert user.last_name == valid_patch_data["last_name"]
    assert user.email == valid_patch_data["email"]


@pytest.mark.django_db
def test_update_user_as_user_validate_data(api_client, user, detail_url, invalid_put_data, invalid_patch_data):
    api_client.force_authenticate(user)
    response = api_client.put(detail_url, invalid_put_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST

    assert response.data["password"][0] == "This field is required."

    response = api_client.patch(detail_url, invalid_patch_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data["email"][0] == "This field must be unique."


@pytest.mark.django_db
def test_update_user_get_404_not_found(api_client, detail_url, users, valid_put_data, valid_patch_data):
    other_user = users[2]
    api_client.force_authenticate(other_user)
    response = api_client.put(detail_url, valid_put_data)
    assert response.status_code == status.HTTP_404_NOT_FOUND

    response = api_client.patch(detail_url, valid_patch_data)
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_delete_user_as_admin(api_client, user, detail_url, admin_token):
    api_client.credentials(HTTP_AUTHORIZATION=f"Token {admin_token}")
    response = api_client.delete(detail_url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert User.objects.filter(username=user.username).exists() == False


@pytest.mark.django_db
def test_delete_user_as_user(api_client, user, detail_url):
    api_client.force_authenticate(user)
    response = api_client.delete(detail_url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert User.objects.filter(id=user.id).exists() == False


@pytest.mark.django_db
def test_delete_user_get_404_not_found(api_client, detail_url, users):
    other_user = users[2]
    api_client.force_authenticate(other_user)
    response = api_client.delete(detail_url)
    assert response.status_code == status.HTTP_404_NOT_FOUND
