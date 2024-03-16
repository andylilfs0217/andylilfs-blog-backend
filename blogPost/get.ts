import { GetCommand } from "@aws-sdk/lib-dynamodb";
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

    const command = new GetCommand({
      TableName: process.env.DYNAMODB_BLOG_POST_TABLE!,
      Key: {
        id: id,
      },
    });
    const res = await docClient.send(command);

    if (!res.Item) {
      return {
        statusCode: 404,
        body: JSON.stringify({ error: "Item not found" }),
      };
    }

    return {
      statusCode: 200,
      body: JSON.stringify(res.Item),
    };
  } catch (error) {
    return {
      statusCode: 500,
      body: JSON.stringify({ error: "Internal Server Error" }),
    };
  }
};
