import { ScanCommand } from "@aws-sdk/lib-dynamodb";
import { docClient } from "../dynamodbClient";
import { APIGatewayProxyEvent, APIGatewayProxyResult } from "aws-lambda";
import { jsonResponse } from "../utils/jsonResponse";

export const handler = async (
  event: APIGatewayProxyEvent
): Promise<APIGatewayProxyResult> => {
  const command = new ScanCommand({
    TableName: process.env.DYNAMODB_BLOG_POST_TABLE!,
  });
  const res = await docClient.send(command);
  return jsonResponse(200, JSON.stringify(res.Items));
};
