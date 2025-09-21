"""
Comprehensive test suite for the Session-Based Authenticated MCP Server.

This module contains all tests for:
- Session-based authentication system
- Books database operations
- Currency exchange functionality
- Error handling and edge cases
- Integration testing

Author: MCP Server Team
Date: September 2025
"""

import asyncio
import pytest
import sys
import os
import time
from typing import Dict, Any, List
from unittest.mock import Mock, patch

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from mcp_server.server import (
    create_jwt_token,
    validate_jwt_token,
    handle_call_tool,
    _USER_SESSIONS,
    _CURRENT_SESSION
)
from mcp_server.books import BooksRepository
from mcp_server.exchange import ExchangeRates, default_rates


class TestJWTTokens:
    """Test JWT token creation and validation functionality."""
    
    def test_create_jwt_token(self):
        """Test JWT token creation with valid parameters."""
        user_id = "test_user_123"
        username = "testuser"
        
        token = create_jwt_token(user_id, username)
        
        # Token should have 3 parts separated by dots
        parts = token.split('.')
        assert len(parts) == 3, "JWT token should have 3 parts"
        
        # Each part should be base64 encoded
        for part in parts:
            assert len(part) > 0, "JWT token parts should not be empty"
    
    def test_validate_valid_jwt_token(self):
        """Test validation of a valid JWT token."""
        user_id = "test_user_456"
        username = "validuser"
        
        token = create_jwt_token(user_id, username)
        payload = validate_jwt_token(token)
        
        assert payload is not None, "Valid token should return payload"
        assert payload["user_id"] == user_id, "Payload should contain correct user_id"
        assert payload["username"] == username, "Payload should contain correct username"
        assert "exp" in payload, "Payload should contain expiration time"
        assert "iat" in payload, "Payload should contain issued at time"
    
    def test_validate_invalid_jwt_token(self):
        """Test validation of invalid JWT tokens."""
        invalid_tokens = [
            "invalid.token.here",
            "not-a-token",
            "too.few.parts",
            "too.many.parts.here.extra",
            "",
            None
        ]
        
        for invalid_token in invalid_tokens:
            if invalid_token is not None:
                payload = validate_jwt_token(invalid_token)
                assert payload is None, f"Invalid token '{invalid_token}' should return None"
    
    def test_expired_jwt_token(self):
        """Test validation of expired JWT tokens."""
        # Create a token that's already expired by mocking time
        with patch('time.time', return_value=1000000):
            token = create_jwt_token("user123", "expireduser")
        
        # Now validate it with current time (should be expired)
        payload = validate_jwt_token(token)
        assert payload is None, "Expired token should return None"


class TestSessionAuthentication:
    """Test session management and authentication functionality."""
    
    def setup_method(self):
        """Clear session state before each test."""
        import mcp_server.server
        _USER_SESSIONS.clear()
        mcp_server.server._CURRENT_SESSION = None
    
    def setup_method(self):
        """Clean up sessions before each test."""
        global _USER_SESSIONS, _CURRENT_SESSION
        _USER_SESSIONS.clear()
        _CURRENT_SESSION = None
    
    @pytest.mark.asyncio
    async def test_authenticate_user(self):
        """Test user authentication and session creation."""
        result = await handle_call_tool("authenticate", {"username": "testuser"})
        response = eval(result[0].text)
        
        assert response["success"] is True, "Authentication should succeed"
        assert response["username"] == "testuser", "Response should contain username"
        assert "user_id" in response, "Response should contain user_id"
        assert "session_id" in response, "Response should contain session_id"
        assert response["expires_in"] == 3600, "Session should expire in 1 hour"
        
        # Check that session was created
        assert len(_USER_SESSIONS) == 1, "Should have one active session"
        # Import module to get current value of _CURRENT_SESSION
        import mcp_server.server
        assert mcp_server.server._CURRENT_SESSION is not None, "Should have current session set"
    
    @pytest.mark.asyncio
    async def test_session_status_unauthenticated(self):
        """Test session status when not authenticated."""
        result = await handle_call_tool("session_status", {})
        response = eval(result[0].text)
        
        assert response["authenticated"] is False, "Should not be authenticated"
        assert "message" in response, "Should contain message about no session"
    
    @pytest.mark.asyncio
    async def test_session_status_authenticated(self):
        """Test session status when authenticated."""
        # First authenticate
        await handle_call_tool("authenticate", {"username": "statususer"})
        
        # Then check status
        result = await handle_call_tool("session_status", {})
        response = eval(result[0].text)
        
        assert response["authenticated"] is True, "Should be authenticated"
        assert response["username"] == "statususer", "Should show correct username"
        assert "session_age" in response, "Should show session age"
        assert "expires_in" in response, "Should show time until expiration"
    
    @pytest.mark.asyncio
    async def test_logout(self):
        """Test user logout and session cleanup."""
        # First authenticate
        await handle_call_tool("authenticate", {"username": "logoutuser"})
        
        # Verify session exists
        assert len(_USER_SESSIONS) == 1, "Should have one session before logout"
        
        # Logout
        result = await handle_call_tool("logout", {})
        response = eval(result[0].text)
        
        assert response["success"] is True, "Logout should succeed"
        assert "Successfully logged out" in response["message"], "Should confirm logout"
        
        # Verify session was cleaned up
        assert len(_USER_SESSIONS) == 0, "Should have no sessions after logout"
        assert _CURRENT_SESSION is None, "Current session should be None"
    
    @pytest.mark.asyncio
    async def test_logout_without_session(self):
        """Test logout when no session exists."""
        result = await handle_call_tool("logout", {})
        response = eval(result[0].text)
        
        assert response["success"] is True, "Logout should still succeed"
        assert "No active session" in response["message"], "Should indicate no session"


class TestProtectedOperations:
    """Test operations that require authentication."""
    
    def setup_method(self):
        """Clean up sessions before each test."""
        import mcp_server.server
        _USER_SESSIONS.clear()
        mcp_server.server._CURRENT_SESSION = None
    
    @pytest.mark.asyncio
    async def test_books_query_without_auth(self):
        """Test books query without authentication should fail."""
        result = await handle_call_tool("books_query", {"title": "python"})
        response = eval(result[0].text)
        
        assert "error" in response, "Should return error"
        assert response["error"] == "authentication_required", "Should require authentication"
        assert "No active session" in response["message"], "Should explain no session"
    
    @pytest.mark.asyncio
    async def test_exchange_convert_without_auth(self):
        """Test currency conversion without authentication should fail."""
        result = await handle_call_tool("exchange_convert", {
            "from_currency": "USD",
            "to_currency": "EUR", 
            "amount": 100
        })
        response = eval(result[0].text)
        
        assert "error" in response, "Should return error"
        assert response["error"] == "authentication_required", "Should require authentication"
    
    @pytest.mark.asyncio
    async def test_books_query_with_auth(self):
        """Test books query with valid authentication."""
        # First authenticate
        await handle_call_tool("authenticate", {"username": "bookuser"})
        
        # Then query books
        result = await handle_call_tool("books_query", {"limit": 5})
        response = eval(result[0].text)
        
        assert "authenticated_user" in response, "Should show authenticated user"
        assert response["authenticated_user"] == "bookuser", "Should show correct user"
        assert "data" in response, "Should contain book data"
        assert "count" in response, "Should contain result count"
        assert isinstance(response["data"], list), "Data should be a list"
    
    @pytest.mark.asyncio
    async def test_exchange_convert_with_auth(self):
        """Test currency conversion with valid authentication."""
        # First authenticate
        await handle_call_tool("authenticate", {"username": "currencyuser"})
        
        # Then convert currency
        result = await handle_call_tool("exchange_convert", {
            "from_currency": "USD",
            "to_currency": "EUR",
            "amount": 100
        })
        response = eval(result[0].text)
        
        assert "authenticated_user" in response, "Should show authenticated user"
        assert response["authenticated_user"] == "currencyuser", "Should show correct user"
        assert response["from"] == "USD", "Should show source currency"
        assert response["to"] == "EUR", "Should show target currency"
        assert response["amount"] == 100.0, "Should show original amount"
        assert "converted" in response, "Should show converted amount"
        assert isinstance(response["converted"], (int, float)), "Converted amount should be numeric"


class TestSessionExpiration:
    """Test session expiration functionality."""
    
    def setup_method(self):
        """Clean up sessions before each test."""
        global _USER_SESSIONS, _CURRENT_SESSION
        _USER_SESSIONS.clear()
        _CURRENT_SESSION = None
    
    @pytest.mark.asyncio
    async def test_expired_session(self):
        """Test that expired sessions are handled correctly."""
        # Authenticate with mocked old timestamp
        with patch('time.time', return_value=1000000):
            await handle_call_tool("authenticate", {"username": "expireduser"})
        
        # Try to use expired session (current time much later)
        result = await handle_call_tool("books_query", {"limit": 1})
        response = eval(result[0].text)
        
        assert "error" in response, "Should return error for expired session"
        assert response["error"] == "session_expired", "Should indicate session expired"
        assert len(_USER_SESSIONS) == 0, "Expired session should be cleaned up"
        assert _CURRENT_SESSION is None, "Current session should be None"


class TestBooksRepository:
    """Test the books database functionality."""
    
    def setup_method(self):
        """Set up test data for books repository."""
        # Create a mock CSV file content
        self.test_csv_content = """Title,Authors,Category,Publisher,Price Starting With ($),Publish Date (Year)
Clean Code,Robert Martin,Programming,Prentice Hall,45.99,2008
The Great Gatsby,F. Scott Fitzgerald,Fiction,Scribner,12.99,1925
Python Tricks,Dan Bader,Programming,Real Python,29.99,2017"""
        
        # Create temporary CSV file
        self.test_csv_path = "/tmp/test_books.csv"
        with open(self.test_csv_path, 'w') as f:
            f.write(self.test_csv_content)
        
        self.books_repo = BooksRepository(self.test_csv_path)
    
    def teardown_method(self):
        """Clean up test files."""
        if os.path.exists(self.test_csv_path):
            os.remove(self.test_csv_path)
    
    def test_books_filter_by_title(self):
        """Test filtering books by title."""
        results = self.books_repo.filter(title_contains="Clean")
        assert len(results) == 1, "Should find one book with 'Clean' in title"
        assert "Clean Code" in results[0]["Title"], "Should find Clean Code book"
    
    def test_books_filter_by_author(self):
        """Test filtering books by author."""
        results = self.books_repo.filter(author="Robert Martin")
        assert len(results) == 1, "Should find one book by Robert Martin"
        assert "Clean Code" in results[0]["Title"], "Should find Clean Code book"
    
    def test_books_filter_by_year(self):
        """Test filtering books by publication year."""
        results = self.books_repo.filter(year="2008")
        assert len(results) == 1, "Should find one book from 2008"
        assert "Clean Code" in results[0]["Title"], "Should find Clean Code book"
    
    def test_books_filter_with_limit(self):
        """Test limiting the number of results."""
        results = self.books_repo.filter(limit=2)
        assert len(results) == 2, "Should return exactly 2 books"
    
    def test_books_get_by_id(self):
        """Test getting a specific book by ID."""
        # First get all books to find an ID
        all_books = self.books_repo.filter()
        if all_books:
            book_id = all_books[0]["id"]
            book = self.books_repo.get_by_id(book_id)
            assert book is not None, "Should find book by ID"
            assert book["id"] == book_id, "Should return correct book"
    
    def test_books_get_nonexistent_id(self):
        """Test getting a book with non-existent ID."""
        book = self.books_repo.get_by_id("nonexistent_id")
        assert book is None, "Should return None for non-existent ID"


class TestExchangeRates:
    """Test the currency exchange functionality."""
    
    def setup_method(self):
        """Set up exchange rates for testing."""
        self.exchange = default_rates()
    
    def test_exchange_same_currency(self):
        """Test exchange between same currencies."""
        result = self.exchange.convert(100, "USD", "USD")
        assert result == 100.0, "Same currency conversion should return same amount"
    
    def test_exchange_usd_to_eur(self):
        """Test USD to EUR conversion."""
        result = self.exchange.convert(100, "USD", "EUR")
        assert result > 0, "Should return positive amount"
        assert result != 100, "Should be different from input amount"
        assert isinstance(result, float), "Should return float"
    
    def test_exchange_invalid_currency(self):
        """Test exchange with invalid currency codes."""
        with pytest.raises(Exception):
            self.exchange.convert(100, "INVALID", "USD")
        
        with pytest.raises(Exception):
            self.exchange.convert(100, "USD", "INVALID")
    
    def test_exchange_zero_amount(self):
        """Test exchange with zero amount."""
        result = self.exchange.convert(0, "USD", "EUR")
        assert result == 0.0, "Zero amount should return zero"
    
    def test_exchange_negative_amount(self):
        """Test exchange with negative amount."""
        result = self.exchange.convert(-100, "USD", "EUR")
        assert result < 0, "Negative amount should return negative result"


class TestIntegration:
    """Integration tests for the complete authentication flow."""
    
    def setup_method(self):
        """Clean up sessions before each test."""
        global _USER_SESSIONS, _CURRENT_SESSION
        _USER_SESSIONS.clear()
        _CURRENT_SESSION = None
    
    @pytest.mark.asyncio
    async def test_complete_authentication_flow(self):
        """Test the complete authentication and usage flow."""
        # Step 1: Check initial status (should be unauthenticated)
        status_result = await handle_call_tool("session_status", {})
        status_response = eval(status_result[0].text)
        assert status_response["authenticated"] is False
        
        # Step 2: Try to use protected operation (should fail)
        books_result = await handle_call_tool("books_query", {"limit": 1})
        books_response = eval(books_result[0].text)
        assert "error" in books_response
        assert books_response["error"] == "authentication_required"
        
        # Step 3: Authenticate
        auth_result = await handle_call_tool("authenticate", {"username": "integrationuser"})
        auth_response = eval(auth_result[0].text)
        assert auth_response["success"] is True
        assert auth_response["username"] == "integrationuser"
        
        # Step 4: Check status after authentication
        status_result = await handle_call_tool("session_status", {})
        status_response = eval(status_result[0].text)
        assert status_response["authenticated"] is True
        assert status_response["username"] == "integrationuser"
        
        # Step 5: Use protected operations (should succeed)
        books_result = await handle_call_tool("books_query", {"limit": 2})
        books_response = eval(books_result[0].text)
        assert "authenticated_user" in books_response
        assert books_response["authenticated_user"] == "integrationuser"
        assert "data" in books_response
        
        currency_result = await handle_call_tool("exchange_convert", {
            "from_currency": "USD",
            "to_currency": "EUR",
            "amount": 50
        })
        currency_response = eval(currency_result[0].text)
        assert "authenticated_user" in currency_response
        assert currency_response["authenticated_user"] == "integrationuser"
        assert currency_response["amount"] == 50.0
        
        # Step 6: Logout
        logout_result = await handle_call_tool("logout", {})
        logout_response = eval(logout_result[0].text)
        assert logout_response["success"] is True
        
        # Step 7: Try to use protected operation after logout (should fail)
        books_result = await handle_call_tool("books_query", {"limit": 1})
        books_response = eval(books_result[0].text)
        assert "error" in books_response
        assert books_response["error"] == "authentication_required"
    
    @pytest.mark.asyncio
    async def test_multiple_user_sessions(self):
        """Test that session system handles user switching correctly."""
        # Authenticate as first user
        await handle_call_tool("authenticate", {"username": "user1"})
        
        # Check session
        status_result = await handle_call_tool("session_status", {})
        status_response = eval(status_result[0].text)
        assert status_response["username"] == "user1"
        
        # Authenticate as second user (should replace first)
        await handle_call_tool("authenticate", {"username": "user2"})
        
        # Check session is now user2
        status_result = await handle_call_tool("session_status", {})
        status_response = eval(status_result[0].text)
        assert status_response["username"] == "user2"
        
        # Use operation - should show user2
        books_result = await handle_call_tool("books_query", {"limit": 1})
        books_response = eval(books_result[0].text)
        assert books_response["authenticated_user"] == "user2"


class TestErrorHandling:
    """Test error handling and edge cases."""
    
    def setup_method(self):
        """Clean up sessions before each test."""
        global _USER_SESSIONS, _CURRENT_SESSION
        _USER_SESSIONS.clear()
        _CURRENT_SESSION = None
    
    @pytest.mark.asyncio
    async def test_invalid_tool_name(self):
        """Test calling non-existent tool."""
        try:
            result = await handle_call_tool("nonexistent_tool", {})
            print(f"Unexpected result: {result}")
            assert False, f"Expected ValueError but got result: {result}"
        except ValueError as e:
            assert "Unknown tool" in str(e), f"Wrong error message: {e}"
    
    @pytest.mark.asyncio
    async def test_exchange_convert_missing_parameters(self):
        """Test currency conversion with missing required parameters."""
        # First authenticate
        await handle_call_tool("authenticate", {"username": "testuser"})
        
        # Try conversion without required parameters
        with pytest.raises(KeyError):
            await handle_call_tool("exchange_convert", {"from_currency": "USD"})
    
    @pytest.mark.asyncio
    async def test_authenticate_without_username(self):
        """Test authentication without username parameter."""
        result = await handle_call_tool("authenticate", {})
        response = eval(result[0].text)
        
        # Should still work with default username
        assert response["success"] is True
        assert "demo_user" in response["username"]


if __name__ == "__main__":
    """Run all tests."""
    pytest.main([__file__, "-v", "--tb=short"])