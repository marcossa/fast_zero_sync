from http import HTTPStatus


def test_root_deve_retornar_ok_e_ola_mundo(client):
    # client = TestClient(app)  # Arrange

    # Act
    response = client.get('/')

    # Asserts
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Olá Mundo!'}


def test_create_user(client):
    # client = TestClient(app)  # Arrange

    # Act
    response = client.post(
        '/users/',
        # UserSchema
        json={
            'username': 'marcos',
            'email': 'marcos@aula.com.br',
            'password': 'password123',
        },
    )

    # Assert: Validar UserPublic
    assert response.status_code == HTTPStatus.CREATED

    # Assert: Validar UserPublic
    assert response.json() == {
        'username': 'marcos',
        'email': 'marcos@aula.com.br',
        'id': 1,
    }


def test_read_users(client):
    # client = TestClient(app)  # Arrange

    # Act
    response = client.get('/users')

    # Asserts
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        # UserList
        'users': [
            {
                'username': 'marcos',
                'email': 'marcos@aula.com.br',
                'id': 1,
            }
        ]
    }


def test_read_user(client):
    # client = TestClient(app)  # Arrange

    # Act
    response = client.get('/user/1')

    # Asserts
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        # UserPublic
        'username': 'marcos_found',
        'email': 'marcos@found.com.br',
        'id': 1,
    }


def test_read_user_not_found(client):
    # client = TestClient(app)  # Arrange

    # Act
    response = client.get('/users/0')

    # Assert
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_update_user(client):
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


def test_update_user_not_found(client):
    # client = TestClient(app)  # Arrange

    # Act
    response = client.put(
        '/users/0',
        # UserDB
        json={
            'username': 'marcos-not_found',
            'email': 'marcos@notfound.com.br',
            'password': 'pwd000',
            'id': 0,
        },
    )

    # Assert
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_delete_user(client):
    # client = TestClient(app)  # Arrange

    # Act
    response = client.delete('/users/1')

    # Assert
    assert response.json() == {'message': 'User deleted'}


def test_delete_user_not_found(client):
    # client = TestClient(app)  # Arrange

    # Act
    response = client.delete('/users/0')

    # Assert
    assert response.status_code == HTTPStatus.NOT_FOUND
