from datetime import datetime
import os
from uuid6 import uuid7
from typing import Optional
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError
from app.db.dynamo import projects_table
from app.db.keys import pk_projects, sk_project


class ProjectRepo:
    def __init__(self):
        self.table = projects_table()

    def list_projects(self):
        try:
            response = self.table.query(
                KeyConditionExpression=Key("PK").eq(pk_projects())
            )
            return response.get('Items', [])
        except ClientError as e:
            print(f"Error listing projects: {e}")
            return []

    def get_project(self, id_or_slug: str):
        try:
            response = self.table.get_item(
                Key={
                    "PK": pk_projects(),
                    "SK": sk_project(id_or_slug)
                }
            )
            item = response.get('Item')
            if item:
                return item

            response = self.table.query(
                KeyConditionExpression=Key("PK").eq(pk_projects()),
                FilterExpression=Attr("slug").eq(id_or_slug)
            )
            items = response.get('Items', [])
            return items[0] if items else None
            
        except ClientError as e:
            print(f"Error getting project {id_or_slug}: {e}")
            return None

    def create_project(self, project_data: dict):
        now = datetime.now().isoformat()
        project_id = uuid7()
        
        item = {
            "PK": pk_projects(),
            "SK": sk_project(str(project_id)),
            "id": str(project_id),
            **project_data,
            "created_at": now,
            "updated_at": now
        }

        try:
            self.table.put_item(
                Item=item,
                ConditionExpression="attribute_not_exists(PK) AND attribute_not_exists(SK)"
            )
            return item
        except ClientError as e:
            print(f"Error creating project: {e}")
            raise e

    def update_project(self, project_id: str, updates: dict):
        now = datetime.now().isoformat()
        
        update_expr_parts = []
        expr_attr_names = {}
        expr_attr_values = {}

        # Filter out None values
        valid_updates = {k: v for k, v in updates.items() if v is not None}
        
        if not valid_updates:
            return self.get_project(project_id)

        for key, value in valid_updates.items():
            attr_name = f"#{key}"
            attr_value = f":{key}"
            update_expr_parts.append(f"{attr_name} = {attr_value}")
            expr_attr_names[attr_name] = key
            expr_attr_values[attr_value] = value

        update_expr_parts.append("#updated_at = :updated_at")
        expr_attr_names["#updated_at"] = "updated_at"
        expr_attr_values[":updated_at"] = now
        real_id = project_id
        current_project = self.get_project(project_id)
        if current_project and current_project.get('id'):
            real_id = current_project.get('id')
        elif not current_project:
             return None

        try:
            response = self.table.update_item(
                Key={
                    "PK": pk_projects(),
                    "SK": sk_project(real_id)
                },
                UpdateExpression="SET " + ", ".join(update_expr_parts),
                ExpressionAttributeNames=expr_attr_names,
                ExpressionAttributeValues=expr_attr_values,
                ReturnValues="ALL_NEW",
                ConditionExpression="attribute_exists(PK) AND attribute_exists(SK)"
            )
            return response.get("Attributes")
        except ClientError as e:
            print(f"Error updating project {project_id}: {e}")
            raise e

    def delete_project(self, project_id: str):
        try:
            self.table.delete_item(
                Key={
                    "PK": pk_projects(),
                    "SK": sk_project(project_id)
                },
                ConditionExpression="attribute_exists(PK) AND attribute_exists(SK)"
            )
            return True
        except ClientError as e:
            print(f"Error deleting project {project_id}: {e}")
            raise e

        try:
            self.table.delete_item(
                Key={
                    "PK": pk_projects(),
                    "SK": sk_project(project_id)
                },
                ConditionExpression="attribute_exists(PK) AND attribute_exists(SK)"
            )
            return True
        except ClientError as e:
            print(f"Error deleting project {project_id}: {e}")
            raise e
