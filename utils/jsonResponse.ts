import { APIGatewayProxyResult } from "aws-lambda";

export function jsonResponse(
  statusCode: number,
  body: string,
  headers?: {
    [header: string]: boolean | number | string;
  }
): APIGatewayProxyResult {
  headers = {
    ...headers,
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": "*", // This allows any origin
    "Access-Control-Allow-Credentials": true, // This allows cookies
  };

  return {
    statusCode,
    body,
    headers,
  };
}
