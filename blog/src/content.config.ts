import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const articles = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/articles' }),
  schema: z.object({
    title: z.string(),
    date: z.string(),
    category: z.string().optional(),
    importance_score: z.number().optional(),
    products: z.array(z.string()).optional(),
    source_url: z.string().url().optional(),
    source_name: z.string().optional(),
    template_type: z.string().optional(),
    word_count: z.number().optional(),
    generated_at: z.string().optional(),
    generated_by: z.string().optional(),
  }),
});

export const collections = { articles };
