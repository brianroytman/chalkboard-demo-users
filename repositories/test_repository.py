import unittest
import pytest
from unittest.mock import patch, AsyncMock
from repositories.user_repository import UserRepository
from schemas import UserCreateModel, UserUpdateModel
from sqlalchemy.ext.asyncio import AsyncSession

@pytest.mark.asyncio
class TestUserRepository(unittest.TestCase):
    @patch('repositories.user_repository.UserRepository.add', new_callable=AsyncMock)
    async def test_create_user(self, mock_add):
        # Test case for creating a user
        user_data = UserCreateModel(
            username='testuser',
            email='testuser@example.com',
            first_name='Test',
            last_name='User',
        )
        session = AsyncMock(spec=AsyncSession)
        
        # Mock the add method to return the user data
        mock_add.return_value = user_data
        
        user_repository = UserRepository()
        actual_user = await user_repository.add(session, user_data)
        
        self.assertEqual(actual_user.username, 'testuser')
        self.assertEqual(actual_user.email, 'testuser@example.com')
        self.assertEqual(actual_user.first_name, 'Test')
        self.assertEqual(actual_user.last_name, 'User')

if __name__ == '__main__':
    unittest.main()