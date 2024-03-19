import { GetCommand } from "@aws-sdk/lib-dynamodb";
import { docClient } from "../utils/dynamodbClient";
import { APIGatewayProxyEvent, APIGatewayProxyResult } from "aws-lambda";
import { jsonResponse } from "../utils/jsonResponse";

export const handler = async (
  event: APIGatewayProxyEvent
): Promise<APIGatewayProxyResult> => {
  try {
    const id = event.pathParameters?.id; // Assuming the ID is passed as a path parameter
    if (!id) {
      return jsonResponse(400, JSON.stringify({ error: "ID is missing" }));
    }

    const command = new GetCommand({
      TableName: process.env.DYNAMODB_BLOG_POST_TABLE!,
      Key: {
        id: id,
      },
    });
    const res = await docClient.send(command);

    if (!res.Item) {
      return jsonResponse(404, JSON.stringify({ error: "Item not found" }));
    }

    return jsonResponse(200, JSON.stringify(res.Item));
  } catch (error) {
    return jsonResponse(
      500,
      JSON.stringify({ error: "Internal Server Error" })
    );
  }
};
