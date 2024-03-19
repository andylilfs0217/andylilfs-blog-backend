import { PutCommand } from "@aws-sdk/lib-dynamodb";
import { docClient } from "../utils/dynamodbClient";
import { BlogPost } from "../models/blogPost";
import { APIGatewayProxyEvent, APIGatewayProxyResult } from "aws-lambda";
import { jsonResponse } from "../utils/jsonResponse";

export const handler = async (
  event: APIGatewayProxyEvent
): Promise<APIGatewayProxyResult> => {
  const body = JSON.parse(event.body!);
  const { title, content, author, coverImage, subtitle } = body;
  const blogPost = new BlogPost(title, content, author, coverImage, subtitle);
  const command = new PutCommand({
    TableName: process.env.DYNAMODB_BLOG_POST_TABLE!,
    Item: blogPost,
  });
  const res = await docClient.send(command);
  return jsonResponse(201, JSON.stringify(res.Attributes));
};
