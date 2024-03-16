"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.docClient = void 0;
var client_dynamodb_1 = require("@aws-sdk/client-dynamodb");
var lib_dynamodb_1 = require("@aws-sdk/lib-dynamodb");
var client = process.env.IS_OFFLINE
    ? new client_dynamodb_1.DynamoDBClient({
        region: "us-east-1",
        endpoint: "http://localhost:8000",
        credentials: {
            accessKeyId: "MockAccessKeyId",
            secretAccessKey: "MockSecretAccessKey",
        },
    })
    : new client_dynamodb_1.DynamoDBClient();
exports.docClient = lib_dynamodb_1.DynamoDBDocumentClient.from(client);
//# sourceMappingURL=dynamodbClient.js.map