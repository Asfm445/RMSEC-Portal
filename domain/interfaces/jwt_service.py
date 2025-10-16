from abc import ABC, abstractmethod


class JWTServiceInterface(ABC):
    @abstractmethod
    def create_refresh_token(self, data: dict) -> str:
        """Create a JWT refresh token"""
        pass
    
    @abstractmethod
    def create_access_token(self, data: dict) -> str:
        """Create a JWT access token with custom expiration"""
        pass

    @abstractmethod
    def decode_token(self, token: str) -> dict:
        """Decode a JWT token and return the payload"""
        pass