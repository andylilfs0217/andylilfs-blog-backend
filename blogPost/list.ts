import { APIGatewayProxyEvent, APIGatewayProxyResult } from "aws-lambda";
import { ScanCommand } from "@aws-sdk/lib-dynamodb";
import { docClient } from "../utils/dynamodbClient";
import { jsonResponse } from "../utils/jsonResponse";

export const handler = async (
  event: APIGatewayProxyEvent
): Promise<APIGatewayProxyResult> => {
  try {
    const command = new ScanCommand({
      TableName: process.env.DYNAMODB_BLOG_POST_TABLE,
    });
    const res = await docClient.send(command);
    res.Items?.sort((a, b) => b.createdAt.localeCompare(a.createdAt));

    return jsonResponse(200, JSON.stringify(res.Items));
  } catch (error) {
    // Handle the error here
    console.error("An error occurred:", error);
    return jsonResponse(500, "Internal Server Error");
  }
};
