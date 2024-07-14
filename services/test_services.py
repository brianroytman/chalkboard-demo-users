import unittest
from unittest.mock import patch, AsyncMock
from services.user_service import UserService
from schemas import UserCreateModel, UserModel, UserUpdateModel
from sqlalchemy.ext.asyncio import AsyncSession
import asyncio

class TestUserServices(unittest.IsolatedAsyncioTestCase):

    @patch('services.user_service.UserService.get_user')
    async def test_create_user(self, mock_get_user):
        mock_repository = AsyncMock()
        
        # Create a valid UserModel instance that matches the schema
        mock_user_instance = UserModel(
            id=1,
            username='testuser',
            email='testuser@example.com',
            first_name='Test',
            last_name='User',
            date_created='2024-07-14T12:00:00Z',  # Example date
            date_updated='2024-07-14T12:00:00Z',  # Example date
        )
        
        # Configure the create method of the mock repository to return the mock instance
        mock_repository.create.return_value = mock_user_instance

        mock_get_user.return_value = None
        user_service = UserService()
        user_service.user_repository = mock_repository

        user_data = UserCreateModel(
            username='testuser',
            email='testuser@example.com',
            first_name='Test',
            last_name='User',
        )
        session = AsyncSession()
        result = await user_service.create_user(user_data, session)

        # Assert that the returned result matches the expected UserModel attributes
        self.assertEqual(result.username, 'testuser')
        self.assertEqual(result.email, 'testuser@example.com')
        self.assertEqual(result.first_name, 'Test')
        self.assertEqual(result.last_name, 'User')

        # Additional assertions if needed for id, date_created, and date_updated
        self.assertEqual(result.id, 1)  # Adjust as per your actual schema and mock data
        self.assertIsNotNone(result.date_created)
        self.assertIsNotNone(result.date_updated)
    
    @patch('services.user_service.UserService.get_user')
    async def test_get_user(self, mock_get_user):
        mock_repository = AsyncMock()
        
        # Mock the repository to return a user when queried by ID
        mock_get_user.return_value = UserModel(
            id=1,
            username='testuser',
            email='testuser@example.com',
            first_name='Test',
            last_name='User',
            date_created='2024-07-14T12:00:00Z',  # Example date
            date_updated='2024-07-14T12:00:00Z',  # Example date
        )
        
        user_service = UserService()
        user_service.user_repository = mock_repository

        # Attempt to fetch the user
        result = await user_service.get_user(1)

        # Assert that the fetched user matches the expected attributes
        self.assertEqual(result.username, 'testuser')
        self.assertEqual(result.email, 'testuser@example.com')
        self.assertEqual(result.first_name, 'Test')
        self.assertEqual(result.last_name, 'User')

    @patch('services.user_service.UserService.get_user')
    async def test_get_user_nonexistent_user(self, mock_get_user):
        mock_repository = AsyncMock()
        
        # Mock the repository to return None when queried by ID, indicating user does not exist
        mock_get_user.return_value = None
        
        user_service = UserService()
        user_service.user_repository = mock_repository

        # Attempt to fetch the user
        result = await user_service.get_user(1)

        # Assert that result is None
        self.assertIsNone(result)

    # @patch('services.user_service.UserService.get_user')
    # async def test_update_user(self, mock_get_user):
    #     mock_repository = AsyncMock()
        
    #     # Mock the repository to return an existing user when queried by ID
    #     mock_get_user.return_value = UserModel(
    #         id=1,
    #         username='testuser',
    #         email='testuser@example.com',
    #         first_name='Test',
    #         last_name='User',
    #         date_created='2024-07-14T12:00:00Z',  # Example date
    #         date_updated='2024-07-14T12:00:00Z',  # Example date
    #     )
        
    #     user_service = UserService()
    #     user_service.user_repository = mock_repository

    #     updated_data = UserUpdateModel(
    #         username='testuser_updated',
    #         email='testuser_updated@example.com',
    #         first_name='Updated',
    #         last_name='User',
    #     )
    #     session = AsyncSession()

    #     # Attempt to update the user
    #     result = await user_service.update_user(1, updated_data, session)

    #     # Assert that the returned result matches the updated attributes
    #     self.assertEqual(result.username, 'testuser_updated')
    #     self.assertEqual(result.email, 'testuser_updated@example.com')
    #     self.assertEqual(result.first_name, 'Updated')
    #     self.assertEqual(result.last_name, 'User')

    @patch('services.user_service.UserService.get_user')
    async def test_delete_user(self, mock_get_user):
        mock_repository = AsyncMock()
        
        # Mock the repository to return an existing user when queried by ID
        mock_get_user.return_value = UserModel(
            id=1,
            username='testuser',
            email='testuser@example.com',
            first_name='Test',
            last_name='User',
            date_created='2024-07-14T12:00:00Z',  # Example date
            date_updated='2024-07-14T12:00:00Z',  # Example date
        )
        
        user_service = UserService()
        user_service.user_repository = mock_repository
        session = AsyncSession()

        # Attempt to delete the user
        result = await user_service.delete_user(1, session)

        # Assert that the delete method was called on the repository
        mock_repository.delete.assert_called_once_with(session, 1)



if __name__ == '__main__':
    unittest.main()
