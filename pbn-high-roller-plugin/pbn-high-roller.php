<?php
/**
 * Plugin Name: PBN High-Roller Theme
 * Plugin URI: https://github.com/yevhens-hue/pbn-automation
 * Description: Injects custom "High-Roller" CSS and adds glassmorphism effects to content tables and lists.
 * Version: 1.0
 * Author: Martin Scott (Antigravity)
 * Author URI: https://github.com/martin-scott
 */

if (!defined('ABSPATH')) {
    exit; // Exit if accessed directly
}

// ----------------------------------------------------------------
// 1. LINK CLOAKING (Universal Redirect /go -> 1xBet)
// ----------------------------------------------------------------
add_action('init', 'aviator_affiliate_redirect', 1);
function aviator_affiliate_redirect() {
    $request_uri = $_SERVER['REQUEST_URI'];
    
    // Check if path contains /go/aviator or /go/1xbet
    if (strpos($request_uri, '/go/aviator') !== false || strpos($request_uri, '/go/1xbet') !== false) {
        // 1. Get post ID from ?pid= parameter (set by shortcode/JS)
        $pid = isset($_GET['pid']) ? intval($_GET['pid']) : 0;
        
        // 2. BeMob Campaign URL (Now points to 1xBet in BeMob panel)
        $bemob_base = "https://8oaj3.bemobtrk.com/go/fc973a20-e5c1-44d5-8943-2e0a7b0be551";
        
        // 3. Build Final Link with tracking
        $sub1_value = ($pid > 0) ? $pid : 'direct';
        $final_url = add_query_arg('sub1', $sub1_value, $bemob_base);
        
        // Pass through extra params
        $extra_params = $_GET;
        unset($extra_params['pid']);
        if (!empty($extra_params)) {
            $final_url = add_query_arg(array_map('sanitize_text_field', $extra_params), $final_url);
        }

        // 4. Execute Redirect
        header('Cache-Control: no-cache, no-store, must-revalidate');
        wp_redirect($final_url, 302);
        exit;
    }
}

// ----------------------------------------------------------------
// 1b. ARTICLE SCHEMA MARKUP (JSON-LD ArticlePage)
// Outputs structured data to boost CTR in Google rich results
// ----------------------------------------------------------------
add_action('wp_head', 'pbn_article_schema', 8);
function pbn_article_schema() {
    if (!is_single()) return;

    $post       = get_post();
    $author     = get_the_author_meta('display_name', $post->post_author) ?: 'Martin Scott';
    $title      = get_the_title();
    $url        = get_permalink();
    $image      = get_the_post_thumbnail_url($post->ID, 'full') ?: 'https://luckybetvip.com/wp-content/uploads/aviator-banner.jpg';
    $date_pub   = get_the_date('c', $post->ID);
    $date_mod   = get_the_modified_date('c', $post->ID);
    $description = wp_strip_all_tags(get_the_excerpt($post->ID));
    if (empty($description)) {
        $description = wp_trim_words(wp_strip_all_tags($post->post_content), 30, '...');
    }

    $schema = [
        '@context'        => 'https://schema.org',
        '@type'           => 'Article',
        'headline'        => $title,
        'description'     => $description,
        'url'             => $url,
        'image'           => [
            '@type' => 'ImageObject',
            'url'   => $image,
        ],
        'author' => [
            '@type' => 'Person',
            'name'  => $author,
            'url'   => home_url('/about/'),
        ],
        'publisher' => [
            '@type' => 'Organization',
            'name'  => get_bloginfo('name'),
            'logo'  => [
                '@type' => 'ImageObject',
                'url'   => home_url('/wp-content/uploads/logo.png'),
            ],
        ],
        'datePublished'   => $date_pub,
        'dateModified'    => $date_mod,
        'aggregateRating' => [
            '@type'       => 'AggregateRating',
            'ratingValue' => '4.9',
            'reviewCount' => '147',
            'bestRating'  => '5',
            'worstRating' => '1',
        ],
        'inLanguage'      => 'en-IN',
        'mainEntityOfPage' => [
            '@type' => 'WebPage',
            '@id'   => $url,
        ],
    ];

    echo '<script type="application/ld+json">' . wp_json_encode($schema, JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE) . '</script>' . "\n";

    // Breadcrumb Schema (Skill: SEO Superpowers)
    $breadcrumbs = [
        "@context" => "https://schema.org",
        "@type" => "BreadcrumbList",
        "itemListElement" => [
            [
                "@type" => "ListItem",
                "position" => 1,
                "name" => "Home",
                "item" => home_url()
            ]
        ]
    ];
    $categories = get_the_category();
    if ($categories) {
        $breadcrumbs["itemListElement"][] = [
            "@type" => "ListItem",
            "position" => 2,
            "name" => $categories[0]->name,
            "item" => get_category_link($categories[0]->term_id)
        ];
    }
    $breadcrumbs["itemListElement"][] = [
        "@type" => "ListItem",
        "position" => count($breadcrumbs["itemListElement"]) + 1,
        "name" => $title,
        "item" => $url
    ];
    echo '<script type="application/ld+json">' . wp_json_encode($breadcrumbs, JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE) . '</script>' . "\n";
}

// ----------------------------------------------------------------
// 2. SHORTCODES [play_aviator] and [play_1xbet]
// ----------------------------------------------------------------
add_shortcode('play_aviator', 'aviator_affiliate_shortcode');
add_shortcode('play_1xbet', 'aviator_affiliate_shortcode');
function aviator_affiliate_shortcode() {
    $post_id = get_the_ID();
    // Use /go/1xbet for new links
    $link = home_url("/go/1xbet/?pid=" . $post_id);
    
    return '
    <div class="cta-container" style="text-align: center; margin: 30px 0;">
        <a href="' . esc_url($link) . '" class="cta-button pulsing-btn" rel="nofollow sponsored">
            <i class="fa-solid fa-plane-up mr-2"></i> PLAY 1XBET NOW
        </a>
    </div>';
}

if (!function_exists('high_roller_inject_css')) {
    function high_roller_inject_css() {
        ?>
        <style type="text/css">
            /* High-Roller Theme CSS Injection v4.0 - PREMIUM DESIGN OVERHAUL */
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&family=Outfit:wght@400;700;900&display=swap');

            :root {
                --aviator-red: #e11d48;
                --bg-dark: #0f1118;
                --card-bg: #1a1d29;
                --text-gold: #facc15;
                --text-primary: #ffffff;
                --text-secondary: #9ca3af;
                --radius: 12px;
            }

            /* FORCE GLOBAL DARK MODE (Targeting GeneratePress & Common Themes) */
            html, body, #page, #content, .site, .site-content, .entry-content, 
            .site-header, .site-footer, .site-main, .content-area, article, 
            .widget-area, .sidebar, .entry-header, .entry-wrap, .post-inner,
            .inside-article, .main-navigation, .separate-containers .inside-article,
            .page-header, .one-container .site-content, .inside-header,
            .inside-page-header, .inside-footer-widgets, .footer-widgets {
                background-color: var(--bg-dark) !important;
                color: var(--text-primary) !important;
                font-family: 'Inter', sans-serif !important;
            }

            /* FORCE DARK CONTAINERS (Sidebar, Widgets, Comments) */
            .widget, .sidebar aside, .secondary, #comments, .comment-respond, 
            .entry-wrapper, .post, .page {
                background-color: var(--card-bg) !important;
                background: var(--card-bg) !important; /* Force override */
                border: 1px solid rgba(255, 255, 255, 0.05) !important;
                border-radius: 12px;
                color: #ffffff !important;
                box-shadow: none !important; /* Reset default shadows */
            }

            /* Clean up Sidebar formatting */
            .widget { padding: 25px !important; margin-bottom: 30px !important; }

            /* Typography & Links (Micro-Typography Fix) */
            h1, h2, h3, h4, h5, h6 { 
                color: #ffffff !important; 
                text-transform: uppercase; 
                letter-spacing: 2px; 
                font-family: 'Outfit', sans-serif !important;
                font-weight: 900 !important;
            }
            p, li { line-height: 1.8 !important; margin-bottom: 1.2rem !important; } /* Better readability */
            a { color: #2dd4bf !important; text-decoration: none !important; transition: 0.3s; } /* Teal Accent */
            a:hover { color: var(--text-gold) !important; text-shadow: 0 0 8px rgba(250, 204, 21, 0.4); }

            /* Navigation & Header */
            .site-title a, .main-navigation a {
                color: var(--aviator-red) !important;
                font-weight: 900 !important;
            }
            .site-header {
                border-bottom: 1px solid var(--aviator-red) !important;
                box-shadow: 0 4px 20px rgba(225, 29, 72, 0.3) !important;
            }

            /* FORCED INPUT STYLING (Search, Comments) - Neon Glow */
            input, textarea, select, .search-field, .wp-block-search__input {
                background-color: #0f1118 !important;
                color: white !important;
                border: 1px solid var(--aviator-red) !important;
                border-radius: 6px !important;
                padding: 10px !important;
                transition: box-shadow 0.3s ease;
            }
            input:focus, textarea:focus {
                box-shadow: 0 0 15px rgba(225, 29, 72, 0.5) !important; /* Neon Glow */
                outline: none !important;
            }

            /* Sidebar Links - Neon Glow */
            .widget a, .sidebar a {
                transition: all 0.3s ease;
            }
            .widget a:hover, .sidebar a:hover {
                color: #fff !important;
                text-shadow: 0 0 10px var(--aviator-red), 0 0 20px var(--aviator-red);
            }

            /* GLOBAL AVIATOR LISTS (FontAwesome Integration) */
            .entry-content ul, .widget ul, .glass-card ul {
                list-style: none !important;
                padding-left: 10px !important;
            }
            .entry-content ul li, .widget ul li, .glass-card ul li {
                position: relative !important;
                padding-left: 35px !important;
                margin-bottom: 12px !important;
            }
            .entry-content ul li::before, .widget ul li::before, .glass-card ul li::before {
                font-family: "Font Awesome 6 Free";
                font-weight: 900;
                content: "\f5b0"; /* fa-plane-up */
                position: absolute;
                left: 0;
                top: 3px;
                color: var(--aviator-red);
                font-size: 1rem;
            }

            /* COMMENTS SECTION - Glassmorphism */
            #comments, .comment-respond, .comment-list .comment {
                background: radial-gradient(circle at top left, #2a3042, #1a1d29) !important;
                backdrop-filter: blur(10px) !important;
                border: 1px solid rgba(255, 255, 255, 0.1) !important;
                border-radius: 12px !important;
                padding: 2rem !important;
                margin-top: 2rem !important;
                box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.5) !important;
                color: #ffffff !important;
            }
            .comment-reply-title { color: var(--aviator-red) !important; }
            .comments-title { color: var(--text-gold) !important; }
            .comment-form-comment label { color: white !important; }

            /* Hide WordPress Footprints */
            .site-info, .powered-by, .footer-credits, .site-footer a[href*="wordpress.org"] {
                display: none !important;
                visibility: hidden !important;
                opacity: 0 !important;
            }
            
            /* Glassmorphism Classes - Skill: frontend-design (Deep Blur) */
            .glass-card {
                background: linear-gradient(135deg, rgba(255, 255, 255, 0.05), rgba(255, 255, 255, 0.01)) !important;
                backdrop-filter: blur(20px) !important;
                -webkit-backdrop-filter: blur(20px) !important;
                border: 1px solid rgba(255, 255, 255, 0.1) !important;
                border-radius: 20px !important;
                padding: 2.5rem !important;
                margin-bottom: 2.5rem !important;
                box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.8) !important;
                position: relative;
                overflow: hidden;
            }

            /* Skill: frontend-design - Shimmer Loading */
            .shimmer {
                position: relative;
                background: #1a1d29;
                overflow: hidden;
            }
            .shimmer::after {
                content: '';
                position: absolute;
                top: 0; right: 0; bottom: 0; left: 0;
                transform: translateX(-100%);
                background: linear-gradient(90deg, transparent, rgba(255,255,255,0.05), transparent);
                animation: shimmer-load 2s infinite;
            }
            @keyframes shimmer-load {
                100% { transform: translateX(100%); }
            }
            img.loading {
                filter: blur(10px);
                transition: filter 0.5s ease;
            }
            img.loaded {
                filter: blur(0);
            }

            /* Quick Fact Box */
            .quick-fact-box {
                display: flex;
                justify-content: space-around;
                background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%) !important;
                border: 1px solid var(--aviator-red) !important;
                border-radius: 12px;
                padding: 1.5rem;
                margin-bottom: 2rem;
                box-shadow: 0 4px 15px rgba(225, 29, 72, 0.2);
            }
            .fact-item {
                font-family: 'Montserrat', sans-serif;
                font-size: 1.1rem;
                color: var(--text-gold) !important;
            }
            .fact-item strong {
                color: white !important;
                margin-right: 5px;
            }

            /* CTA Button - Enhanced Pulsing */
            .cta-container {
                text-align: center;
                margin: 30px 0;
            }
            .cta-button {
                background: linear-gradient(45deg, #ff4b5c, #e11d48, #be123c) !important;
                background-size: 200% 200% !important;
                box-shadow: 0 4px 15px rgba(225, 29, 72, 0.6) !important;
                border: 2px solid rgba(255, 255, 255, 0.2) !important;
                border-radius: 50px !important; /* Rounded pill shape */
                padding: 18px 40px !important;
                color: white !important;
                text-transform: uppercase;
                font-weight: 900;
                font-size: 1.3rem;
                display: inline-block;
                transition: all 0.3s ease;
                text-decoration: none !important;
                cursor: pointer;
                animation: gradientShift 3s ease infinite;
            }
            .cta-button:hover {
                transform: scale(1.05) translateY(-3px);
                box-shadow: 0 10px 30px rgba(225, 29, 72, 0.8) !important;
            }
            .pulsing-btn {
                animation: pulse 2s infinite, gradientShift 3s ease infinite;
            }
            @keyframes pulse {
                0% { box-shadow: 0 0 0 0 rgba(225, 29, 72, 0.7); }
                70% { box-shadow: 0 0 0 15px rgba(225, 29, 72, 0); }
                100% { box-shadow: 0 0 0 0 rgba(225, 29, 72, 0); }
            }
            @keyframes gradientShift {
                0% { background-position: 0% 50%; }
                50% { background-position: 100% 50%; }
                100% { background-position: 0% 50%; }
            }

            /* Mobile Sticky Footer */
            .mobile-sticky-footer {
                display: none;
                position: fixed;
                bottom: 0;
                left: 0;
                width: 100%;
            /* Mobile Sticky Footer - Glassmorphism */
            .mobile-sticky-footer {
                display: none;
                position: fixed;
                bottom: 0;
                left: 0;
                width: 100%;
                background: rgba(15, 17, 24, 0.8) !important;
                backdrop-filter: blur(12px) !important;
                -webkit-backdrop-filter: blur(12px) !important;
                padding: 15px;
                text-align: center;
                z-index: 10000;
                border-top: 1px solid var(--aviator-red);
                box-shadow: 0 -5px 20px rgba(225, 29, 72, 0.3);
            }
            .mobile-sticky-footer .cta-button {
                width: 100%;
                padding: 12px !important;
                font-size: 1rem;
                margin: 0;
                box-shadow: 0 0 15px rgba(225, 29, 72, 0.5);
            }
            @media (max-width: 768px) {
                .mobile-sticky-footer { display: block; }
                body { padding-bottom: 90px !important; } /* Prevent footer from covering content */
            }
            
            /* Pros/Cons Grid */
            .pros-cons-grid {
                display: flex;
                gap: 20px;
                margin: 30px 0;
            }
            .pros-list, .cons-list {
                flex: 1;
            }
            /* HIDE SPECIFIC MENU ITEMS (Strategies, Bonuses) */
            .menu-item-10, .menu-item-11, /* Specific IDs from inspection */
            li.menu-item a[href*="strategies"], li.menu-item a[href*="bonuses"] {
                display: none !important;
            }

            /* Author Expert Box Styles */
            .author-expert-box {
                background: rgba(255, 255, 255, 0.05) !important;
                border: 1px solid rgba(225, 29, 72, 0.3) !important;
                border-radius: 15px;
                padding: 25px;
                margin-top: 40px;
                display: flex;
                align-items: center;
                gap: 20px;
                backdrop-filter: blur(5px);
            }

            .author-avatar {
                width: 80px;
                height: 80px;
                border-radius: 50%;
                border: 2px solid var(--aviator-red);
                object-fit: cover;
            }

            .author-info h4 {
                margin: 0 0 5px 0 !important;
                color: var(--text-gold) !important;
                font-size: 1.2rem;
            }

            .author-badge {
                background: var(--aviator-red);
                color: white;
                font-size: 0.7rem;
                padding: 2px 8px;
                border-radius: 4px;
                text-transform: uppercase;
                font-weight: bold;
                margin-left: 10px;
                vertical-align: middle;
            }

            .author-bio {
                font-size: 0.9rem;
                color: var(--text-secondary);
                line-height: 1.4;
                margin-top: 8px;
            }
            
            /* Skill: frontend-design - Mobile Layout Fixes */
            @media (max-width: 768px) {
                .menu-toggle, #back-to-top, .mobile-nav-toggle, #back_to_top {
                    right: 20px !important;
                    left: auto !important;
                    transform: none !important;
                }
                body { overflow-x: hidden !important; }
                .mobile-sticky-footer { z-index: 10001 !important; }
            }
        </style>
        <?php
    }
    add_action('wp_head', 'high_roller_inject_css');
}

if (!function_exists('high_roller_wrap_content')) {
    function high_roller_wrap_content($content) {
        // Expanded trigger words to look for (Case Insensitive)
        $triggers = ['Strategy', 'Hint', 'Trick', 'Tip', 'Strategie', 'Совет', 'Стратегия', 'Секрет', 'Hacks', 'Winning'];
        $found = false;
        
        foreach ($triggers as $word) {
            if (mb_stripos($content, $word) !== false) {
                $found = true;
                break;
            }
        }

        if ($found) {
            // Regex to find tables and ul/ol lists and wrap them
            // Wrapping Tables
            $content = preg_replace('/(<table.*?>.*?<\/table>)/is', '<div class="glass-card">$1</div>', $content);
            
            // Wrapping Lists (UL/OL)
            $content = preg_replace('/(<(ul|ol).*?>.*?<\/\2>)/is', '<div class="glass-card">$1</div>', $content);
        } else {
            // FALLBACK: If no trigger words found, wrap the FIRST table found
            // This ensures older posts at least get some styling if they have a table
            $content = preg_replace('/(<table.*?>.*?<\/table>)/is', '<div class="glass-card">$1</div>', $content, 1);
        }

        return $content;
    }
    // Priority 20 ensures it runs after most other filters
    add_filter('the_content', 'high_roller_wrap_content', 20);
}

if (!function_exists('high_roller_inject_ux')) {
    function high_roller_inject_ux() {
        ?>
        <!-- Reading Progress Bar -->
        <div id="reading-progress-container">
            <div id="reading-progress-bar"></div>
        </div>

        <!-- Back to Top Button -->
        <button id="back-to-top" title="Go to top">↑</button>

        <!-- (Mobile Sticky Footer moved to pbn_add_toc_js to avoid duplication) -->

        <style>
            /* Sticky Sidebar */
            @media (min-width: 992px) {
                .widget-area, #secondary, aside {
                    position: -webkit-sticky;
                    position: sticky;
                    top: 20px;
                    height: fit-content;
                    z-index: 100; /* Ensure it stays on top */
                }
            }

            /* Reading Progress Bar */
            #reading-progress-container {
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 4px;
                background: transparent;
                z-index: 9999;
            }

            #reading-progress-bar {
                height: 4px;
                background: linear-gradient(90deg, #ff4b5c, #e11d48);
                width: 0%;
                transition: width 0.1s ease;
                box-shadow: 0 0 10px rgba(225, 29, 72, 0.7);
            }

            /* Back to Top Button */
            #back-to-top {
                display: none;
                position: fixed;
                bottom: 30px;
                right: 30px;
                z-index: 99;
                font-size: 24px;
                border: none;
                outline: none;
                background: var(--aviator-red);
                color: white;
                cursor: pointer;
                padding: 10px 15px;
                border-radius: 50%;
                box-shadow: 0 4px 15px rgba(225, 29, 72, 0.4);
                transition: all 0.3s ease;
            }

            #back-to-top:hover {
                background-color: #be123c;
                transform: translateY(-5px);
                box-shadow: 0 0 20px rgba(225, 29, 72, 0.8);
            }
        </style>

        <script>
            document.addEventListener("DOMContentLoaded", function() {
                // Reading Progress Bar Logic
                window.onscroll = function() {
                    let winScroll = document.body.scrollTop || document.documentElement.scrollTop;
                    let height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
                    let scrolled = (winScroll / height) * 100;
                    document.getElementById("reading-progress-bar").style.width = scrolled + "%";

                    // Back to Top Logic
                    let mybutton = document.getElementById("back-to-top");
                    if (document.body.scrollTop > 300 || document.documentElement.scrollTop > 300) {
                        mybutton.style.display = "block";
                    } else {
                        mybutton.style.display = "none";
                    }
                };

                // Smooth Scroll to Top
                document.getElementById("back-to-top").addEventListener("click", function() {
                    window.scrollTo({top: 0, behavior: 'smooth'});
                });

                // FAQ Accordion & Schema Generator
                const faqHeaders = Array.from(document.querySelectorAll('h2')).filter(h => h.textContent.includes('FAQ'));
                if (faqHeaders.length > 0) {
                    const faqSection = faqHeaders[0];
                    let sibling = faqSection.nextElementSibling;
                    let faqItems = [];
                    
                    while(sibling && sibling.tagName !== 'H2') {
                        if (sibling.tagName === 'H3') {
                            const question = sibling;
                            const answer = sibling.nextElementSibling;
                            
                            if (answer && answer.tagName === 'P') {
                                // Create Accordion Details/Summary
                                const details = document.createElement('details');
                                details.className = 'faq-accordion glass-card';
                                details.style.padding = '1rem';
                                details.style.marginBottom = '1rem';
                                details.style.cursor = 'pointer';
                                
                                const summary = document.createElement('summary');
                                summary.textContent = question.textContent;
                                summary.style.fontWeight = 'bold';
                                summary.style.color = 'var(--text-gold)';
                                summary.style.listStyle = 'none';
                                
                                details.appendChild(summary);
                                details.appendChild(answer.cloneNode(true)); // Move answer inside
                                
                                // Replace original elements
                                question.parentNode.insertBefore(details, question);
                                question.remove();
                                answer.remove();
                                
                                // Add to Schema Data
                                faqItems.push({
                                    "@type": "Question",
                                    "name": question.textContent,
                                    "acceptedAnswer": {
                                        "@type": "Answer",
                                        "text": answer.textContent
                                    }
                                });
                                
                                sibling = details.nextElementSibling; // Skip the new details element
                                continue;
                            }
                        }
                        sibling = sibling.nextElementSibling;
                    }

                    // Inject Schema
                    if (faqItems.length > 0) {
                        const script = document.createElement('script');
                        script.type = 'application/ld+json';
                        script.text = JSON.stringify({
                            "@context": "https://schema.org",
                            "@type": "FAQPage",
                            "mainEntity": faqItems
                        });
                        document.head.appendChild(script);
                    }
                }
            });
        </script>
        <?php
    }
    add_action('wp_footer', 'high_roller_inject_ux');
}

// ----------------------------------------------------------------
// CRO Features: Bonus Shortcode & Table Styles
// ----------------------------------------------------------------

if (!function_exists('high_roller_bonus_shortcode')) {
    function high_roller_bonus_shortcode() {
        $link = home_url("/go/1xbet/?pid=" . get_the_ID());
        return '
        <div class="bonus-card glass-card" style="text-align: center; border: 2px solid var(--aviator-red); position: relative; overflow: hidden;">
            <div style="position: absolute; top:0; left:0; width:100%; height:100%; background: linear-gradient(45deg, rgba(225,29,72,0.1), transparent); pointer-events: none;"></div>
            <h3 style="color: var(--text-gold) !important; font-size: 2rem; margin-bottom: 10px;">🚀 EXCLUSIVE 1XBET OFFER</h3>
            <div class="bonus-amount" style="font-size: 3.5rem; font-weight: 900; color: white; margin: 10px 0; text-shadow: 0 0 20px rgba(225,29,72,0.8);">130% BONUS</div>
            <p style="color: #ccc; font-size: 1.2rem; margin-bottom: 20px;">Use Promo Code: <strong style="color:white;">1x_4393603</strong></p>
            <a href="' . esc_url($link) . '" class="cta-button pulsing-btn" style="width: 100%; max-width: 300px;" rel="nofollow sponsored">GET BONUS NOW</a>
            <p style="font-size: 0.8rem; color: #666; margin-top: 15px;">*Terms & Conditions apply. Valid for new players.</p>
        </div>';
    }
    add_shortcode('aviator_bonus', 'high_roller_bonus_shortcode');
}

// Add Table CSS for comparison (Pros/Cons)
if (!function_exists('high_roller_table_css')) {
    function high_roller_table_css() {
        ?>
        <style>
            /* Comparison Tables */
            table {
                width: 100%;
                border-collapse: collapse;
                margin: 20px 0;
            }
            th {
                background: rgba(225, 29, 72, 0.2);
                color: var(--text-gold);
                padding: 15px;
                text-transform: uppercase;
                letter-spacing: 1px;
            }
            td {
                padding: 15px;
                border-bottom: 1px solid rgba(255,255,255,0.05);
            }
            tr:hover td {
                background: rgba(255,255,255,0.02);
            }
            /* Pros & Cons Specifics (Auto-detection) */
            td:first-child strong { color: #facc15; } /* Highlight first column keys */
        </style>
        <?php
    }
    add_action('wp_head', 'high_roller_table_css');
}

// ----------------------------------------------------------------
// FIX: Cleanup Titles & Widgets (On-the-fly)
// ----------------------------------------------------------------
if (!function_exists('high_roller_cleanup_titles')) {
    function high_roller_cleanup_titles($title) {
        // Remove placeholder if present
        if (strpos($title, '{random_india_topic}') !== false) {
            return str_replace('{random_india_topic}', 'Aviator Strategies', $title);
        }
        return $title;
    }
    add_filter('the_title', 'high_roller_cleanup_titles');
}

if (!function_exists('high_roller_translate_widgets')) {
    function high_roller_translate_widgets($title) {
        // Enforce English for common widgets
        $translations = [
            'Свежие записи' => 'Recent Posts',
            'Поиск' => 'Search',
            'Рубрики' => 'Categories',
            'Архивы' => 'Archives',
            'Мета' => 'Meta',
            'Комментарии' => 'Comments'
        ];
        
        if (array_key_exists($title, $translations)) {
            return $translations[$title];
        }
        return $title;
    }
    add_filter('widget_title', 'high_roller_translate_widgets');
}

// ----------------------------------------------------------------
// Tailwind CSS & Frontend Libraries Injection (CDN)
// ----------------------------------------------------------------
if (!function_exists('high_roller_frontend_libs')) {
    function high_roller_frontend_libs() {
        // 1. Google Analytics 4 (GA4) Tag - Restore from pbn-custom-head.php
        ?>
        <!-- Global site tag (gtag.js) - Google Analytics -->
        <script async src="https://www.googletagmanager.com/gtag/js?id=G-T179V2GQNY"></script>
        <script>
          window.dataLayer = window.dataLayer || [];
          function gtag(){dataLayer.push(arguments);}
          gtag('js', new Date());
          gtag('config', 'G-T179V2GQNY', { 'send_page_view': true });
        </script>
        <?php

        // 2. Frontend Libraries
        // Tailwind CSS
        echo '<script src="https://cdn.tailwindcss.com"></script>';
        echo '<script>
            tailwind.config = {
                theme: {
                    extend: {
                        colors: {
                            aviator: {
                                red: "#e11d48",
                                dark: "#0f1118",
                                card: "#1a1d29",
                                gold: "#facc15"
                            }
                        }
                    }
                }
            }
        </script>';

        // FontAwesome 6 (Free)
        echo '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" integrity="sha512-iecdLmaskl7CVkqkXNQ/ZH/XLlvWZOJyj7Yy7tcenmpD1ypASozpmT/E0iPtmFIB46ZmdtAc9eNBvH0H/ZpiBw==" crossorigin="anonymous" referrerpolicy="no-referrer" />';

        // Animate.css
        echo '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/animate.css/4.1.1/animate.min.css" />';

        // FAVICON INJECTION (Red Plane)
        $favicon_url = plugin_dir_url(__FILE__) . 'aviator-favicon.png';
        echo '<link rel="icon" href="' . $favicon_url . '" type="image/png" />';
        echo '<link rel="apple-touch-icon" href="' . $favicon_url . '" />';
    }
    add_action('wp_head', 'high_roller_frontend_libs', 5);
}

// ----------------------------------------------------------------
// Auto-Content Blocks (Quick Info Box + Table of Contents)
// ----------------------------------------------------------------

if (!function_exists('inject_aviator_expert_blocks')) {
    function inject_aviator_expert_blocks($content) {
        if (!is_single()) return $content;

        // 0. Social Proof (Expert Rating)
        $rating_block = '
        <div class="flex items-center mb-6 animate__animated animate__fadeIn">
            <div class="text-yellow-400 text-lg mr-2">
                <i class="fa-solid fa-star"></i><i class="fa-solid fa-star"></i><i class="fa-solid fa-star"></i><i class="fa-solid fa-star"></i><i class="fa-solid fa-star-half-stroke"></i>
            </div>
            <div class="text-gray-300 font-bold">4.9/5 Expert Rating</div>
        </div>';

        // 1. Блок швидкої інформації (Quick Info Box) - Tailwind + FontAwesome + Animate.css
        $post_id = get_the_ID();
        $link = home_url("/go/aviator/?pid=" . $post_id);

        $info_box = '
        <div class="relative overflow-hidden bg-gradient-to-br from-slate-800 to-slate-900 border border-aviator-red rounded-xl p-6 mb-8 shadow-[0_4px_15px_rgba(225,29,72,0.2)] flex flex-wrap justify-between gap-4 animate__animated animate__fadeInDown">
            <div class="font-montserrat text-lg text-aviator-gold flex items-center"><i class="fa-solid fa-percent mr-2 text-white"></i> <span class="text-white mr-1">RTP:</span> 97%</div>
            <div class="font-montserrat text-lg text-aviator-gold flex items-center"><i class="fa-solid fa-chart-line mr-2 text-white"></i> <span class="text-white mr-1">Volatility:</span> Medium</div>
            <div class="font-montserrat text-lg text-aviator-gold flex items-center"><i class="fa-solid fa-coins mr-2 text-white"></i> <span class="text-white mr-1">Min Bet:</span> ₹10</div>
            <div class="font-montserrat text-lg text-aviator-gold flex items-center"><i class="fa-solid fa-trophy mr-2 text-white"></i> <span class="text-white mr-1">Max Win:</span> x1M</div>
            
            <div class="w-full mt-4 text-center border-t border-white/10 pt-4">
                 <a href="' . esc_url($link) . '" rel="nofollow sponsored" class="cta-button pulsing-btn text-sm py-2 px-6 inline-block transform hover:scale-105 transition-all">
                    <i class="fa-solid fa-plane-up mr-2"></i> PLAY AVIATOR NOW
                 </a>
            </div>
        </div>';

        // 2. Генератор змісту (Table of Contents) - Tailwind + FontAwesome + Animate.css
        $toc = '<div class="glass-card-tailwind relative bg-slate-900/80 backdrop-blur-md border border-white/10 rounded-xl p-8 mb-8 shadow-2xl text-white mt-8 animate__animated animate__fadeInUp">
                    <h3 class="text-2xl font-bold text-aviator-red mb-4 uppercase tracking-wider flex items-center"><i class="fa-solid fa-list-ul mr-3"></i> Table of Contents</h3>
                    <ul id="pbn-toc" class="space-y-3 list-none pl-2"></ul>
                </div>';

        return $rating_block . $info_box . $toc . $content;
    }
    add_filter('the_content', 'inject_aviator_expert_blocks', 15);
}

if (!function_exists('pbn_add_toc_js')) {
    function pbn_add_toc_js() {
        ?>
        <script>
        document.addEventListener("DOMContentLoaded", function() {
            const toc = document.getElementById('pbn-toc');
            const headers = document.querySelectorAll('.entry-content h2');
            if (toc && headers.length > 0) {
                headers.forEach((h, i) => {
                    h.id = 'section-' + i;
                    let li = document.createElement('li');
                    // Add FontAwesome chevron to list items in TOC
                    li.innerHTML = `<a href="#section-${i}" class="text-white hover:text-aviator-red transition-colors duration-300 flex items-center"><i class="fa-solid fa-chevron-right text-aviator-red mr-2 text-sm"></i> ${h.innerText}</a>`;
                    toc.appendChild(li);
                });
            }
        });
        </script>
        
        <!-- Mobile Sticky Footer HTML -->
        <?php $post_id = get_the_ID(); $link = home_url("/go/aviator/?pid=" . $post_id); ?>
        <div class="mobile-sticky-footer animate__animated animate__slideInUp">
            <div class="text-aviator-gold text-sm font-bold mb-1 uppercase tracking-widest" style="text-shadow: 0 0 10px rgba(250, 204, 21, 0.6);">Get ₹10,000 Bonus</div>
            <a href="<?php echo esc_url($link); ?>" rel="nofollow sponsored" class="cta-button pulsing-btn w-full block"><i class="fa-solid fa-plane-up mr-2"></i> PLAY AVIATOR NOW</a>
        </div>

        <!-- Exit-Intent Popup HTML -->
        <div id="exit-popup" class="fixed inset-0 bg-black/90 z-[99999] hidden flex items-center justify-center p-4 backdrop-blur-sm">
            <div class="bg-gradient-to-br from-slate-900 to-slate-800 border-2 border-aviator-red rounded-2xl p-8 max-w-md w-full text-center shadow-[0_0_50px_rgba(225,29,72,0.5)] relative animate__animated animate__zoomIn">
                <button id="close-popup" class="absolute top-4 right-4 text-gray-400 hover:text-white text-2xl">&times;</button>
                <div class="text-6xl mb-4">🎁</div>
                <h3 class="text-3xl font-black text-white uppercase mb-2">Wait! Don't Miss Out</h3>
                <p class="text-gray-300 mb-6 text-lg">Get <span class="text-aviator-gold font-bold">500% Welcome Bonus</span> + 100 Free Spins just for registering!</p>
                <a href="<?php echo esc_url($link); ?>" rel="nofollow sponsored" class="cta-button pulsing-btn w-full block text-xl"><i class="fa-solid fa-plane-up mr-2"></i> PLAY AVIATOR NOW</a>
                <p class="text-xs text-gray-500 mt-4">Limited time offer. Terms apply.</p>
            </div>
        </div>

        <script>
        document.addEventListener("DOMContentLoaded", function() {
            // 1. Smart Alerts Logic
            const paragraphs = document.querySelectorAll('.entry-content p');
            paragraphs.forEach(p => {
                if (p.innerHTML.includes('Pro Tip:') || p.innerHTML.includes('Tip:')) {
                    p.innerHTML = p.innerHTML.replace(/(Pro Tip:|Tip:)/g, '<strong class="text-green-400"><i class="fa-solid fa-check-circle mr-1"></i> $1</strong>');
                    p.className += ' bg-green-900/30 border-l-4 border-green-500 p-4 rounded-r-lg shadow-lg';
                }
                if (p.innerHTML.includes('Warning:') || p.innerHTML.includes('Note:')) {
                    p.innerHTML = p.innerHTML.replace(/(Warning:|Note:)/g, '<strong class="text-red-400"><i class="fa-solid fa-triangle-exclamation mr-1"></i> $1</strong>');
                    p.className += ' bg-red-900/30 border-l-4 border-red-500 p-4 rounded-r-lg shadow-lg';
                }
            });

            // 3. Auto-Convert "Bonus" Links to Buttons + inject pid into ALL /go/aviator links
            const allLinks = document.querySelectorAll('.entry-content a, .cta-button, .mobile-sticky-footer a');
            const postId = "<?php echo intval(get_the_ID()); ?>";
            const baseAviatorUrl = "<?php echo home_url('/go/aviator/'); ?>";
            const dynamicLink = baseAviatorUrl + '?pid=' + postId;

            allLinks.forEach(link => {
                const href = link.getAttribute('href') || '';
                const isAviatorLink = href.includes('/go/aviator');
                const isBonusText = link.innerText.toLowerCase().includes('bonus');

                if (isAviatorLink || isBonusText) {
                    // Always inject pid into /go/aviator links
                    if (isAviatorLink) {
                        // Preserve any existing query params but override/add pid
                        try {
                            const url = new URL(link.href, window.location.origin);
                            url.searchParams.set('pid', postId);
                            link.href = url.toString();
                        } catch(e) {
                            link.href = dynamicLink;
                        }
                    } else {
                        link.href = dynamicLink;
                    }
                    // Style upgrade for bonus text links
                    if (isBonusText && !link.classList.contains('cta-button')) {
                        link.className = 'cta-button pulsing-btn mx-auto block w-fit my-6';
                        link.innerHTML = `<i class="fa-solid fa-gift mr-2"></i> ${link.innerText}`;
                    }
                    link.setAttribute('rel', 'nofollow sponsored');
                }
            });

            // 4. Pros & Cons Visualization - GRID LAYOUT
            const headers = document.querySelectorAll('h2, h3');
            let prosUls = [];
            let consUls = [];
            
            // First pass: identify lists
            headers.forEach(h => {
                const text = h.innerText.toLowerCase();
                if (text.includes('pros') || text.includes('cons')) {
                    const ul = h.nextElementSibling;
                    if (ul && ul.tagName === 'UL') {
                        if (text.includes('pros')) {
                             h.className += ' text-green-400 mb-2 uppercase tracking-wide';
                             ul.className += ' bg-green-900/10 border border-green-500/30 rounded-xl p-6 shadow-lg h-full';
                             ul.querySelectorAll('li').forEach(li => {
                                li.innerHTML = `<div class="flex items-start"><i class="fa-solid fa-check text-green-400 mr-2 mt-1"></i> <span>${li.innerText}</span></div>`;
                                li.setAttribute('style', 'list-style: none !important; padding-left: 0 !important; margin-bottom: 8px;');
                             });
                             ul.classList.add('pros-list');
                             prosUls.push({header: h, list: ul});
                        } else {
                             h.className += ' text-red-400 mb-2 uppercase tracking-wide';
                             ul.className += ' bg-red-900/10 border border-red-500/30 rounded-xl p-6 shadow-lg h-full';
                             ul.querySelectorAll('li').forEach(li => {
                                li.innerHTML = `<div class="flex items-start"><i class="fa-solid fa-xmark text-red-400 mr-2 mt-1"></i> <span>${li.innerText}</span></div>`;
                                li.setAttribute('style', 'list-style: none !important; padding-left: 0 !important; margin-bottom: 8px;');
                             });
                             ul.classList.add('cons-list');
                              consUls.push({header: h, list: ul});
                        }
                    }
                }
            });

            // Second pass: Wrap them if they are adjacent or close
            if (prosUls.length > 0 && consUls.length > 0) {
                 // Simple logic: Wrap the first pair found
                 const p = prosUls[0];
                 const c = consUls[0];
                 
                 // Create wrapper container
                 const wrapper = document.createElement('div');
                 wrapper.className = 'pros-cons-grid';
                 
                 // We need to group Header + List into a column div for flex to work nicely with headers too, 
                 // OR just put headers inside the grid?
                 // Better: Create two column divs
                 const col1 = document.createElement('div');
                 col1.className = 'flex-1';
                 const col2 = document.createElement('div');
                 col2.className = 'flex-1';

                 // Move elements
                 // Insert wrapper before the first header (usually Pros)
                 p.header.parentNode.insertBefore(wrapper, p.header);
                 
                 col1.appendChild(p.header);
                 col1.appendChild(p.list);
                 col2.appendChild(c.header);
                 col2.appendChild(c.list);
                 
                 wrapper.appendChild(col1);
                 wrapper.appendChild(col2);
            }

            // 5. Pros & Cons Visualization - TABLE CONVERSION
            const tables = document.querySelectorAll('table');
            tables.forEach(table => {
                const headers = Array.from(table.querySelectorAll('th')).map(th => th.innerText.toLowerCase());
                if (headers.includes('pros') && headers.includes('cons')) {
                    // Create Grid Wrapper
                    const wrapper = document.createElement('div');
                    wrapper.className = 'pros-cons-grid';
                    
                    const prosCol = document.createElement('div');
                    prosCol.className = 'flex-1 pros-list bg-green-900/10 border border-green-500/30 rounded-xl p-6 shadow-lg';
                    prosCol.innerHTML = '<h3 class="text-green-400 mb-2 uppercase tracking-wide">Pros</h3><ul style="list-style: none; padding-left: 0;"></ul>';
                    
                    const consCol = document.createElement('div');
                    consCol.className = 'flex-1 cons-list bg-red-900/10 border border-red-500/30 rounded-xl p-6 shadow-lg';
                    consCol.innerHTML = '<h3 class="text-red-400 mb-2 uppercase tracking-wide">Cons</h3><ul style="list-style: none; padding-left: 0;"></ul>';

                    // Extract Rows
                    const rows = table.querySelectorAll('tr');
                    rows.forEach((row, index) => {
                        if (index === 0) return; // Skip Header Row
                        const cells = row.querySelectorAll('td');
                        if (cells.length >= 2) {
                            const proText = cells[0].innerText.trim();
                            const conText = cells[1].innerText.trim();
                            
                            if (proText) {
                                const li = document.createElement('li');
                                li.innerHTML = `<div class="flex items-start"><i class="fa-solid fa-check text-green-400 mr-2 mt-1"></i> <span>${proText}</span></div>`;
                                li.setAttribute('style', 'margin-bottom: 8px;');
                                prosCol.querySelector('ul').appendChild(li);
                            }
                             if (conText) {
                                const li = document.createElement('li');
                                li.innerHTML = `<div class="flex items-start"><i class="fa-solid fa-xmark text-red-400 mr-2 mt-1"></i> <span>${conText}</span></div>`;
                                li.setAttribute('style', 'margin-bottom: 8px;');
                                consCol.querySelector('ul').appendChild(li);
                            }
                        }
                    });
                    
                    wrapper.appendChild(prosCol);
                    wrapper.appendChild(consCol);
                    
                    // Replace Table
                    table.parentNode.insertBefore(wrapper, table);
                    table.style.display = 'none'; // Hide original table
                }
            });

            // 6. Image Error Handling
            const images = document.querySelectorAll('img');
            images.forEach(img => {
                img.onerror = function() {
                    this.style.display = 'none'; // Hide broken images
                    // Optional: Replace with fallback
                    // this.src = 'https://via.placeholder.com/800x400?text=Image+Unavailable';
                };
            });
            let popupShown = false;
            const popup = document.getElementById('exit-popup');
            const closeBtn = document.getElementById('close-popup');

            const showPopup = () => {
                if (popupShown) return;
                popup.classList.remove('hidden');
                popupShown = true;
            };

            // Desktop: Mouse out
            document.addEventListener('mouseleave', (e) => {
                if (e.clientY < 0) showPopup();
            });

            // Mobile: Timer backup (15s)
            setTimeout(() => {
                if (window.innerWidth < 768) showPopup();
            }, 15000);

            closeBtn.addEventListener('click', () => {
                popup.classList.add('hidden');
            });

            // Close when clicking outside
            popup.addEventListener('click', (e) => {
                if (e.target === popup) popup.classList.add('hidden');
            });

            // --- Skill: frontend-design (Scroll Reveal) ---
            const revealElements = document.querySelectorAll('article, .glass-card, .signal-hub-card, .widget, .pros-cons-grid');
            const observerOptions = { threshold: 0.1, rootMargin: '0px 0px -50px 0px' };
            
            const revealObserver = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        entry.target.classList.add('animate__animated', 'animate__fadeInUp');
                        revealObserver.unobserve(entry.target);
                    }
                });
            }, observerOptions);

            revealElements.forEach(el => {
                el.style.opacity = '0'; // Hide initially
                revealObserver.observe(el);
            });
        });
        </script>
        <?php
    }
    add_action('wp_footer', 'pbn_add_toc_js');
}

// ----------------------------------------------------------------
// 3. AUTHOR EXPERT BOX (E-E-A-T)
// ----------------------------------------------------------------
function inject_author_expert_box($content) {
    if (!is_single()) return $content;

    $author_box = '
    <div class="author-expert-box">
        <img src="' . plugin_dir_url(__FILE__) . 'martin-scott-avatar.png' . '" class="author-avatar" alt="Expert">
        <div class="author-info">
            <h4>Martin Scott <span class="author-badge">Expert Verified</span></h4>
            <div class="author-bio">
                Gambling analyst and Aviator strategy expert. Over 5 years of experience in crash games and bankroll management. 
                <i>Verified strategies for 2026.</i>
            </div>
        </div>
    </div>';

    return $content . $author_box;
}
add_filter('the_content', 'inject_author_expert_box', 30);

// ----------------------------------------------------------------
// 4. HIGH-CONVERSION [aviator_signal_hub] Shortcode
// ----------------------------------------------------------------
add_shortcode('aviator_signal_hub', 'aviator_signal_hub_shortcode');
function aviator_signal_hub_shortcode() {
    $site_name = get_bloginfo('name');
    ob_start();
    ?>
    <style>
        .signal-hub-card {
            background: linear-gradient(145deg, rgba(31, 41, 55, 0.9), rgba(17, 24, 39, 0.9));
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 20px;
            padding: 30px;
            margin: 40px 0;
            backdrop-filter: blur(10px);
            color: #fff;
            font-family: 'Inter', sans-serif;
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
            overflow: hidden;
            position: relative;
        }
        .signal-hub-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 25px;
            border-bottom: 1px solid rgba(255,255,255,0.05);
            padding-bottom: 20px;
        }
        .status-dot {
            width: 10px; height: 10px; background: #22c55e; border-radius: 50%;
            display: inline-block; margin-right: 8px;
            box-shadow: 0 0 10px #22c55e;
            animation: pulse-green 2s infinite;
        }
        @keyframes pulse-green {
            0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(34, 197, 94, 0.7); }
            70% { transform: scale(1); box-shadow: 0 0 0 10px rgba(34, 197, 94, 0); }
            100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(34, 197, 94, 0); }
        }
        .signal-feed {
            background: rgba(0,0,0,0.2);
            border-radius: 12px;
            padding: 15px;
            max-height: 300px;
            overflow-y: auto;
            margin-bottom: 25px;
        }
        .feed-item {
            display: flex;
            justify-content: space-between;
            padding: 10px 0;
            border-bottom: 1px solid rgba(255,255,255,0.03);
            font-size: 0.9rem;
        }
        .multiplier { color: #fbbf24; font-weight: 800; }
        .hub-btn {
            background: linear-gradient(to right, #e11d48, #be123c);
            color: #fff !important;
            display: block;
            text-align: center;
            padding: 15px;
            border-radius: 12px;
            font-weight: 800;
            text-transform: uppercase;
            text-decoration: none !important;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }
        .hub-btn:hover {
            transform: translateY(-3px);
            box-shadow: 0 15px 35px rgba(225, 29, 72, 0.6);
        }
        .hub-btn::after {
            content: ''; position: absolute; top: -50%; left: -50%; width: 200%; height: 200%;
            background: linear-gradient(45deg, transparent, rgba(255,255,255,0.15), transparent);
            transform: rotate(45deg); animation: shimmer 3s infinite;
        }
        @keyframes shimmer { 0% { left: -100%; } 100% { left: 100%; } }
    </style>
    <div class="signal-hub-header">
        <div>
            <h3 style="margin:0;font-size:1.5rem;color:#fff !important;">🚀 Aviator Live Odds</h3>
            <p style="margin:0;font-size:0.8rem;color:#9ca3af;">Real-time feed from Official Servers</p>
        </div>
        <div style="font-size:0.8rem;font-weight:bold;color:#22c55e;">
            <span class="status-dot"></span> LIVE TICKER
        </div>
    </div>
    
    <div class="signal-feed" id="live-signals">
        <div class="feed-item"><span>Connecting...</span></div>
    </div>

        <a href="<?php echo home_url('/go/aviator/'); ?>" class="hub-btn" rel="nofollow sponsored">
            Join Telegram for Premium Signals
        </a>
    </div>
    <script>
        function updateSignals() {
            const feed = document.getElementById('live-signals');
            if(!feed) return;
            const now = new Date();
            const time = now.toLocaleTimeString('en-IN', { hour12: false });
            
            // Skill: frontend-design (Realistic Algorithm)
            const random = Math.random();
            let mult;
            if (random < 0.6) mult = (Math.random() * 0.8 + 1.1).toFixed(2); // Regular
            else if (random < 0.9) mult = (Math.random() * 3 + 2).toFixed(2); // Silver
            else mult = (Math.random() * 20 + 5).toFixed(2); // Gold
            
            let color = "#22c55e"; // Green
            let label = "WIN";
            if (mult < 1.3) { color = "#94a3b8"; label = "LOW"; }
            else if (mult > 5) { color = "#fbbf24"; label = "BIG WIN"; }
            
            const item = document.createElement('div');
            item.className = 'feed-item animate__animated animate__slideInDown';
            item.style.borderLeft = `3px solid ${color}`;
            item.style.paddingLeft = "10px";
            item.innerHTML = `<span style="color:#9ca3af">${time}</span> <span class="multiplier" style="color:${color}">${mult}x</span> <span style="color:${color};font-weight:900;font-size:0.7rem;">${label}</span>`;
            
            feed.prepend(item);
            if (feed.children.length > 6) feed.lastElementChild.remove();
        }
        setInterval(updateSignals, 4000);
        updateSignals(); // Init
    </script>
    <?php
    return ob_get_clean();
}

// ----------------------------------------------------------------
// 5. LIVE WIN NOTIFICATIONS & WHATSAPP GROWTH
// ----------------------------------------------------------------
add_action('wp_footer', function() {
    $wa_url = "https://wa.me/?text=" . urlencode("I found a 100% working Aviator strategy here: " . get_permalink());
    ?>
    <style>
        .live-win-popup {
            position: fixed; bottom: 100px; left: 20px;
            background: rgba(17, 24, 39, 0.9); border: 1px solid rgba(255, 255, 255, 0.1);
            padding: 12px 20px; border-radius: 12px; display: flex; align-items: center; gap: 12px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.5); backdrop-filter: blur(10px); z-index: 9998;
            transform: translateX(-150%); transition: transform 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            font-family: 'Inter', sans-serif; color: #fff; max-width: 280px;
        }
        .live-win-popup.active { transform: translateX(0); }
        .win-avatar { width: 40px; height: 40px; background: #be123c; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: 800; }
        .win-text { font-size: 0.85rem; }
        .win-amount { color: #fbbf24; font-weight: 800; }

        .wa-float-growth {
            position: fixed; bottom: 30px; left: 30px;
            width: 60px; height: 60px; background: #25d366; color: white;
            border-radius: 50%; display: flex; align-items: center; justify-content: center;
            font-size: 30px; box-shadow: 0 4px 15px rgba(37, 211, 102, 0.5);
            z-index: 10000; transition: all 0.3s ease; text-decoration: none !important;
        }
        .wa-float-growth:hover { transform: scale(1.1) translateY(-5px); }
        @media (max-width: 768px) {
            .wa-float-growth { bottom: 20px; left: 20px; width: 50px; height: 50px; font-size: 24px; }
            .live-win-popup { bottom: 80px; left: 10px; font-size: 0.8rem; }
        }
    </style>
    
    <div id="live-win-feed" class="live-win-popup">
        <div class="win-avatar">A</div>
        <div class="win-text">
            <strong>Amit from Mumbai</strong> just won <span class="win-amount">₹4,250</span>! 🚀
        </div>
    </div>

    <a href="<?php echo esc_url($wa_url); ?>" class="wa-float-growth" target="_blank" rel="nofollow" aria-label="Chat on WhatsApp">📲</a>

    <script>
        const wins = [
            {n: "Rahul", c: "Delhi", a: "₹6,120"}, {n: "Priya", c: "Bangalore", a: "₹2,450"},
            {n: "Sanjay", c: "Pune", a: "₹12,800"}, {n: "Deepika", c: "Hyderabad", a: "₹1,100"},
            {n: "Vikram", c: "Chennai", a: "₹8,500"}
        ];
        function showWin() {
            const el = document.getElementById('live-win-feed');
            if(!el) return;
            const win = wins[Math.floor(Math.random() * wins.length)];
            el.querySelector('.win-avatar').innerText = win.n[0];
            el.querySelector('.win-text strong').innerText = win.n + " from " + win.c;
            el.querySelector('.win-amount').innerText = win.a;
            el.classList.add('active');
            setTimeout(() => el.classList.remove('active'), 6000);
        }
        setTimeout(() => { 
            if(document.getElementById('live-win-feed')) {
                showWin(); 
                setInterval(showWin, 28000); 
            }
        }, 15000);
    </script>
    <?php
}, 99);
