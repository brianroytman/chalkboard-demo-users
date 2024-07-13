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

    @patch('routers.user_routes.user_service.create_user', new_callable=AsyncMock)
    async def test_create_user(self, mock_create_user):
        mock_create_user.return_value = {'id': 1, 'username': 'John Doe', 'email': 'johnnydoe@gmail.com', 'first_name': 'John', 'last_name': 'Doe'}
        response = await self.client.post('/users', json={'username': 'John Doe', 'email': 'johnnydoe@gmail.com', 'first_name': 'John', 'last_name': 'Doe'})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {'id': 1, 'username': 'John Doe', 'email': 'johnnydoe@gmail.com', 'first_name': 'John', 'last_name': 'Doe'})
        mock_create_user.assert_called_once_with({'username': 'John Doe', 'email': 'johnnydoe@gmail.com', 'first_name': 'John', 'last_name': 'Doe'}, session=AsyncMock())

    @patch('routers.user_routes.user_service.create_user', new_callable=AsyncMock)
    async def test_create_user_duplicate(self, mock_create_user):
        mock_create_user.side_effect = Exception("User already exists")
        response = await self.client.post('/users', json={'username': 'John Doe', 'email': 'johnnydoe@gmail.com', 'first_name': 'John', 'last_name': 'Doe'})
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json(), {"detail": "User already exists"})

if __name__ == '__main__':
    unittest.main()
