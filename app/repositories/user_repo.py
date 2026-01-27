from app.db.dynamo import users_table
from app.db.keys import pk_user, sk_user
from app.core.utils import get_password_hash
from botocore.exceptions import ClientError
from uuid6 import uuid7

class UserRepo:
    def __init__(self):
        self.table = users_table()

    def get_user_by_username(self, username: str):
        try:
            response = self.table.get_item(
                Key={
                    "PK": pk_user(),
                    "SK": sk_user(username)
                }
            )
            return response.get("Item")
        except ClientError:
            return None

    def create_user(self, username: str, password: str):
        if self.get_user_by_username(username):
            raise ValueError("Username already exists")

        hashed_password = get_password_hash(password)
        user_id = str(uuid7())
        
        item = {
            "PK": pk_user(),
            "SK": sk_user(username),
            "id": user_id,
            "username": username,
            "hashed_password": hashed_password,
            "is_active": True,
            "is_superuser": True # All created users via signup are admins per requirement
        }
        
        try:
            self.table.put_item(Item=item)
            return item
        except ClientError as e:
            raise ValueError(f"Could not create user: {e}")
