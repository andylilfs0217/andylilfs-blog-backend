import datetime
import json
import os
import boto3
from uuid import uuid4
from operator import itemgetter

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
    Validates that the given value is a string or None and optionally checks its length.

    Args:
        value (any): The value to validate.
        field_name (str): The name of the field being validated, used in error messages.
        max_length (int, optional): The maximum allowed length of the string. Defaults to None.

    Raises:
        ValueError: If the value is not a string or None, or if it exceeds the maximum length.
    """
    if value is not None and not isinstance(value, str):
        raise ValueError(f"{field_name} must be a string or None")
    if value is not None and max_length and len(value) > max_length:
        raise ValueError(f"{field_name} must be no longer than {max_length} characters")


def validate_date(value, field_name):
    """
    Validates that the given value is a valid ISO format date or None.

    Args:
        value (str): The date string to validate.
        field_name (str): The name of the field being validated, used in the error message.

    Raises:
        ValueError: If the value is not a valid ISO format date or None.
    """
    if value is not None:
        try:
            datetime.datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%fZ")
        except ValueError:
            raise ValueError(f"{field_name} must be a valid ISO format date or None")


def validate_list_of_strings(value, field_name):
    """
    Validates that the given value is a list of strings, an empty list, or None.

    Args:
        value (any): The value to be validated.
        field_name (str): The name of the field being validated, used in the error message.

    Raises:
        ValueError: If the value is not a list of strings, an empty list, or None.
    """
    if value is not None:
        if not isinstance(value, list):
            raise ValueError(
                f"{field_name} must be a list of strings, an empty list, or None"
            )
        if value and not all(isinstance(item, str) for item in value):
            raise ValueError(f"{field_name} must contain only strings")


def validate_boolean(value, field_name):
    """
    Validates that the given value is a boolean or None.

    Args:
        value: The value to be checked.
        field_name: The name of the field being validated, used in the error message.

    Raises:
        ValueError: If the value is not a boolean or None.
    """
    if value is not None and not isinstance(value, bool):
        raise ValueError(f"{field_name} must be a boolean or None")


def validate_json(value, field_name):
    """
    Validates that the given value is a JSON object (dictionary) or None.

    Args:
        value (any): The value to be validated.
        field_name (str): The name of the field being validated, used in the error message.

    Raises:
        ValueError: If the value is not a dictionary or None.
    """
    if value is not None and not isinstance(value, dict):
        raise ValueError(f"{field_name} must be a valid JSON object or None")


###!SECTION


###SECTION - HANDLER FUNCTIONS
def get_blogs(event, context):
    """
    Retrieve all blog entries from the database, sorted by date in descending order.

    This function scans the database table for all blog entries, sorts them by date
    in descending order, and returns them in the response. If an error occurs during
    the scan or sorting process, it catches the exception and returns a 500 status code
    with an error message.

    Args:
        event (dict): The event dictionary containing request parameters.
        context (object): The context object providing runtime information.

    Returns:
        dict: A dictionary containing the status code and the response body.
            - If successful, the status code is 200 and the body contains the sorted list of blogs.
            - If an error occurs, the status code is 500 and the body contains an error message.
    """
    try:
        response = table.scan()
        items = response.get("Items", [])

        # Sort items by date in descending order
        sorted_items = sorted(items, key=itemgetter("date"), reverse=True)

        return {
            "statusCode": 200,
            "body": json.dumps({"count": len(sorted_items), "blogs": sorted_items}),
        }
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps({"message": "Error retrieving and sorting blogs"}),
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
    try:
        body = json.loads(event["body"])
        post_id = str(uuid4())
        print(f"post_id: {post_id}")

        item = {
            "id": post_id,
            "title": body.get("title"),
            "date": body.get("date"),
            "tags": body.get("tags"),
            "lastmod": body.get("lastmod"),
            "draft": body.get("draft"),
            "summary": body.get("summary"),
            "image": body.get("image"),
            "authors": body.get("authors"),
            "layout": body.get("layout"),
            "bibliography": body.get("bibliography"),
            "canonicalUrl": body.get("canonicalUrl"),
            "content": body.get("content"),
        }

        # Validate the item fields
        validate_string(item["title"], "title", max_length=100)
        validate_date(item["date"], "date")
        validate_list_of_strings(item["tags"], "tags")
        validate_date(item["lastmod"], "lastmod")
        validate_boolean(item["draft"], "draft")
        validate_string(item["summary"], "summary", max_length=500)
        validate_list_of_strings(item["image"], "image")
        validate_list_of_strings(item["authors"], "authors")
        validate_string(item["layout"], "layout", max_length=50)
        validate_string(item["bibliography"], "bibliography", max_length=500)
        validate_string(item["canonicalUrl"], "canonicalUrl", max_length=100)
        validate_string(item["content"], "content")

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

        # Validate the updated fields
        if "title" in body:
            validate_string(body["title"], "title", max_length=100)
        if "date" in body:
            validate_date(body["date"], "date")
        if "tags" in body:
            validate_list_of_strings(body["tags"], "tags")
        if "lastmod" in body:
            validate_date(body["lastmod"], "lastmod")
        if "draft" in body:
            validate_boolean(body["draft"], "draft")
        if "summary" in body:
            validate_string(body["summary"], "summary", max_length=500)
        if "image" in body:
            validate_list_of_strings(body["image"], "image")
        if "authors" in body:
            validate_list_of_strings(body["authors"], "authors")
        if "layout" in body:
            validate_string(body["layout"], "layout", max_length=50)
        if "bibliography" in body:
            validate_string(body["bibliography"], "bibliography", max_length=500)
        if "canonicalUrl" in body:
            validate_string(body["canonicalUrl"], "canonicalUrl", max_length=100)
        if "content" in body:
            validate_string(body["content"], "content")

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
    except ValueError as ve:
        print(f"Validation Error: {str(ve)}")
        return {
            "statusCode": 400,
            "body": json.dumps({"message": f"Validation Error: {str(ve)}"}),
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
