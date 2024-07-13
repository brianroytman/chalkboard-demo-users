import unittest
from unittest.mock import patch
from services.user_service import UserService
from schemas import UserCreateModel
from sqlalchemy.ext.asyncio import AsyncSession


class TestUserServices(unittest.TestCase):

    @patch('services.user_service.UserService.get_user')
    async def test_create_user(self, mock_get_user):
        # Mock the get_user function
        mock_get_user.return_value = None

        # Create a new user
        user_service = UserService()
        user_data = UserCreateModel(
            username='testuser',
            email='testuser@example.com',
            first_name='Test',
            last_name='User',
        )
        result = await user_service.create_user(user_data, session=AsyncSession)

        # Assert that the user was created successfully
        self.assertEqual(result.username, 'testuser')
        self.assertEqual(result.email, 'testuser@example.com')
        self.assertEqual(result.first_name, 'Test')
        self.assertEqual(result.last_name, 'User')

    @patch('services.user_service.UserService.get_user')
    async def test_create_user_existing_user(self, mock_get_user):
        # Mock the get_user function to return an existing user
        mock_get_user.return_value = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'first_name': 'Test',
            'last_name': 'User',
        }

        # Try to create a user with the same username
        user_service = UserService()
        user_data = UserCreateModel(
            username='testuser',
            email='testuser@example.com',
            first_name='Test',
            last_name='User',
        )
        result = await user_service.create_user(user_data, session=AsyncSession)

        # Assert that the user creation failed
        self.assertIsNone(result)

    @patch('services.user_service.UserService.get_user')
    async def test_get_user(self, mock_get_user):
        # Mock the get_user function to return a user
        mock_get_user.return_value = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'first_name': 'Test',
            'last_name': 'User',
        }

        # Get a user by username
        user_service = UserService()
        result = await user_service.get_user('testuser', session=AsyncSession)

        # Assert that the correct user was returned
        self.assertEqual(result['username'], 'testuser')
        self.assertEqual(result['email'], 'testuser@example.com')
        self.assertEqual(result['first_name'], 'Test')
        self.assertEqual(result['last_name'], 'User')

    @patch('services.user_service.UserService.get_user')
    async def test_get_user_nonexistent_user(self, mock_get_user):
        # Mock the get_user function to return None
        mock_get_user.return_value = None

        # Try to get a nonexistent user
        user_service = UserService()
        result = await user_service.get_user('nonexistentuser', session=AsyncSession)

        # Assert that the user does not exist
        self.assertIsNone(result)

    @patch('services.user_service.UserService.get_user')
    async def test_update_user(self, mock_get_user):
        # Mock the get_user function to return a user
        mock_get_user.return_value = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'first_name': 'Test',
            'last_name': 'User',
        }

        # Update a user's email
        user_service = UserService()
        result = await user_service.update_user('testuser', email='newemail@example.com', session=AsyncSession)

        # Assert that the user's email was updated successfully
        self.assertEqual(result['email'], 'newemail@example.com')

    @patch('services.user_service.UserService.get_user')
    async def test_update_user_nonexistent_user(self, mock_get_user):
        # Mock the get_user function to return None
        mock_get_user.return_value = None

        # Try to update a nonexistent user
        user_service = UserService()
        result = await user_service.update_user('nonexistentuser', email='newemail@example.com', session=AsyncSession)

        # Assert that the user does not exist
        self.assertIsNone(result)

    @patch('services.user_service.UserService.get_user')
    async def test_delete_user(self, mock_get_user):
        # Mock the get_user function to return a user
        mock_get_user.return_value = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'first_name': 'Test',
            'last_name': 'User',
        }

        # Delete a user
        user_service = UserService()
        result = await user_service.delete_user('testuser', session=AsyncSession)

        # Assert that the user was deleted successfully
        self.assertTrue(result)

    @patch('services.user_service.UserService.get_user')
    async def test_delete_user_nonexistent_user(self, mock_get_user):
        # Mock the get_user function to return None
        mock_get_user.return_value = None

        # Try to delete a nonexistent user
        user_service = UserService()
        result = await user_service.delete_user('nonexistentuser', session=AsyncSession)

        # Assert that the user does not exist
        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()
