from app.repositories.user_repo import UserRepo
from app.services.token import TokenService
from app.core.utils import verify_password
from app.core.config import settings

class AuthService:
    def __init__(self):
        self.user_repo = UserRepo()

    def authenticate_user(self, username, password):
        user = self.user_repo.get_user_by_username(username)
        if not user:
            return None
        if not verify_password(password, user["hashed_password"]):
            return None
        return user

    def login(self, username, password):
        user = self.authenticate_user(username, password)
        if not user:
            return None
        
        access_token = TokenService.create_access_token(
            data={"sub": user["username"]}
        )
        refresh_token = TokenService.create_refresh_token(
            data={"sub": user["username"]}
        )
        return access_token, refresh_token

    def refresh_session(self, token: str):
        payload = TokenService.verify_token(token)
        if not payload or payload.get("type") != "refresh":
            return None
        
        username = payload.get("sub")
        if not username:
            return None
            
        user = self.user_repo.get_user_by_username(username)
        if not user:
            return None
            
        access_token = TokenService.create_access_token(
            data={"sub": username}
        )
        refresh_token = TokenService.create_refresh_token(
            data={"sub": username}
        )
        return access_token, refresh_token

    def signup(self, username, password, passkey):
        if passkey != settings.PASSKEY:
            raise ValueError("Invalid passkey for admin creation")
        
        return self.user_repo.create_user(username, password)
