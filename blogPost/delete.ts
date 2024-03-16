import { DeleteCommand } from "@aws-sdk/lib-dynamodb";
import { docClient } from "../dynamodbClient";
import { APIGatewayProxyEvent, APIGatewayProxyResult } from "aws-lambda";

export const handler = async (
  event: APIGatewayProxyEvent
): Promise<APIGatewayProxyResult> => {
  try {
    const id = event.pathParameters?.id; // Assuming the ID is passed as a path parameter
    if (!id) {
      return {
        statusCode: 400,
        body: JSON.stringify({ error: "ID is missing" }),
      };
    }

    const command = new DeleteCommand({
      TableName: process.env.DYNAMODB_BLOG_POST_TABLE!,
      Key: {
        id: id,
      },
    });
    await docClient.send(command);

    return {
      statusCode: 204, // No content
      body: "",
    };
  } catch (error) {
    return {
      statusCode: 500,
      body: JSON.stringify({ error: "Internal Server Error" }),
    };
  }
};
