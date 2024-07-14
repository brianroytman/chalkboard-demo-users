import unittest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from datetime import datetime, timezone
from main import app
from schemas import UserCreateModel, UserModel, UserUpdateModel
from services.user_service import UserService


class TestUserRoutes(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.client = TestClient(app)

    @patch.object(UserService, 'create_user', return_value=UserModel(
        id=1,
        username="testuser",
        email="testuser@example.com",
        first_name="Test",
        last_name="User",
        date_created=datetime.now(timezone.utc),
        date_updated=datetime.now(timezone.utc)
    ))
    async def test_create_user(self, mock_create_user):
        response = self.client.post("/users", json={
            "username": "testuser",
            "email": "testuser@example.com",
            "first_name": "Test",
            "last_name": "User"
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["username"], "testuser")
        mock_create_user.assert_called_once()

    @patch.object(UserService, 'create_user', side_effect=Exception("Duplicate entry"))
    async def test_create_user_duplicate(self, mock_create_user):
        response = self.client.post("/users", json={
            "username": "testuser",
            "email": "testuser@example.com",
            "first_name": "Test",
            "last_name": "User"
        })
        self.assertEqual(response.status_code, 500)
        self.assertIn("Duplicate entry", response.json()["detail"])
        mock_create_user.assert_called_once()

    @patch.object(UserService, 'get_user', return_value=UserModel(
        id=1,
        username="testuser",
        email="testuser@example.com",
        first_name="Test",
        last_name="User",
        date_created=datetime.now(timezone.utc),
        date_updated=datetime.now(timezone.utc)
    ))
    async def test_get_user(self, mock_get_user):
        response = self.client.get("/users/1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["username"], "testuser")
        mock_get_user.assert_called_once_with(1, unittest.mock.ANY)

    @patch.object(UserService, 'get_user', return_value=None)
    async def test_get_user_not_found(self, mock_get_user):
        response = self.client.get("/users/999")
        self.assertEqual(response.status_code, 500)
        error_detail = response.json()["detail"]
        self.assertEqual(error_detail, "404: User not found")
        mock_get_user.assert_called_once_with(999, unittest.mock.ANY)

    @patch.object(UserService, 'get_users', return_value=[
        UserModel(
            id=1,
            username="testuser",
            email="testuser@example.com",
            first_name="Test",
            last_name="User",
            date_created=datetime.now(timezone.utc),
            date_updated=datetime.now(timezone.utc)
        )
    ])
    async def test_get_users(self, mock_get_users):
        response = self.client.get("/users")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]["username"], "testuser")
        mock_get_users.assert_called_once()

    @patch.object(UserService, 'update_user', return_value=UserModel(
        id=1,
        username="updateduser",
        email="updateduser@example.com",
        first_name="Updated",
        last_name="User",
        date_created=datetime.now(timezone.utc),
        date_updated=datetime.now(timezone.utc)
    ))
    async def test_update_user(self, mock_update_user):
        response = self.client.put("/users/1", json={
            "username": "updateduser",
            "email": "updateduser@example.com",
            "first_name": "Updated",
            "last_name": "User"
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["username"], "updateduser")
        mock_update_user.assert_called_once_with(1, UserUpdateModel(
            username="updateduser",
            email="updateduser@example.com",
            first_name="Updated",
            last_name="User"
       ), unittest.mock.ANY)

    @patch.object(UserService, 'update_user', side_effect=Exception("User not found"))
    async def test_update_user_not_found(self, mock_update_user):
        response = self.client.put("/users/999", json={
            "username": "updateduser",
            "email": "updateduser@example.com",
            "first_name": "Updated",
            "last_name": "User"
        })
        self.assertEqual(response.status_code, 500)
        self.assertIn("User not found", response.json()["detail"])
        mock_update_user.assert_called_once_with(999, UserUpdateModel(
            username="updateduser",
            email="updateduser@example.com",
            first_name="Updated",
            last_name="User"
        ), unittest.mock.ANY)

    @patch.object(UserService, 'delete_user', return_value=None)
    async def test_delete_user(self, mock_delete_user):
        response = self.client.delete("/users/1")
        self.assertEqual(response.status_code, 204)
        mock_delete_user.assert_called_once_with(1, unittest.mock.ANY)

    # @patch.object(UserService, 'delete_user', side_effect=Exception("User not found"))
    # async def test_delete_user_not_found(self, mock_delete_user):
    #     response = self.client.delete("/users/999")
    #     self.assertEqual(response.status_code, 500)
    #     error_detail = response.json()["detail"]
    #     self.assertEqual(error_detail, "404: User not found")
    #     mock_delete_user.assert_called_once_with(999, unittest.mock.ANY)



if __name__ == "__main__":
    unittest.main(verbosity=2)
