import datetime
import json
import os
import boto3
from uuid import uuid4

###SECTION - GLOBAL VARIABLES

# Initialize the DynamoDB client
# Get environment variables
aws_environment = os.environ["AWSENV"]

# Check if executing locally or on AWS, and configure DynamoDB connection accordingly.
if aws_environment == "AWS_SAM_LOCAL":
    print("Using local DynamoDB")
    dynamodb = boto3.resource("dynamodb", endpoint_url="http://dynamodb-local:8000")
else:
    print("Using AWS DynamoDB")
    dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["ANDYLILFSBLOGTABLE_TABLE_NAME"])

###!SECTION


###SECTION - VALIDATION FUNCTIONS
def validate_string(value, field_name, max_length=None):
    """
    Validates that the given value is a string and optionally checks its length.

    Args:
        value (any): The value to validate.
        field_name (str): The name of the field being validated, used in error messages.
        max_length (int, optional): The maximum allowed length of the string. Defaults to None.

    Raises:
        ValueError: If the value is not a string or if it exceeds the maximum length.
    """
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be a string")
    if max_length and len(value) > max_length:
        raise ValueError(f"{field_name} must be no longer than {max_length} characters")


def validate_date(value, field_name):
    """
    Validates that the given value is a valid ISO format date.

    Args:
        value (str): The date string to validate.
        field_name (str): The name of the field being validated, used in the error message.

    Raises:
        ValueError: If the value is not a valid ISO format date.
    """
    try:
        datetime.fromisoformat(value)
    except ValueError:
        raise ValueError(f"{field_name} must be a valid ISO format date")


def validate_list_of_strings(value, field_name):
    """
    Validates that the given value is a list of strings.

    Args:
        value (any): The value to be validated.
        field_name (str): The name of the field being validated, used in the error message.

    Raises:
        ValueError: If the value is not a list or if any element in the list is not a string.
    """
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        raise ValueError(f"{field_name} must be a list of strings")


def validate_boolean(value, field_name):
    """
    Validates that the given value is a boolean.

    Args:
        value: The value to be checked.
        field_name: The name of the field being validated, used in the error message.

    Raises:
        ValueError: If the value is not a boolean.
    """
    if not isinstance(value, bool):
        raise ValueError(f"{field_name} must be a boolean")


def validate_json(value, field_name):
    """
    Validates that the given value is a JSON object (dictionary).

    Args:
        value (any): The value to be validated.
        field_name (str): The name of the field being validated, used in the error message.

    Raises:
        ValueError: If the value is not a dictionary.
    """
    if not isinstance(value, dict):
        raise ValueError(f"{field_name} must be a valid JSON object")


###!SECTION


###SECTION - HANDLER FUNCTIONS
def get_blogs(event, context):
    """
    Retrieve all blog entries from the database.

    This function scans the database table for all blog entries and returns them
    in the response. If an error occurs during the scan, it catches the exception
    and returns a 500 status code with an error message.

    Args:
        event (dict): The event dictionary containing request parameters.
        context (object): The context object providing runtime information.

    Returns:
        dict: A dictionary containing the status code and the response body.
            - If successful, the status code is 200 and the body contains the list of blogs.
            - If an error occurs, the status code is 500 and the body contains an error message.
    """
    try:
        response = table.scan()
        items = response.get("Items", [])

        return {
            "statusCode": 200,
            "body": json.dumps({"count": len(items), "blogs": items}),
        }
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps({"message": "Error retrieving blogs"}),
        }


def get_blog_by_id(event, context):
    """
    Retrieve a blog post by its ID from the database.

    Args:
        event (dict): The event dictionary containing request parameters.
                      Expected to have a "pathParameters" key with an "id".
        context (object): The context in which the function is called (not used).

    Returns:
        dict: A dictionary containing the HTTP status code and the response body.
              - If the blog post is found, returns status code 200 and the blog post data in JSON format.
              - If the blog post is not found, returns status code 404 and an error message in JSON format.
              - If an error occurs during retrieval, returns status code 500 and an error message in JSON format.
    """
    try:
        blog_id = event["pathParameters"]["id"]
        response = table.get_item(Key={"id": blog_id})
        item = response.get("Item")

        if item:
            return {"statusCode": 200, "body": json.dumps(item)}
        else:
            return {
                "statusCode": 404,
                "body": json.dumps({"message": "Blog not found"}),
            }
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps({"message": "Error retrieving blog"}),
        }


def create_blog(event, context):
    """
    Creates a new blog post and inserts it into a DynamoDB table.

    Args:
        event (dict): The event dictionary containing the HTTP request data.
                      Expected to have a "body" key with a JSON string.
        context (object): The context in which the function is called (not used).

    Returns:
        dict: A dictionary containing the HTTP response with a status code and a message.
              - On success: {"statusCode": 201, "body": json.dumps({"message": "Blog post created successfully", "postId": post_id})}
              - On failure: {"statusCode": 500, "body": json.dumps({"message": "Error creating blog post"})}

    Raises:
        Exception: If there is an error during the creation of the blog post.
    """
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
    """
    Update a blog post by its ID.

    This function handles an AWS Lambda event to update a blog post in a DynamoDB table.
    It extracts the blog ID from the event path parameters and the update data from the event body.
    The function constructs an update expression and updates the blog post in the DynamoDB table.

    Parameters:
    event (dict): The event dictionary containing the request data.
        - pathParameters (dict): Contains the blog ID under the key "id".
        - body (str): A JSON string containing the update data.
    context (object): The context in which the function is called (not used in this function).

    Returns:
    dict: A dictionary containing the status code and a message.
        - statusCode (int): The HTTP status code of the response.
        - body (str): A JSON string containing the response message and the updated blog post if successful.

    Raises:
    Exception: If there is an error during the update process, an exception is caught and a 500 status code is returned.
    """
    try:
        blog_id = event["pathParameters"]["id"]
        body = json.loads(event["body"])

        update_expression = "set "
        expression_attribute_values = {}
        expression_attribute_names = {}

        for key, value in body.items():
            update_expression += f"#{key} = :{key}, "
            expression_attribute_values[f":{key}"] = value
            expression_attribute_names[f"#{key}"] = key

        update_expression = update_expression.rstrip(", ")

        response = table.update_item(
            Key={"id": blog_id},
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attribute_values,
            ExpressionAttributeNames=expression_attribute_names,
            ReturnValues="ALL_NEW",
        )

        return {
            "statusCode": 200,
            "body": json.dumps(
                {
                    "message": "Blog updated successfully",
                    "updatedBlog": response["Attributes"],
                }
            ),
        }
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps({"message": "Error updating blog post"}),
        }


def delete_blog_by_id(event, context):
    """
    Deletes a blog post by its ID.

    This function handles the deletion of a blog post from a DynamoDB table
    based on the ID provided in the event's path parameters. It returns a
    response indicating the success or failure of the deletion operation.

    Args:
        event (dict): The event dictionary containing the path parameters.
                      Expected to have a key "pathParameters" with a nested
                      key "id" representing the blog post ID.
        context (object): The context in which the function is called.
                          (Not used in this function)

    Returns:
        dict: A dictionary containing the status code and a message. If the
              deletion is successful, it includes the deleted blog post's
              attributes. If the blog post is not found, it returns a 404
              status code. If an error occurs, it returns a 500 status code.
    """
    try:
        blog_id = event["pathParameters"]["id"]

        response = table.delete_item(Key={"id": blog_id}, ReturnValues="ALL_OLD")

        if "Attributes" in response:
            return {
                "statusCode": 200,
                "body": json.dumps(
                    {
                        "message": "Blog deleted successfully",
                        "deletedBlog": response["Attributes"],
                    }
                ),
            }
        else:
            return {
                "statusCode": 404,
                "body": json.dumps({"message": "Blog not found"}),
            }
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps({"message": "Error deleting blog post"}),
        }


###!SECTION
