import os
from uuid6 import uuid7
from botocore.exceptions import ClientError
from app.db.dynamo import profile_table
from app.db.keys import (
    pk_profile,
    sk_exp,
    sk_paper,
    sk_ach,
    pk_bio,
    sk_bio
)


class ProfileRepo:
    def __init__(self):
        self.table = profile_table()
    
    def list_experience(self):
        try:
            response = self.table.query(
                KeyConditionExpression="PK = :pk AND begins_with(SK, :sk)",
                ExpressionAttributeValues={
                    ":pk": pk_profile(),
                    ":sk": "EXP#"
                }
            )
            return response.get("Items", [])
        except ClientError as e:
            print(f"Error listing experience: {e}")
            return []
    
    def create_experience(self, data: dict):
        exp_id = str(uuid7())
        item = {
            "PK": pk_profile(),
            "SK": sk_exp(exp_id),
            "id": exp_id,
            **data
        }
        self.table.put_item(Item=item)
        return item

    def update_experience(self, exp_id: str, updates: dict):
        update_expr = []
        expr_attr_names = {}
        expr_attr_values = {}

        for key, value in updates.items():
            if value is not None:
                attr_name = f"#{key}"
                attr_value = f":{key}"
                update_expr.append(f"{attr_name} = {attr_value}")
                expr_attr_names[attr_name] = key
                expr_attr_values[attr_value] = value

        if not update_expr:
            return None

        try:
            response = self.table.update_item(
                Key={
                    "PK": pk_profile(),
                    "SK": sk_exp(exp_id)
                },
                UpdateExpression="SET " + ", ".join(update_expr),
                ExpressionAttributeNames=expr_attr_names,
                ExpressionAttributeValues=expr_attr_values,
                ReturnValues="ALL_NEW",
                ConditionExpression="attribute_exists(PK) AND attribute_exists(SK)"
            )
            return response.get("Attributes")
        except ClientError:
            return None

    def delete_experience(self, exp_id: str):
        try:
            self.table.delete_item(
                Key={
                    "PK": pk_profile(),
                    "SK": sk_exp(exp_id)
                },
                ConditionExpression="attribute_exists(PK) AND attribute_exists(SK)"
            )
            return True
        except ClientError:
            return False

    def list_papers(self):
        try:
            response = self.table.query(
                KeyConditionExpression="PK = :pk AND begins_with(SK, :sk)",
                ExpressionAttributeValues={
                    ":pk": pk_profile(),
                    ":sk": "PAPER#"
                }
            )
            return response.get("Items", [])
        except ClientError as e:
            print(f"Error listing papers: {e}")
            return []

    def create_paper(self, data: dict):
        paper_id = str(uuid7())
        item = {
            "PK": pk_profile(),
            "SK": sk_paper(paper_id),
            "id": paper_id,
            **data
        }
        self.table.put_item(Item=item)
        return item

    def update_paper(self, paper_id: str, updates: dict):
        update_expr = []
        expr_attr_names = {}
        expr_attr_values = {}

        for key, value in updates.items():
            if value is not None:
                attr_name = f"#{key}"
                attr_value = f":{key}"
                update_expr.append(f"{attr_name} = {attr_value}")
                expr_attr_names[attr_name] = key
                expr_attr_values[attr_value] = value

        if not update_expr:
            return None

        try:
            response = self.table.update_item(
                Key={
                    "PK": pk_profile(),
                    "SK": sk_paper(paper_id)
                },
                UpdateExpression="SET " + ", ".join(update_expr),
                ExpressionAttributeNames=expr_attr_names,
                ExpressionAttributeValues=expr_attr_values,
                ReturnValues="ALL_NEW",
                ConditionExpression="attribute_exists(PK) AND attribute_exists(SK)"
            )
            return response.get("Attributes")
        except ClientError:
            return None

    def delete_paper(self, paper_id: str):
        try:
            self.table.delete_item(
                Key={
                    "PK": pk_profile(),
                    "SK": sk_paper(paper_id)
                },
                ConditionExpression="attribute_exists(PK) AND attribute_exists(SK)"
            )
            return True
        except ClientError:
            return False

    def list_achievements(self):
        try:
            response = self.table.query(
                KeyConditionExpression="PK = :pk AND begins_with(SK, :sk)",
                ExpressionAttributeValues={
                    ":pk": pk_profile(),
                    ":sk": "ACH#"
                }
            )
            return response.get("Items", [])
        except ClientError as e:
            print(f"Error listing achievements: {e}")
            return []

    def create_achievement(self, data: dict):
        ach_id = str(uuid7())
        item = {
            "PK": pk_profile(),
            "SK": sk_ach(ach_id),
            "id": ach_id,
            **data
        }
        self.table.put_item(Item=item)
        return item

    def update_achievement(self, ach_id: str, updates: dict):
        update_expr = []
        expr_attr_names = {}
        expr_attr_values = {}

        for key, value in updates.items():
            if value is not None:
                attr_name = f"#{key}"
                attr_value = f":{key}"
                update_expr.append(f"{attr_name} = {attr_value}")
                expr_attr_names[attr_name] = key
                expr_attr_values[attr_value] = value

        if not update_expr:
            return None

        try:
            response = self.table.update_item(
                Key={
                    "PK": pk_profile(),
                    "SK": sk_ach(ach_id)
                },
                UpdateExpression="SET " + ", ".join(update_expr),
                ExpressionAttributeNames=expr_attr_names,
                ExpressionAttributeValues=expr_attr_values,
                ReturnValues="ALL_NEW",
                ConditionExpression="attribute_exists(PK) AND attribute_exists(SK)"
            )
            return response.get("Attributes")
        except ClientError:
            return None

    def delete_achievement(self, ach_id: str):
        try:
            self.table.delete_item(
                Key={
                    "PK": pk_profile(),
                    "SK": sk_ach(ach_id)
                },
                ConditionExpression="attribute_exists(PK) AND attribute_exists(SK)"
            )
            return True
        except ClientError:
            return False

    def get_bio(self):
        try:
            response = self.table.get_item(
                Key={
                    "PK": pk_bio(),
                    "SK": sk_bio()
                }
            )
            item = response.get("Item")
            if item:
                # remove internal keys
                item.pop("PK", None)
                item.pop("SK", None)
                return item
            return {}
        except ClientError as e:
            print(f"Error getting bio: {e}")
            return {}

    def update_bio(self, data: dict):
        item = {
            "PK": pk_bio(),
            "SK": sk_bio(),
            **data
        }
        try:
            self.table.put_item(Item=item)
            return True
        except ClientError as e:
            print(f"Error updating bio: {e}")
            return False
