import datetime
import json
import os
import boto3
from uuid import uuid4

# Initialize the DynamoDB client
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["ANDYLILFSBLOGTABLE_TABLE_NAME"])


def get_blogs(event, context):
    # Log the event argument for debugging and for use in local development.
    print(json.dumps(event))

    return {
        "statusCode": 200,
        "body": json.dumps(
            {
                "message": "get blogs",
                # "location": ip.text.replace("\n", "")
            }
        ),
    }


def get_blog_by_id(event, context):
    # Log the event argument for debugging and for use in local development.
    print(json.dumps(event))

    return {
        "statusCode": 200,
        "body": json.dumps(
            {
                "message": "get blog by id",
                # "location": ip.text.replace("\n", "")
            }
        ),
    }


def create_blog(event, context):
    try:
        # Parse the incoming JSON body from the event
        body = json.loads(event["body"])

        # Generate a unique ID for the blog post
        post_id = str(uuid4())

        # Prepare the item to be inserted into DynamoDB
        item = {
            "id": post_id,
            "title": body.get("title"),  # String
            "date": body.get("date"),  # Date
            "tags": body.get("tags"),  # List of strings
            "lastmod": body.get("lastmod"),  # Date
            "draft": body.get("draft"),  # Boolean
            "summary": body.get("summary"),  # String
            "images": body.get("images"),  # JSON
            "authors": body.get("authors"),  # List of strings
            "layout": body.get("layout"),  # String
            "bibliography": body.get("bibliography"),  # String
            "canonicalURL": body.get("canonicalURL"),  # String
            "content": body.get("content"),  # String
        }

        # Insert the item into DynamoDB
        table.put_item(Item=item)

        return {
            "statusCode": 201,
            "body": json.dumps(
                {"message": "Blog post created successfully", "postId": post_id}
            ),
        }
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps({"message": "Error creating blog post"}),
        }


def update_blog_by_id(event, context):
    # Log the event argument for debugging and for use in local development.
    print(json.dumps(event))

    return {
        "statusCode": 200,
        "body": json.dumps(
            {
                "message": "update blog by id",
                # "location": ip.text.replace("\n", "")
            }
        ),
    }


def delete_blog_by_id(event, context):
    # Log the event argument for debugging and for use in local development.
    print(json.dumps(event))

    return {
        "statusCode": 200,
        "body": json.dumps(
            {
                "message": "delete blog by id",
                # "location": ip.text.replace("\n", "")
            }
        ),
    }
