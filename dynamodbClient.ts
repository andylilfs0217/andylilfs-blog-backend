import { DynamoDBClient } from "@aws-sdk/client-dynamodb";
import { DynamoDBDocumentClient } from "@aws-sdk/lib-dynamodb";

const client = process.env.IS_OFFLINE
  ? new DynamoDBClient({
      region: "us-east-1",
      endpoint: "http://localhost:8000",
      credentials: {
        accessKeyId: "MockAccessKeyId",
        secretAccessKey: "MockSecretAccessKey",
      },
    })
  : new DynamoDBClient();

export const docClient: DynamoDBDocumentClient =
  DynamoDBDocumentClient.from(client);
