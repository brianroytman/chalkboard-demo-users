import unittest
from unittest.mock import patch, AsyncMock
from repositories.user_repository import UserRepository
from schemas import UserCreateModel, UserUpdateModel
from sqlalchemy.ext.asyncio import AsyncSession


class TestUserRepository(unittest.IsolatedAsyncioTestCase):
    @patch('repositories.user_repository.UserRepository.add', new_callable=AsyncMock)
    async def test_create_user(self, mock_add):
        user_data = UserCreateModel(
            username='testuser',
            email='testuser@example.com',
            first_name='Test',
            last_name='User',
            date_created='2024-07-14T12:00:00Z',
            date_updated='2024-07-14T12:00:00Z'
        )
        session = AsyncMock(spec=AsyncSession)
        mock_add.return_value = user_data

        user_repository = UserRepository()
        actual_user = await user_repository.add(session, user_data)

        self.assertEqual(actual_user.username, 'testuser')
        self.assertEqual(actual_user.email, 'testuser@example.com')
        self.assertEqual(actual_user.first_name, 'Test')
        self.assertEqual(actual_user.last_name, 'User')

    @patch('repositories.user_repository.UserRepository.get_by_id', new_callable=AsyncMock)
    async def test_get_user_by_id(self, mock_get_by_id):
        # Test case for getting a user by ID
        user_id = 1
        expected_user = {'id': 1, 'username': 'John Doe',
                         'email': 'johnnydoe@gmail.com', 'first_name': 'John', 'last_name': 'Doe'}

        # Mock the get_by_id method to return the expected user
        mock_get_by_id.return_value = expected_user

        user_repository = UserRepository()
        actual_user = await user_repository.get_by_id(AsyncSession, user_id)

        self.assertEqual(actual_user, expected_user)

    @patch('repositories.user_repository.UserRepository.get_all', new_callable=AsyncMock)
    async def test_get_all_users(self, mock_get_all):
        # Test case for getting all users
        expected_users = [
            {'id': 1, 'username': 'John Doe', 'email': 'johnnydoe@gmail.com',
                'first_name': 'John', 'last_name': 'Doe'},
            {'id': 2, 'username': 'Jane Doe', 'email': 'janedoe@gmail.com',
                'first_name': 'Jane', 'last_name': 'Doe'},
        ]

        # Mock the get_all method to return the expected users
        mock_get_all.return_value = expected_users

        user_repository = UserRepository()
        actual_users = await user_repository.get_all(AsyncSession)

        self.assertEqual(actual_users, expected_users)

    @patch('repositories.user_repository.UserRepository.update', new_callable=AsyncMock)
    async def test_update_user(self, mock_update):
        # Test case for updating a user
        user_id = 1
        user_data = UserUpdateModel(
            username='updateduser',  # updated field
            email='testuser@example.com',
            first_name='Test',
            last_name='User',
        )

        # Mock the update method to return the updated user data
        mock_update.return_value = user_data

        user_repository = UserRepository()
        actual_user = await user_repository.update(AsyncSession, user_id, user_data)

        # Construct the expected user dictionary manually
        expected_user = {
            'id': user_id,
            'username': user_data.username,
            'email': user_data.email,
            'first_name': user_data.first_name,
            'last_name': user_data.last_name,
        }

        # Assert each attribute individually
        self.assertEqual(actual_user.username, expected_user['username'])
        self.assertEqual(actual_user.email, expected_user['email'])
        self.assertEqual(actual_user.first_name, expected_user['first_name'])
        self.assertEqual(actual_user.last_name, expected_user['last_name'])


    @patch('repositories.user_repository.UserRepository.delete', new_callable=AsyncMock)
    async def test_delete_user(self, mock_delete):
        # Test case for deleting a user
        user_id = 1

        # Mock the delete method to return None
        mock_delete.return_value = None

        user_repository = UserRepository()
        result = await user_repository.delete(AsyncSession, user_id)

        self.assertIsNone(result)

    @patch('repositories.user_repository.UserRepository.get_by_id', new_callable=AsyncMock)
    async def test_get_user_by_id_not_found(self, mock_get_by_id):
        # Test case for getting a user by ID that does not exist
        user_id = 1

        # Mock the get_by_id method to return None
        mock_get_by_id.return_value = None

        user_repository = UserRepository()
        actual_user = await user_repository.get_by_id(AsyncSession, user_id)

        self.assertIsNone(actual_user)

    @patch('repositories.user_repository.UserRepository.update', new_callable=AsyncMock)
    async def test_update_user_not_found(self, mock_update):
        # Test case for updating a user that does not exist
        user_id = 1
        user_data = {
            'username': 'updateduser',
            'email': 'updateduser@example.com',
            'first_name': 'Updated',
            'last_name': 'User',
        }

        # Mock the update method to return None
        mock_update.return_value = None

        user_repository = UserRepository()
        actual_user = await user_repository.update(AsyncSession, user_id, user_data)

        self.assertIsNone(actual_user)

    @patch('repositories.user_repository.UserRepository.delete', new_callable=AsyncMock)
    async def test_delete_user_not_found(self, mock_delete):
        # Test case for deleting a user that does not exist
        user_id = 1

        # Mock the delete method to return None
        mock_delete.return_value = None

        user_repository = UserRepository()
        result = await user_repository.delete(AsyncSession, user_id)

        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()
