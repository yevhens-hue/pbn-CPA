import React from 'react';
import { getPostBySlug } from '@/lib/posts';
import { notFound } from 'next/navigation';
import Link from 'next/link';

export const dynamic = 'force-dynamic';

interface PageProps {
    params: Promise<{ slug: string }>;
}

function renderMarkdown(text: string): string {
    // Simple server-side markdown table and heading renderer
    return text
        .replace(/^### (.+)$/gm, '<h3 class="text-xl font-bold mt-8 mb-4 text-white">$1</h3>')
        .replace(/^## (.+)$/gm, '<h2 class="text-2xl font-bold mt-12 mb-6 border-l-4 border-blue-500 pl-4 text-white">$1</h2>')
        .replace(/^# (.+)$/gm, '<h1 class="text-3xl font-extrabold mb-8 text-white">$1</h1>')
        .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
        .replace(/\*(.+?)\*/g, '<em>$1</em>')
        .replace(/`(.+?)`/g, '<code class="bg-white/10 px-1 rounded text-blue-300">$1</code>')
        .replace(/^\| (.+) \|$/gm, (line) => {
            const cells = line.split('|').filter(c => c.trim()).map(c => `<td class="p-3 border-t border-gray-800 text-sm text-gray-300">${c.trim()}</td>`).join('');
            return `<tr>${cells}</tr>`;
        })
        .replace(/^- (.+)$/gm, '<li class="ml-4 mb-1 text-gray-300 list-disc">$1</li>')
        .replace(/^\n+/g, '')
        .split('\n\n').map(p => {
            if (p.startsWith('<h') || p.startsWith('<li') || p.startsWith('<tr')) return p;
            return `<p class="text-gray-300 leading-relaxed mb-6">${p}</p>`;
        }).join('\n');
}

export default async function BlogPostPage({ params }: PageProps) {
    const { slug } = await params;
    const post = await getPostBySlug(slug);

    if (!post) {
        notFound();
    }

    const contentHtml = renderMarkdown(post!.content);

    return (
        <div className="min-h-screen bg-[#0a0a0a] text-white py-12 px-4 sm:px-6 lg:px-8">
            <article className="max-w-3xl mx-auto">
                <header className="mb-12 border-b border-gray-800 pb-12">
                    <Link
                        href="/blog"
                        className="text-blue-400 hover:text-blue-300 mb-8 inline-block font-medium"
                    >
                        ← Back to Blog
                    </Link>
                    <h1 className="text-4xl sm:text-5xl font-extrabold mb-6 leading-tight tracking-tighter">
                        {post!.title}
                    </h1>
                    <div className="flex items-center gap-4 text-gray-500 text-sm font-mono uppercase tracking-widest">
                        <span>{post!.date}</span>
                        <span>•</span>
                        <span>Expert Insights</span>
                    </div>
                </header>

                <div
                    className="prose-content"
                    dangerouslySetInnerHTML={{ __html: contentHtml }}
                />

                <section className="mt-20 p-10 bg-gradient-to-br from-blue-900/20 to-indigo-900/20 border border-blue-500/30 rounded-3xl text-center">
                    <h2 className="text-2xl font-bold mb-4 tracking-tighter uppercase">Looking for the Best Bonuses?</h2>
                    <p className="text-gray-300 mb-8 max-w-lg mx-auto leading-relaxed">
                        Our database is updated every 6 hours with the latest casino and betting offers from vetted brands.
                    </p>
                    <Link
                        href="/all-bonuses"
                        className="inline-block bg-blue-500 hover:bg-blue-600 text-white font-bold py-4 px-10 rounded-full transition-all shadow-lg shadow-blue-500/30 uppercase tracking-widest text-sm"
                    >
                        View Full Bonus Table
                    </Link>
                </section>

                <footer className="mt-20 border-t border-gray-800 pt-12 text-center">
                    <div className="text-gray-600 text-xs mb-8 uppercase tracking-widest font-mono">
                        © 2026 games-income.com — All Rights Reserved
                    </div>
                </footer>
            </article>
        </div>
    );
}
