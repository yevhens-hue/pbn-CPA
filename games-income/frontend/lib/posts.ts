import fs from 'fs';
import path from 'path';

const postsDirectory = path.join(process.cwd(), 'data', 'blog');

export interface PostData {
  title: string;
  slug: string;
  content: string;
  date: string;
  excerpt?: string;
}

export async function getAllPosts(): Promise<PostData[]> {
  if (!fs.existsSync(postsDirectory)) {
    return [];
  }

  const fileNames = fs.readdirSync(postsDirectory);
  const allPostsData = fileNames
    .filter((fileName) => fileName.endsWith('.json'))
    .map((fileName) => {
      const fullPath = path.join(postsDirectory, fileName);
      const fileContents = fs.readFileSync(fullPath, 'utf8');
      const postData = JSON.parse(fileContents);
      
      return {
        ...postData,
        date: fileName.split('-').slice(0, 3).join('-'), // Use date from filename if missing
      };
    });

  // Sort posts by date
  return allPostsData.sort((a, b) => (a.date < b.date ? 1 : -1));
}

export async function getPostBySlug(slug: string): Promise<PostData | null> {
  const allPosts = await getAllPosts();
  return allPosts.find((post) => post.slug === slug) || null;
}
