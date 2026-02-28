<?php
// Google Search Console Verification
add_action('wp_head', function() {
    echo '<meta name="google-site-verification" content="oe4pPP27pwEyKhJf74HvgETrQBAu9zUKZtcdjn7v8S4" />' . "\n";
});

/**
 * High-Roller Theme Integration
 * Copy this content into your active theme's functions.php
 */

if (!function_exists('inject_high_roller_css')) {
    function inject_high_roller_css() {
        ?>
        <style type="text/css">
            /* High-Roller Theme CSS Injection */
            :root {
                --aviator-red: #e11d48;
                --bg-dark: #0f1118;
                --card-bg: #1a1d29;
                --text-gold: #facc15;
                --text-primary: #ffffff;
                --text-secondary: #9ca3af;
                --radius: 12px;
            }

            body {
                background-color: var(--bg-dark) !important;
                color: var(--text-primary) !important;
                font-family: 'Inter', 'Montserrat', sans-serif !important;
            }

            /* Article Container */
            .article-container, .entry-content {
                max-width: 900px;
                margin: 0 auto;
                padding: 2rem;
            }

            /* Glassmorphism Effect */
            .glass-card {
                background: rgba(26, 29, 41, 0.7);
                backdrop-filter: blur(10px);
                -webkit-backdrop-filter: blur(10px);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: var(--radius);
                padding: 2rem;
                margin-bottom: 2rem;
                box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
            }

            /* Quick Fact Box */
            .quick-fact-box {
                display: flex;
                justify-content: space-around;
                background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
                border: 1px solid var(--aviator-red);
                border-radius: var(--radius);
                padding: 1.5rem;
                margin-bottom: 2rem;
                box-shadow: 0 4px 15px rgba(225, 29, 72, 0.2);
            }

            .fact-item {
                font-family: 'Montserrat', sans-serif;
                font-size: 1.1rem;
                color: var(--text-gold);
            }

            .fact-item strong {
                color: white;
                margin-right: 5px;
            }

            /* CTA Button */
            .cta-container {
                text-align: center;
                margin: 30px 0;
            }

            .cta-button {
                background: linear-gradient(180deg, #ff4b5c 0%, #e11d48 100%);
                box-shadow: 0 4px 15px rgba(225, 29, 72, 0.4);
                border-radius: 8px;
                padding: 15px 30px;
                color: white !important;
                text-transform: uppercase;
                font-weight: 800;
                font-size: 1.2rem;
                display: inline-block;
                transition: all 0.2s ease;
                text-decoration: none;
                border: none;
                cursor: pointer;
            }

            .cta-button:hover {
                transform: scale(1.05) translateY(-2px);
                box-shadow: 0 0 25px rgba(225, 29, 72, 0.6);
            }

            /* Pulsing Animation */
            .pulsing-btn {
                animation: pulse 2s infinite;
            }

            @keyframes pulse {
                0% { box-shadow: 0 0 0 0 rgba(225, 29, 72, 0.7); }
                70% { box-shadow: 0 0 0 10px rgba(225, 29, 72, 0); }
                100% { box-shadow: 0 0 0 0 rgba(225, 29, 72, 0); }
            }
        </style>
        <?php
    }
    add_action('wp_head', 'inject_high_roller_css');
}

if (!function_exists('wrap_content_glass_card')) {
    function wrap_content_glass_card($content) {
        // Trigger words to look for
        $triggers = ['Strategy', 'Hint', 'Strategie', 'Tip', 'Trick', 'Секрет', 'Стратегия'];
        $found = false;
        
        foreach ($triggers as $word) {
            if (stripos($content, $word) !== false) {
                $found = true;
                break;
            }
        }

        if ($found) {
            // Regex to find tables and ul/ol lists and wrap them
            // Wrapping Tables
            $content = preg_replace('/(<table.*?>.*?<\/table>)/is', '<div class="glass-card">$1</div>', $content);
            
            // Wrapping Lists (UL/OL) - treating consecutive lists? 
            // Simple replacement for any list not already inside a glass-card (hard to check with regex alone, doing simple replace)
            $content = preg_replace('/(<(ul|ol).*?>.*?<\/\2>)/is', '<div class="glass-card">$1</div>', $content);
        }

        return $content;
    }
    add_filter('the_content', 'wrap_content_glass_card');
}


// ================================================================
// ON-SITE SEO ENHANCEMENTS v2.0
// ================================================================

// 1. Remove clutter from <head> (WordPress garbage)
if (!function_exists('pbn_clean_head')) {
    function pbn_clean_head() {
        remove_action('wp_head', 'wp_generator');              // Remove WP version
        remove_action('wp_head', 'wlwmanifest_link');          // Remove Windows Live Writer
        remove_action('wp_head', 'rsd_link');                  // Remove RSD link
        remove_action('wp_head', 'wp_shortlink_wp_head');      // Remove shortlink
        remove_action('wp_head', 'adjacent_posts_rel_link_wp_head', 10);
    }
    add_action('init', 'pbn_clean_head');
}

// 2. Canonical URL for every page
if (!function_exists('pbn_add_canonical')) {
    function pbn_add_canonical() {
        if (is_singular()) {
            echo '<link rel="canonical" href="' . esc_url(get_permalink()) . '">' . "\n";
        }
    }
    add_action('wp_head', 'pbn_add_canonical', 1);
}

// 3. Open Graph Meta Tags (Facebook, Telegram, WhatsApp previews)
if (!function_exists('pbn_open_graph')) {
    function pbn_open_graph() {
        global $post;
        if (!is_singular()) return;

        $title = esc_attr(get_the_title());
        $url   = esc_url(get_permalink());
        $desc  = esc_attr(wp_trim_words(get_the_excerpt(), 20, '...'));
        $image = get_the_post_thumbnail_url($post->ID, 'large');
        if (!$image) $image = 'https://luckybetvip.com/wp-content/uploads/og-default.jpg';

        echo '<meta property="og:type" content="article">' . "\n";
        echo '<meta property="og:title" content="' . $title . '">' . "\n";
        echo '<meta property="og:description" content="' . $desc . '">' . "\n";
        echo '<meta property="og:url" content="' . $url . '">' . "\n";
        echo '<meta property="og:image" content="' . esc_url($image) . '">' . "\n";
        echo '<meta property="og:site_name" content="LuckyBet VIP">' . "\n";
        echo '<meta name="twitter:card" content="summary_large_image">' . "\n";
        echo '<meta name="twitter:title" content="' . $title . '">' . "\n";
        echo '<meta name="twitter:image" content="' . esc_url($image) . '">' . "\n";

        // hreflang for India
        echo '<link rel="alternate" hreflang="en-IN" href="' . $url . '">' . "\n";
        echo '<link rel="alternate" hreflang="x-default" href="' . $url . '">' . "\n";
    }
    add_action('wp_head', 'pbn_open_graph');
}

// 4. Breadcrumbs with JSON-LD Schema (BreadcrumbList)
if (!function_exists('pbn_breadcrumbs')) {
    function pbn_breadcrumbs() {
        if (!is_singular()) return;
        global $post;

        $home_url  = get_home_url();
        $post_url  = get_permalink();
        $post_name = get_the_title();

        // Get category
        $categories = get_the_category($post->ID);
        $cat_name = $categories ? $categories[0]->name : 'Blog';
        $cat_url  = $categories ? get_category_link($categories[0]->term_id) : $home_url;

        $schema = json_encode([
            '@context' => 'https://schema.org',
            '@type'    => 'BreadcrumbList',
            'itemListElement' => [
                ['@type' => 'ListItem', 'position' => 1, 'name' => 'Home',    'item' => $home_url],
                ['@type' => 'ListItem', 'position' => 2, 'name' => $cat_name, 'item' => $cat_url],
                ['@type' => 'ListItem', 'position' => 3, 'name' => $post_name,'item' => $post_url],
            ]
        ], JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE);

        echo '<script type="application/ld+json">' . $schema . '</script>' . "\n";
    }
    add_action('wp_head', 'pbn_breadcrumbs');
}

// 5. Lazy loading for all images (native HTML attribute)
if (!function_exists('pbn_lazy_load_images')) {
    function pbn_lazy_load_images($content) {
        return str_replace('<img ', '<img loading="lazy" ', $content);
    }
    add_filter('the_content', 'pbn_lazy_load_images');
}

// 6. Add Google Fonts (Inter) for performance and modern typography
if (!function_exists('pbn_enqueue_fonts')) {
    function pbn_enqueue_fonts() {
        wp_enqueue_style('pbn-fonts',
            'https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap',
            [], null
        );
    }
    add_action('wp_enqueue_scripts', 'pbn_enqueue_fonts');
}

// 7. Social Sharing Buttons (WhatsApp, Telegram, Facebook, Twitter)
if (!function_exists('pbn_social_share_buttons')) {
    function pbn_social_share_buttons($content) {
        if (!is_single()) return $content;
        $url   = urlencode(get_permalink());
        $title = urlencode(get_the_title());
        $wa  = "https://wa.me/?text={$title}%20{$url}";
        $tg  = "https://t.me/share/url?url={$url}&text={$title}";
        $fb  = "https://www.facebook.com/sharer/sharer.php?u={$url}";
        $tw  = "https://twitter.com/intent/tweet?url={$url}&text={$title}";
        $html = '<div class="social-share-bar" style="display:flex;gap:10px;flex-wrap:wrap;justify-content:center;background:rgba(26,29,41,0.8);border-radius:12px;padding:20px;margin:30px 0;border:1px solid rgba(255,255,255,0.1);">
<p style="width:100%;text-align:center;margin:0 0 10px;color:#9ca3af;font-size:0.9rem;text-transform:uppercase;letter-spacing:1px;">📤 Share this article</p>
<a href="'.$wa.'" target="_blank" rel="nofollow noopener" style="display:inline-flex;align-items:center;gap:8px;background:#25D366;color:white;padding:10px 20px;border-radius:50px;text-decoration:none;font-weight:700;">📱 WhatsApp</a>
<a href="'.$tg.'" target="_blank" rel="nofollow noopener" style="display:inline-flex;align-items:center;gap:8px;background:#2CA5E0;color:white;padding:10px 20px;border-radius:50px;text-decoration:none;font-weight:700;">✈️ Telegram</a>
<a href="'.$fb.'" target="_blank" rel="nofollow noopener" style="display:inline-flex;align-items:center;gap:8px;background:#1877F2;color:white;padding:10px 20px;border-radius:50px;text-decoration:none;font-weight:700;">👍 Facebook</a>
<a href="'.$tw.'" target="_blank" rel="nofollow noopener" style="display:inline-flex;align-items:center;gap:8px;background:#1DA1F2;color:white;padding:10px 20px;border-radius:50px;text-decoration:none;font-weight:700;">🐦 Twitter</a>
</div>';
        return $content . $html;
    }
    add_filter('the_content', 'pbn_social_share_buttons', 25);
}

// 8. Footer Legal Links (injected via wp_footer — no theme menu support needed)
add_action('wp_footer', function() {
    echo '
<div id="pbn-footer-links" style="
    text-align:center;
    padding:20px 15px;
    background:rgba(10,12,20,0.95);
    border-top:1px solid rgba(225,29,72,0.3);
    font-size:0.85rem;
    color:#6b7280;
    position:relative;
    z-index:100;
">
    <div style="margin-bottom:8px;">
        <a href="/privacy-policy-2/" style="color:#9ca3af;text-decoration:none;margin:0 12px;" rel="nofollow">🔒 Privacy Policy</a>
        <a href="/terms-and-conditions/" style="color:#9ca3af;text-decoration:none;margin:0 12px;" rel="nofollow">📋 Terms &amp; Conditions</a>
        <a href="/aviator-guide/" style="color:#9ca3af;text-decoration:none;margin:0 12px;" rel="nofollow">✈️ Aviator Guide</a>
        <a href="/cricket-betting-guide/" style="color:#9ca3af;text-decoration:none;margin:0 12px;" rel="nofollow">🏏 Cricket Betting</a>
    </div>
    <div style="font-size:0.75rem;color:#4b5563;">
        ⚠️ 18+ Only. Gambling involves risk. Play responsibly. | &copy; ' . date('Y') . ' LuckyBetVIP.com
    </div>
</div>';
}, 99);
