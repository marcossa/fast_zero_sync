from http import HTTPStatus

from fastapi.testclient import TestClient

from fast_zero.schemas import UserPublic


def test_root_deve_retornar_ok_e_ola_mundo(client: TestClient):
    # client = TestClient(app)  # Arrange

    # Act
    response = client.get('/')

    # Asserts
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Olá Mundo!'}


def test_create_user(client: TestClient):
    # client = TestClient(app)  # Arrange

    # Act
    response = client.post(
        '/users/',
        # UserSchema
        json={
            'username': 'marcos-new',
            'email': 'marcos@post.com.br',
            'password': 'password123',
        },
    )

    # Asserts
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'username': 'marcos-new',
        'email': 'marcos@post.com.br',
        'id': 1,
    }


def test_create_user_username_exists(client: TestClient, user: UserPublic):
    # client = TestClient(app)  # Arrange

    # Act
    response = client.post(
        '/users/',
        # UserSchema
        json={
            'username': 'marcos',
            'email': 'marcos@post.com.br',
            'password': 'password123',
        },
    )

    # Asserts
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.text == '{"detail":"Username already exists"}'


def test_create_user_email_exists(client: TestClient, user: UserPublic):
    # client = TestClient(app)  # Arrange

    # Act
    response = client.post(
        '/users/',
        # UserSchema
        json={
            'username': 'marcos-new',
            'email': 'marcos@aula.com.br',
            'password': 'password123',
        },
    )

    # Asserts
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.text == '{"detail":"Email already exists"}'


def test_read_users(client: TestClient):
    # client = TestClient(app)  # Arrange

    # Act
    response = client.get('/users')

    # Asserts
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        # UserList
        'users': []
    }


def test_read_users_with_user(client: TestClient, user: UserPublic):
    # client = TestClient(app)  # Arrange
    user_schema = UserPublic.model_validate(user).model_dump()

    # Act
    response = client.get('/users/')

    # Asserts
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [user_schema]}


def test_read_user(client: TestClient, user: UserPublic):
    # client = TestClient(app)  # Arrange
    user_schema = UserPublic.model_validate(user).model_dump()

    # Act
    response = client.get('/user/1')

    # Asserts
    assert response.status_code == HTTPStatus.OK
    assert response.json() == user_schema


def test_read_user_not_found(client: TestClient):
    # client = TestClient(app)  # Arrange

    # Act
    response = client.get('/user/0')

    # Assert
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_update_user(client: TestClient, user: UserPublic):
    # client = TestClient(app)  # Arrange

    # Act
    response = client.put(
        '/users/1',
        # UserDB
        json={
            'username': 'marcos-alterado',
            'email': 'marcos@put.com.br',
            'password': 'pwd321',
            'id': 1,
        },
    )

    # Asserts
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        # UserPublic
        'username': 'marcos-alterado',
        'email': 'marcos@put.com.br',
        'id': 1,
    }


def test_update_user_not_found(client: TestClient):
    # client = TestClient(app)  # Arrange

    # Act
    response = client.put(
        '/users/0',
        # UserSchema
        json={
            'username': 'marcos-fake',
            'email': 'marcos@fake.com.br',
            'password': 'null',
        },
    )

    # Assert
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_delete_user(client: TestClient, user: UserPublic):
    # client = TestClient(app)  # Arrange

    # Act
    response = client.delete('/users/1')

    # Asserts
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}


def test_delete_user_not_found(client: TestClient):
    # client = TestClient(app)  # Arrange

    # Act
    response = client.delete('/users/0')

    # Assert
    assert response.status_code == HTTPStatus.NOT_FOUND
