import { ScanCommand } from "@aws-sdk/lib-dynamodb";
import { docClient } from "../dynamodbClient";
import { APIGatewayProxyEvent, APIGatewayProxyResult } from "aws-lambda";

export const handler = async (
  event: APIGatewayProxyEvent
): Promise<APIGatewayProxyResult> => {
  const command = new ScanCommand({
    // ProjectionExpression: "#Name, Color, AvgLifeSpan",
    // ExpressionAttributeNames: { "#Name": "Name" },
    TableName: process.env.DYNAMODB_BLOG_POST_TABLE!,
  });
  const res = await docClient.send(command);
  return {
    statusCode: 200,
    body: JSON.stringify(res),
  };
};
