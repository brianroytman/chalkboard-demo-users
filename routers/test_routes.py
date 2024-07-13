import unittest
from unittest.mock import patch, AsyncMock
from fastapi.testclient import TestClient
from routers.user_routes import router
from fastapi import FastAPI

app = FastAPI()
app.include_router(router)


class TestUserRoutes(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    # Happy path tests
    @patch('routers.user_routes.user_service.create_user', new_callable=AsyncMock)
    async def test_create_user(self, mock_create_user):
        mock_create_user.return_value = {'id': 1, 'username': 'John Doe',
                                         'email': 'johnnydoe@gmail.com', 'first_name': 'John', 'last_name': 'Doe'}
        response = await self.client.post('/users', json={'username': 'John Doe', 'email': 'johnnydoe@gmail.com', 'first_name': 'John', 'last_name': 'Doe'})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {'id': 1, 'username': 'John Doe',
                         'email': 'johnnydoe@gmail.com', 'first_name': 'John', 'last_name': 'Doe'})
        mock_create_user.assert_called_once_with(
            {'username': 'John Doe', 'email': 'johnnydoe@gmail.com', 'first_name': 'John', 'last_name': 'Doe'}, session=AsyncMock())

    @patch('routers.user_routes.user_service.get_user', new_callable=AsyncMock)
    async def test_get_user(self, mock_get_user):
        mock_get_user.return_value = {'id': 1, 'username': 'John Doe',
                                      'email': 'johnnydoe@gmail.com', 'first_name': 'John', 'last_name': 'Doe'}
        response = await self.client.get('/users/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'id': 1, 'username': 'John Doe',
                         'email': 'johnnydoe@gmail.com', 'first_name': 'John', 'last_name': 'Doe'})
        mock_get_user.assert_called_once_with(1, session=AsyncMock())

    @patch('routers.user_routes.user_service.update_user', new_callable=AsyncMock)
    async def test_update_user(self, mock_update_user):
        mock_update_user.return_value = {'id': 1, 'username': 'John Doe',
                                         'email': 'johnnydoe@gmail.com', 'first_name': 'John', 'last_name': 'Doe'}
        response = await self.client.put('/users/1', json={'username': 'John Doe', 'email': 'johnnydoe@gmail.com', 'first_name': 'John', 'last_name': 'Doe'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'id': 1, 'username': 'John Doe',
                         'email': 'johnnydoe@gmail.com', 'first_name': 'John', 'last_name': 'Doe'})
        mock_update_user.assert_called_once_with(
            1, {'username': 'John Doe', 'email': 'johnnydoe@gmail.com', 'first_name': 'John', 'last_name': 'Doe'}, session=AsyncMock())

    @patch('routers.user_routes.user_service.delete_user', new_callable=AsyncMock)
    async def test_delete_user(self, mock_delete_user):
        mock_delete_user.return_value = None
        response = await self.client.delete('/users/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'User deleted'})
        mock_delete_user.assert_called_once_with(1, session=AsyncMock())

    @patch('routers.user_routes.user_service.get_users', new_callable=AsyncMock)
    async def test_get_users(self, mock_get_users):
        mock_get_users.return_value = [
            {'id': 1, 'username': 'John Doe', 'email': 'johnnydoe@gmail.com',
                'first_name': 'John', 'last_name': 'Doe'},
            {'id': 2, 'username': 'Jane Doe', 'email': 'janedoe@gmail.com',
                'first_name': 'Jane', 'last_name': 'Doe'}
        ]
        response = await self.client.get('/users')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [
            {'id': 1, 'username': 'John Doe', 'email': 'johnnydoe@gmail.com',
                'first_name': 'John', 'last_name': 'Doe'},
            {'id': 2, 'username': 'Jane Doe', 'email': 'janedoe@gmail.com',
                'first_name': 'Jane', 'last_name': 'Doe'}
        ])
        mock_get_users.assert_called_once_with(session=AsyncMock())

    # Non-happy path tests
    @patch('routers.user_routes.user_service.create_user', new_callable=AsyncMock)
    async def test_create_user_duplicate(self, mock_create_user):
        mock_create_user.side_effect = Exception("User already exists")
        response = await self.client.post('/users', json={'username': 'John Doe', 'email': 'johnnydoe@gmail.com', 'first_name': 'John', 'last_name': 'Doe'})
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json(), {"detail": "User already exists"})

    @patch('routers.user_routes.user_service.get_user', new_callable=AsyncMock)
    async def test_get_user_not_found(self, mock_get_user):
        mock_get_user.side_effect = Exception("User not found")
        response = await self.client.get('/users/999')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json(), {"detail": "User not found"})

    @patch('routers.user_routes.user_service.create_user', new_callable=AsyncMock)
    async def test_create_user_duplicate(self, mock_create_user):
        mock_create_user.side_effect = Exception("User already exists")
        response = await self.client.post('/users', json={'username': 'John Doe', 'email': 'johnnydoe@gmail.com', 'first_name': 'John', 'last_name': 'Doe'})
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json(), {"detail": "User already exists"})

    @patch('routers.user_routes.user_service.update_user', new_callable=AsyncMock)
    async def test_update_user_not_found(self, mock_update_user):
        mock_update_user.side_effect = Exception("User not found")
        response = await self.client.put('/users/999', json={'username': 'John Doe', 'email': 'johnnydoe@gmail.com', 'first_name': 'John', 'last_name': 'Doe'})
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json(), {"detail": "User not found"})

    @patch('routers.user_routes.user_service.delete_user', new_callable=AsyncMock)
    async def test_delete_user_not_found(self, mock_delete_user):
        mock_delete_user.side_effect = Exception("User not found")
        response = await self.client.delete('/users/999')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json(), {"detail": "User not found"})


if __name__ == '__main__':
    unittest.main()
