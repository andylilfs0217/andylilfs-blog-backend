import { v4 as uuidv4 } from "uuid";

class BlogPost {
  id: string;
  title: string;
  content: string;
  author: string;
  createdAt: string;
  updatedAt: string;

  constructor(title: string, content: string, author: string);
  constructor(title: string, content: string, author: string, id?: string);
  constructor(
    title: string,
    content: string,
    author: string,
    id?: string,
    updatedAt?: string
  );
  constructor(
    title: string,
    content: string,
    author: string,
    id?: string,
    updatedAt?: string,
    createdAt?: string
  ) {
    this.id = id || uuidv4();
    this.title = title;
    this.content = content;
    this.author = author;
    this.createdAt = createdAt || new Date().toISOString();
    this.updatedAt = updatedAt || new Date().toISOString();
  }

  publish(): void {
    // Logic to publish the blog post
    console.log(`"${this.title}" by ${this.author} has been published.`);
  }
}

export { BlogPost };
