import React from 'react';
import { getAllPosts } from '@/lib/posts';
import Link from 'next/link';

export const dynamic = 'force-dynamic';

export default async function BlogPage() {
    const posts = await getAllPosts();

    return (
        <div className="min-h-screen bg-[#0a0a0a] text-white py-12 px-4 sm:px-6 lg:px-8">
            <div className="max-w-4xl mx-auto">
                <header className="mb-16 text-center">
                    <h1 className="text-5xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-indigo-500 mb-4 tracking-tighter uppercase">
                        iGaming Insights & Guides
                    </h1>
                    <p className="text-gray-400 text-lg">
                        The latest trends, bonus strategies, and market analysis for 2026.
                    </p>
                </header>

                {posts.length === 0 ? (
                    <div className="text-center py-20 border border-dashed border-gray-800 rounded-3xl">
                        <p className="text-gray-500 italic">Our AI analysts are currently writing new insights. Check back soon!</p>
                    </div>
                ) : (
                    <div className="space-y-8">
                        {posts.map((post) => (
                            <Link
                                key={post.slug}
                                href={`/blog/${post.slug}`}
                                className="block group"
                            >
                                <article className="bg-[#111] border border-gray-800 p-8 rounded-3xl hover:border-blue-500/50 transition-all duration-300 group-hover:bg-[#151515]">
                                    <div className="flex justify-between items-start mb-4">
                                        <span className="text-xs font-mono text-blue-400 uppercase tracking-widest bg-blue-500/10 px-3 py-1 rounded-full">
                                            {post.date}
                                        </span>
                                        <span className="text-gray-600 text-xs">
                                            5 min read
                                        </span>
                                    </div>
                                    <h2 className="text-2xl font-bold mb-4 group-hover:text-blue-400 transition-colors tracking-tight">
                                        {post.title}
                                    </h2>
                                    <p className="text-gray-400 line-clamp-2 leading-relaxed">
                                        {post.excerpt || "Expert analysis of the latest iGaming trends and bonus opportunities in the global market..."}
                                    </p>
                                    <div className="mt-6 flex items-center text-blue-400 font-semibold text-sm">
                                        Read Article <span className="ml-2 group-hover:translate-x-1 transition-transform">→</span>
                                    </div>
                                </article>
                            </Link>
                        ))}
                    </div>
                )}

                <footer className="mt-20 border-t border-gray-800 pt-12 flex flex-col items-center">
                    <Link href="/" className="text-gray-500 hover:text-white transition-colors">
                        ← Back to Home
                    </Link>
                </footer>
            </div>
        </div>
    );
}
