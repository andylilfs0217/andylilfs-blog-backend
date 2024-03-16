import { PutCommand } from "@aws-sdk/lib-dynamodb";
import { docClient } from "../dynamodbClient";
import { BlogPost } from "../models/blogPost";
import { APIGatewayProxyEvent, APIGatewayProxyResult } from "aws-lambda";

export const handler = async (
  event: APIGatewayProxyEvent
): Promise<APIGatewayProxyResult> => {
  const body = JSON.parse(event.body!);
  const { title, content, author } = body;
  const blogPost = new BlogPost(title, content, author);
  const command = new PutCommand({
    TableName: process.env.DYNAMODB_BLOG_POST_TABLE!,
    Item: blogPost,
  });
  const res = await docClient.send(command);
  return {
    statusCode: 201,
    body: JSON.stringify(res),
  };
};