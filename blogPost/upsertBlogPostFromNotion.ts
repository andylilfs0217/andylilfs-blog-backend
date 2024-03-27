import { PutCommand } from "@aws-sdk/lib-dynamodb";
import { docClient } from "../utils/dynamodbClient";
import { BlogPost } from "../models/blogPost";
import { APIGatewayProxyEvent, APIGatewayProxyResult } from "aws-lambda";
import { jsonResponse } from "../utils/jsonResponse";
import { Client } from "@notionhq/client";
import { NotionToMarkdown } from "notion-to-md";
import { getSecretString } from "../utils/secretManagerClient";

export const handler = async (
  event: APIGatewayProxyEvent
): Promise<APIGatewayProxyResult> => {
  try {
    const notionId = event.pathParameters?.id;
    if (!notionId) {
      return jsonResponse(400, JSON.stringify({ error: "ID is missing" }));
    }

    const secret_name = "prod/AndyBlog/Notion";

    const notionSecretString = await getSecretString(secret_name);
    const notionSecretJson = JSON.parse(notionSecretString);
    const notionSecret = notionSecretJson["notion_secret"];

    const notion = new Client({
      auth: notionSecret,
    });

    // passing notion client to the option
    const n2m = new NotionToMarkdown({ notionClient: notion });
    const notionPage = await notion.pages.retrieve({ page_id: notionId });
    const user = await notion.users.retrieve({
      user_id: notionPage["created_by"]["id"],
    });
    const mdblocks = await n2m.pageToMarkdown(notionId);
    const mdString = n2m.toMarkdownString(mdblocks);
    // Title
    const titleObjectList: { plain_text: string }[] =
      notionPage["properties"]?.Title?.title ?? [];
    const title = convertToTitlePlainText(titleObjectList);
    // Markdown Content
    const content = mdString.parent;
    // Author
    const author = {
      name: user.name ?? "Unknown",
      picture: user.avatar_url ?? "",
    };
    // Cover Image
    const coverImage = notionPage["cover"]?.external?.url ?? "";
    // Subtitle
    const subtitleObjectList: { plain_text: string }[] =
      notionPage["properties"]?.Subtitle?.rich_text ?? [];
    const subtitle = convertToSubtitlePlainText(subtitleObjectList);

    const blogPost = new BlogPost(
      title,
      content,
      author,
      coverImage,
      subtitle,
      notionId
    );

    const putCommand = new PutCommand({
      TableName: process.env.DYNAMODB_BLOG_POST_TABLE!,
      Item: blogPost,
    });
    await docClient.send(putCommand);

    return jsonResponse(204, JSON.stringify(blogPost));
  } catch (error) {
    return jsonResponse(500, JSON.stringify({ error: error.message }));
  }
};

function convertToTitlePlainText(titleObjectList: { plain_text: string }[]) {
  return titleObjectList.map((titleObject) => titleObject.plain_text).join("");
}

function convertToSubtitlePlainText(
  subtitleObjectList: { plain_text: string }[]
) {
  return subtitleObjectList
    .map((subtitleObject) => subtitleObject.plain_text)
    .join("");
}
