import { v4 as uuidv4 } from "uuid";

class BlogPost {
  id: string;
  title: string;
  content: string;
  author: Author;
  createdAt: string;
  updatedAt: string;
  coverImage: string;
  subtitle: string;

  constructor(
    title: string,
    content: string,
    author: Author,
    coverImage: string,
    subtitle: string
  );
  constructor(
    title: string,
    content: string,
    author: Author,
    coverImage: string,
    subtitle: string,
    id?: string
  );
  constructor(
    title: string,
    content: string,
    author: Author,
    coverImage: string,
    subtitle: string,
    id?: string,
    updatedAt?: string
  );
  constructor(
    title: string,
    content: string,
    author: Author,
    coverImage: string,
    subtitle: string,
    id?: string,
    updatedAt?: string,
    createdAt?: string
  ) {
    this.id = id || uuidv4();
    this.title = title;
    this.content = content;
    this.author = author;
    this.coverImage = coverImage;
    this.subtitle = subtitle;
    this.createdAt = createdAt || new Date().toISOString();
    this.updatedAt = updatedAt || new Date().toISOString();
  }
}

export { BlogPost };
