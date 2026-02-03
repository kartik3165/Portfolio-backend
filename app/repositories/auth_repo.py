from datetime import datetime
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from app.db.dynamo import profile_table


class AuthRepo:
    def __init__(self):
        self.table = profile_table()
        self.ph = PasswordHasher()
        
    async def credentials_exist(self) -> bool:
        """Check if admin credentials are already initialized"""
        try:
            response = self.table.get_item(
                Key={
                    "PK": "ADMIN#CREDENTIALS",
                    "SK": "METADATA"
                }
            )
            return "Item" in response
        except Exception as e:
            print(f"Error checking credentials: {e}")
            return False
    
    async def get_credentials(self) -> dict | None:
        """Retrieve stored admin credentials"""
        try:
            response = self.table.get_item(
                Key={
                    "PK": "ADMIN#CREDENTIALS",
                    "SK": "METADATA"
                }
            )
            return response.get("Item")
        except Exception as e:
            print(f"Error getting credentials: {e}")
            return None
    
    async def init_credentials(self, email: str, password: str) -> dict:
        """Initialize credentials from environment variables"""
        normalized_email = email.lower().strip()
        password_hash = self.ph.hash(password)
        now = datetime.now().isoformat()
        
        item = {
            "PK": "ADMIN#CREDENTIALS",
            "SK": "METADATA",
            "email": normalized_email,
            "password_hash": password_hash,
            "created_at": now,
            "updated_at": now
        }
        
        try:
            self.table.put_item(
                Item=item,
                ConditionExpression="attribute_not_exists(PK) AND attribute_not_exists(SK)"
            )
            return {"email": email}
        except Exception as e:
            print(f"Error initializing credentials: {e}")
            raise e
    
    async def update_credentials(self, email: str | None = None, password: str | None = None) -> dict:
        """Update admin credentials"""
        now = datetime.now().isoformat()
        
        update_expr_parts = []
        expr_attr_names = {}
        expr_attr_values = {}
        
        if email:
            normalized_email = email.lower().strip()
            update_expr_parts.append("#email = :email")
            expr_attr_names["#email"] = "email"
            expr_attr_values[":email"] = normalized_email
        
        if password:
            password_hash = self.ph.hash(password)
            update_expr_parts.append("#password_hash = :password_hash")
            expr_attr_names["#password_hash"] = "password_hash"
            expr_attr_values[":password_hash"] = password_hash
        
        update_expr_parts.append("#updated_at = :updated_at")
        expr_attr_names["#updated_at"] = "updated_at"
        expr_attr_values[":updated_at"] = now
        
        try:
            response = self.table.update_item(
                Key={
                    "PK": "ADMIN#CREDENTIALS",
                    "SK": "METADATA"
                },
                UpdateExpression="SET " + ", ".join(update_expr_parts),
                ExpressionAttributeNames=expr_attr_names,
                ExpressionAttributeValues=expr_attr_values,
                ReturnValues="ALL_NEW",
                ConditionExpression="attribute_exists(PK) AND attribute_exists(SK)"
            )
            return response.get("Attributes")
        except Exception as e:
            print(f"Error updating credentials: {e}")
            raise e
    
    async def verify_password(self, password: str) -> bool:
        """Verify a password against the stored hash"""
        creds = await self.get_credentials()
        if not creds:
            return False
        
        try:
            self.ph.verify(creds["password_hash"], password)
            return True
        except VerifyMismatchError:
            return False
