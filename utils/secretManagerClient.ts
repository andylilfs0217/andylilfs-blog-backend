import {
  GetSecretValueCommand,
  SecretsManagerClient,
} from "@aws-sdk/client-secrets-manager";

export const secretsManagerClient = new SecretsManagerClient();

export const getSecretString = async (secret_name: string) => {
  let secretResponse;

  try {
    secretResponse = await secretsManagerClient.send(
      new GetSecretValueCommand({
        SecretId: secret_name,
      })
    );
  } catch (error) {
    throw error;
  }

  const secretString = secretResponse.SecretString;
  return secretString;
};
