import { GetCommand, UpdateCommand } from "@aws-sdk/lib-dynamodb";
import { docClient } from "../dynamodbClient";
import { APIGatewayProxyEvent, APIGatewayProxyResult } from "aws-lambda";

export const handler = async (
  event: APIGatewayProxyEvent
): Promise<APIGatewayProxyResult> => {
  const body = JSON.parse(event.body!);
  const id = event.pathParameters?.id;
  if (!id) {
    return {
      statusCode: 400,
      body: JSON.stringify({ error: "ID is missing" }),
    };
  }
  const { title, content, author } = body;
  const updatedAt = new Date().toISOString();

  // Retrieve the existing blog post from the database
  const getCommand = new GetCommand({
    TableName: process.env.DYNAMODB_BLOG_POST_TABLE!,
    Key: { id },
  });
  const existingPost = await docClient.send(getCommand);

  // Update the blog post with the new values
  const updatedPost = {
    ...existingPost.Item,
    title,
    content,
    author,
    updatedAt,
  };

  // Save the updated blog post to the database
  const updateCommand = new UpdateCommand({
    TableName: process.env.DYNAMODB_BLOG_POST_TABLE!,
    Key: { id },
    UpdateExpression:
      "SET title = :title, content = :content, author = :author, updatedAt = :updatedAt",
    ExpressionAttributeValues: {
      ":title": updatedPost.title,
      ":content": updatedPost.content,
      ":author": updatedPost.author,
      ":updatedAt": updatedPost.updatedAt,
    },
    ReturnValues: "ALL_NEW",
  });
  const res = await docClient.send(updateCommand);

  return {
    statusCode: 200,
    body: JSON.stringify(res.Attributes),
  };
};
