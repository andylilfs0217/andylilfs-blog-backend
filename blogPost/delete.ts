import { DeleteCommand } from "@aws-sdk/lib-dynamodb";
import { docClient } from "../dynamodbClient";
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

    const command = new DeleteCommand({
      TableName: process.env.DYNAMODB_BLOG_POST_TABLE!,
      Key: {
        id: id,
      },
    });
    await docClient.send(command);

    return jsonResponse(204, "");
  } catch (error) {
    return jsonResponse(
      500,
      JSON.stringify({ error: "Internal Server Error" })
    );
  }
};
