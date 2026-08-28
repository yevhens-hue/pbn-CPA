import React from 'react';
import { getPostBySlug } from '@/lib/posts';
import { notFound } from 'next/navigation';
import Link from 'next/link';
import DOMPurify from 'isomorphic-dompurify';
import * as motion from 'framer-motion/client';
import { ArrowLeft, Calendar, Clock, Share2, Bookmark, CheckCircle2 } from 'lucide-react';
import { clsx, type ClassValue } from 'clsx';
import { twMerge } from 'tailwind-merge';

function cn(...inputs: ClassValue[]) {
    return twMerge(clsx(inputs));
}

export const dynamic = 'force-dynamic';

interface PageProps {
    params: Promise<{ slug: string }>;
}

function renderMarkdown(text: string): string {
    let result = text
        .replace(/^### (.+)$/gm, '<h3 class="text-xl font-bold mt-8 mb-4 text-white">$1</h3>')
        .replace(/^## (.+)$/gm, '<h2 class="text-2xl font-bold mt-12 mb-6 border-l-4 border-blue-500 pl-4 text-white">$1</h2>')
        .replace(/^# (.+)$/gm, '<h1 class="text-3xl font-extrabold mb-8 text-white">$1</h1>')
        .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
        .replace(/\*(.+?)\*/g, '<em>$1</em>')
        .replace(/`(.+?)`/g, '<code class="bg-white/10 px-1.5 py-0.5 rounded text-blue-300 font-mono text-sm">$1</code>');

    // Process tables
    result = result.replace(/(\|[^\n]+\|\n)+/g, (match) => {
        const lines = match.trim().split('\n');
        const rows = lines.map((row, idx) => {
            if (row.trim().match(/^\|?[-:| ]+\|?$/)) return ''; // Skip separator
            const isHeader = idx === 0;
            const cells = row.split('|').filter(c => c.trim() || row.includes('|')).map(c => {
                const content = c.trim();
                if (isHeader) return `<th class="p-4 text-left font-bold text-white border-b border-white/10 bg-white/5">${content}</th>`;
                return `<td class="p-4 border-b border-white/5 text-gray-400">${content}</td>`;
            }).join('');
            return `<tr>${cells}</tr>`;
        }).filter(r => r).join('');
        return `<div class="overflow-x-auto my-8 rounded-2xl border border-white/10 bg-black/20"><table class="w-full border-collapse">${rows}</table></div>`;
    });

    // Process lists
    result = result.replace(/^- (.+)$/gm, '<li class="flex gap-3 mb-2 text-gray-400"><span class="text-blue-500 mt-1.5 h-1.5 w-1.5 rounded-full bg-blue-500 flex-shrink-0"></span><span>$1</span></li>');
    result = result.replace(/(<li[^>]*>[\s\S]*?<\/li>\n?)+/g, '<ul class="my-6 space-y-2">$0</ul>');

    // Process paragraphs
    result = result
        .split('\n\n').map(p => {
            const trimmed = p.trim();
            if (!trimmed) return '';
            if (trimmed.startsWith('<h') || trimmed.startsWith('<ul') || trimmed.startsWith('<div') || trimmed.startsWith('<table') || trimmed.startsWith('<li')) return trimmed;
            return `<p class="text-gray-400 leading-relaxed mb-6 text-lg">${trimmed}</p>`;
        }).filter(p => p).join('\n');

    return result;
}

export default async function BlogPostPage({ params }: PageProps) {
    const { slug } = await params;
    const post = await getPostBySlug(slug);

    if (!post) {
        notFound();
    }

    const contentHtml = DOMPurify.sanitize(renderMarkdown(post!.content));
    const wordCount = post!.content.split(/\s+/).length;
    const readingTime = Math.ceil(wordCount / 200);

    return (
        <div className="min-h-screen bg-[#0a0d1a] text-white">
            {/* Ambient Background */}
            <div className="fixed inset-0 pointer-events-none overflow-hidden">
                <div className="absolute top-[-10%] right-[-10%] w-[40%] h-[40%] bg-blue-600/10 rounded-full blur-[120px]" />
                <div className="absolute bottom-[-10%] left-[-10%] w-[40%] h-[40%] bg-purple-600/10 rounded-full blur-[120px]" />
            </div>

            <main className="relative z-10 py-20 px-4 sm:px-6 lg:px-8">
                <article className="max-w-4xl mx-auto">
                    {/* Navigation */}
                    <motion.div
                        initial={{ opacity: 0, x: -20 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ duration: 0.5 }}
                        className="mb-12"
                    >
                        <Link
                            href="/blog"
                            className="inline-flex items-center gap-2 text-gray-400 hover:text-white transition-all group"
                        >
                            <span className="p-2 rounded-full border border-white/5 group-hover:bg-white/5 transition-colors">
                                <ArrowLeft size={16} />
                            </span>
                            <span className="font-bold uppercase tracking-widest text-[10px]">Back to Insights</span>
                        </Link>
                    </motion.div>

                    {/* Hero Section */}
                    <header className="mb-16">
                        <motion.div
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ duration: 0.6 }}
                        >
                            <div className="flex items-center gap-3 mb-6">
                                <span className="bg-blue-500/10 border border-blue-500/20 text-blue-400 text-[10px] font-black uppercase tracking-[0.2em] px-3 py-1.5 rounded-full">
                                    Market Insight
                                </span>
                                <div className="h-px flex-1 bg-gradient-to-r from-blue-500/20 to-transparent" />
                            </div>

                            <h1 className="text-4xl sm:text-6xl md:text-7xl font-black mb-8 leading-[0.9] tracking-tighter text-white uppercase">
                                {post!.title}
                            </h1>

                            <div className="flex flex-wrap items-center gap-8 py-6 border-y border-white/5">
                                <div className="flex items-center gap-3">
                                    <div className="p-2 rounded-lg bg-white/5">
                                        <Calendar size={14} className="text-blue-400" />
                                    </div>
                                    <div className="flex flex-col">
                                        <span className="text-[9px] text-gray-500 font-bold uppercase tracking-widest">Published</span>
                                        <span className="text-xs font-black text-white uppercase tracking-tight">{post!.date}</span>
                                    </div>
                                </div>
                                <div className="flex items-center gap-3">
                                    <div className="p-2 rounded-lg bg-white/5">
                                        <Clock size={14} className="text-purple-400" />
                                    </div>
                                    <div className="flex flex-col">
                                        <span className="text-[9px] text-gray-500 font-bold uppercase tracking-widest">Reading Time</span>
                                        <span className="text-xs font-black text-white uppercase tracking-tight">{readingTime} MIN READ</span>
                                    </div>
                                </div>
                                <div className="flex-1" />
                                <div className="flex items-center gap-2">
                                    <button className="p-2.5 rounded-xl border border-white/5 bg-white/5 hover:bg-white/10 transition-colors text-gray-400 hover:text-white">
                                        <Share2 size={18} />
                                    </button>
                                    <button className="p-2.5 rounded-xl border border-white/5 bg-white/5 hover:bg-white/10 transition-colors text-gray-400 hover:text-white">
                                        <Bookmark size={18} />
                                    </button>
                                </div>
                            </div>
                        </motion.div>
                    </header>

                    {/* Content Section */}
                    <motion.div
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        transition={{ duration: 0.8, delay: 0.3 }}
                        className="relative"
                    >
                        <div
                            className="prose-content max-w-none"
                            dangerouslySetInnerHTML={{ __html: contentHtml }}
                        />
                    </motion.div>

                    {/* CTA Section */}
                    <motion.section
                        initial={{ opacity: 0, y: 40 }}
                        whileInView={{ opacity: 1, y: 0 }}
                        viewport={{ once: true }}
                        transition={{ duration: 0.7 }}
                        className="mt-32 relative overflow-hidden p-12 bg-gradient-to-br from-[#111] to-[#0a0a0a] border border-white/10 rounded-[2.5rem] text-center group"
                    >
                        <div className="absolute top-0 right-0 p-12 text-8xl opacity-[0.03] group-hover:scale-110 transition-transform duration-700 pointer-events-none">🎰</div>
                        <CheckCircle2 size={40} className="text-blue-500 mx-auto mb-8" />
                        <h2 className="text-4xl md:text-5xl font-black text-white mb-6 tracking-tighter uppercase leading-[0.9]">
                            Upgrade Your<br />Game Strategy
                        </h2>
                        <p className="text-gray-400 mb-10 max-w-xl mx-auto text-lg leading-relaxed">
                            Don't miss the best verified offers. Our real-time database tracks 30+ top brands with 6h refresh rate.
                        </p>
                        <div className="flex flex-col sm:flex-row gap-4 justify-center">
                            <Link
                                href="/all-bonuses"
                                className="bg-white text-black font-black px-12 py-5 rounded-2xl transition-all transform hover:scale-105 active:scale-95 shadow-2xl shadow-white/5 uppercase tracking-widest text-sm"
                            >
                                View Live Bonuses
                            </Link>
                            <Link
                                href="/"
                                className="bg-white/5 hover:bg-white/10 border border-white/20 text-white font-black px-12 py-5 rounded-2xl transition-all uppercase tracking-widest text-sm backdrop-blur-md"
                            >
                                Learn More
                            </Link>
                        </div>
                    </motion.section>

                    {/* Authorship / Disclaimer */}
                    <footer className="mt-24 pt-12 border-t border-white/5 flex flex-col items-center">
                        <div className="bg-white/2 border border-white/5 p-8 rounded-3xl max-w-2xl w-full">
                            <h4 className="text-white font-black uppercase tracking-widest text-xs mb-4">Editorial Transparency</h4>
                            <p className="text-gray-500 text-xs leading-relaxed italic">
                                This analysis is provided for informational purposes only. iGaming regulations vary by region (IN, TR, BR). 
                                Always ensure you are playing on licensed platforms. Games Income uses AI-assisted market research to provide 
                                granular insights into bonus structures and operator reputation.
                            </p>
                        </div>
                        <div className="mt-12 text-gray-700 text-[9px] uppercase tracking-[0.3em] font-black">
                            Games Income Insights Engine v2.6.4
                        </div>
                    </footer>
                </article>
            </main>
        </div>
    );
}
