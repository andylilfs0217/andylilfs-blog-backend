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
  };

  return {
    statusCode,
    body,
    headers,
  };
}
