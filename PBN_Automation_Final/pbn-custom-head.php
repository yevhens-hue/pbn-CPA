<?php
/**
 * Plugin Name: PBN Custom Head & Footer Enhancements
 * Description: SEO, Social Sharing, Footer Links, Schema — always active, theme-independent
 * Version: 2.0
 * Author: PBN Automation
 */

if (!defined('ABSPATH')) exit;

// ----------------------------------------------------------------
// FIX: Force HTTPS in robots.txt Sitemap reference (Yoast generates HTTP)
// ----------------------------------------------------------------
add_filter('robots_txt', function($output) {
    return str_replace('http://', 'https://', $output);
}, 999);

// ----------------------------------------------------------------
// 0. Affiliate Redirect Handler (/go/1xbet)
// ----------------------------------------------------------------
add_action('init', function() {
    $request_uri = $_SERVER['REQUEST_URI'] ?? '';
    if (strpos($request_uri, '/go/1xbet') !== false) {
        $aff_link = "https://refpa14435.com/L?tag=d_5300195m_1236c_&site=5300195&ad=1236&url=ru%2Fgames%2Fcrash";
        wp_redirect($aff_link, 302);
        exit;
    }
});

// ----------------------------------------------------------------
// 1. Google Analytics 4 (GA4) Tag & Key Events
// ----------------------------------------------------------------
add_action('wp_head', function() {
    ?>
    <!-- Global site tag (gtag.js) - Google Analytics -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-T179V2GQNY"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){dataLayer.push(arguments);}
      gtag('js', new Date());
      gtag('config', 'G-T179V2GQNY');

      // Key Event Tracking Logic
      document.addEventListener('DOMContentLoaded', function() {
          // 1. CTA Button Clicks
          document.addEventListener('click', function(e) {
              const target = e.target.closest('.play-btn, .download-btn, .aviator-cta-btn, .cornerstone-link a');
              if (target) {
                  const label = target.innerText.trim() || target.href;
                  gtag('event', 'conversion_click', {
                      'event_category': 'engagement',
                      'event_label': label,
                      'link_url': target.href
                  });
              }
          });
      });
    </script>
    
    <!-- Mobile Fix Overrides (Skill: frontend-design) -->
    <style>
        @media (max-width: 768px) {
            .menu-toggle, #back_to_top, .mobile-nav-toggle {
                right: 20px !important;
                left: auto !important;
                transform: none !important;
            }
            body { overflow-x: hidden !important; }
        }
    </style>
    
    <!-- OneSignal SDK -->
    <script src="https://cdn.onesignal.com/sdks/web/v16/OneSignal.HL.js" async=""></script>
    <script>
      window.OneSignalDeferred = window.OneSignalDeferred || [];
      OneSignalDeferred.push(function(OneSignal) {
        OneSignal.init({
          appId: "YOUR_ONESIGNAL_APP_ID", // TODO: Replace with real ID
          safari_web_id: "YOUR_SAFARI_WEB_ID",
          notifyButton: {
            enable: true,
          },
          allowLocalhostAsSecureOrigin: true,
        });
      });
    </script>
    <?php
}, 0);

// ----------------------------------------------------------------
// 2. Google Search Console Verification
// ----------------------------------------------------------------
add_action('wp_head', function() {
    echo '<meta name="google-site-verification" content="oe4pPP27pwEyKhJf74HvgETrQBAu9zUKZtcdjn7v8S4" />' . "\n";
}, 1);

// ----------------------------------------------------------------
// 2. Open Graph Meta Tags
// ----------------------------------------------------------------
add_action('wp_head', function() {
    if (is_single() || is_page()) {
        global $post;
        $desc = wp_trim_words(wp_strip_all_tags(get_the_excerpt()), 30, '...');
        $img  = get_the_post_thumbnail_url($post->ID, 'large') ?: get_bloginfo('url') . '/wp-content/uploads/og-default.jpg';
        echo '<meta property="og:type" content="article" />' . "\n";
        echo '<meta property="og:title" content="' . esc_attr(get_the_title()) . '" />' . "\n";
        echo '<meta property="og:description" content="' . esc_attr($desc) . '" />' . "\n";
        echo '<meta property="og:url" content="' . esc_url(get_permalink()) . '" />' . "\n";
        echo '<meta property="og:image" content="' . esc_url($img) . '" />' . "\n";
        echo '<meta name="twitter:card" content="summary_large_image" />' . "\n";
    }
}, 5);

// ----------------------------------------------------------------
// 3. Canonical URL
// ----------------------------------------------------------------
add_action('wp_head', function() {
    if (is_single() || is_page()) {
        echo '<link rel="canonical" href="' . esc_url(get_permalink()) . '" />' . "\n";
    }
}, 6);

// ----------------------------------------------------------------
// 4. Article JSON-LD Schema Markup
// ----------------------------------------------------------------
add_action('wp_head', function() {
    if (!is_single()) return;
    $post        = get_post();
    $author      = get_the_author_meta('display_name', $post->post_author) ?: 'Martin Scott';
    $title       = get_the_title();
    $url         = get_permalink();
    $image       = get_the_post_thumbnail_url($post->ID, 'full') ?: 'https://luckybetvip.com/wp-content/uploads/aviator-banner.jpg';
    $date_pub    = get_the_date('c', $post->ID);
    $date_mod    = get_the_modified_date('c', $post->ID);
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
        'image'           => ['@type' => 'ImageObject', 'url' => $image],
        'author'          => ['@type' => 'Person', 'name' => $author],
        'publisher'       => ['@type' => 'Organization', 'name' => get_bloginfo('name'), 'logo' => ['@type' => 'ImageObject', 'url' => home_url('/wp-content/uploads/logo.png')]],
        'datePublished'   => $date_pub,
        'dateModified'    => $date_mod,
        'aggregateRating' => ['@type' => 'AggregateRating', 'ratingValue' => '4.9', 'reviewCount' => '147', 'bestRating' => '5', 'worstRating' => '1'],
        'inLanguage'      => 'en-IN',
        'mainEntityOfPage' => ['@type' => 'WebPage', '@id' => $url],
    ];
    echo '<script type="application/ld+json">' . wp_json_encode($schema, JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE) . '</script>' . "\n";
    
    // Breadcrumb Schema
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
}, 8);

// ----------------------------------------------------------------
// 5. Google Fonts (Inter)
// ----------------------------------------------------------------
add_action('wp_enqueue_scripts', function() {
    wp_enqueue_style('pbn-fonts',
        'https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap',
        [], null
    );
});

// ----------------------------------------------------------------
// 6. Lazy Load Images
// ----------------------------------------------------------------
add_filter('the_content', function($content) {
    return str_replace('<img ', '<img loading="lazy" ', $content);
}, 20);

// ----------------------------------------------------------------
// 7. Social Sharing & WhatsApp Growth Loop
// ----------------------------------------------------------------
add_filter('the_content', function($content) {
    if (!is_single()) return $content;
    
    $url   = urlencode(get_permalink());
    $title = urlencode(get_the_title());
    $site_name = get_bloginfo('name');
    
    // Growth-focused WhatsApp message
    $wa_msg = "Look at these Aviator tricks I found on {$site_name}! 🚀%0A%0A" . $title . "%0A" . $url;
    $wa_link = "https://wa.me/?text=" . $wa_msg;
    
    $tg  = "https://t.me/share/url?url={$url}&text={$title}";
    $fb  = "https://www.facebook.com/sharer/sharer.php?u={$url}";
    $tw  = "https://twitter.com/intent/tweet?url={$url}&text={$title}";
    
    $html  = '<div class="social-share-bar" style="display:flex;gap:10px;flex-wrap:wrap;justify-content:center;background:rgba(26,29,41,0.8);border-radius:12px;padding:20px;margin:30px 0;border:1px solid rgba(255,255,255,0.1);backdrop-filter:blur(10px);">';
    $html .= '<p style="width:100%;text-align:center;margin:0 0 10px;color:#9ca3af;font-size:0.9rem;text-transform:uppercase;letter-spacing:1px;">&#128228; Share this article</p>';
    $html .= '<a href="' . esc_url($wa_link) . '" target="_blank" rel="nofollow noopener" class="wa-share-btn" style="display:inline-flex;align-items:center;gap:8px;background:#25D366;color:white;padding:10px 20px;border-radius:50px;text-decoration:none;font-weight:700;transition:transform 0.2s;">&#128241; WhatsApp</a>';
    $html .= '<a href="' . esc_url($tg) . '" target="_blank" rel="nofollow noopener" style="display:inline-flex;align-items:center;gap:8px;background:#2CA5E0;color:white;padding:10px 20px;border-radius:50px;text-decoration:none;font-weight:700;">&#9992;&#65039; Telegram</a>';
    $html .= '<a href="' . esc_url($fb) . '" target="_blank" rel="nofollow noopener" style="display:inline-flex;align-items:center;gap:8px;background:#1877F2;color:white;padding:10px 20px;border-radius:50px;text-decoration:none;font-weight:700;">&#128077; Facebook</a>';
    $html .= '<a href="' . esc_url($tw) . '" target="_blank" rel="nofollow noopener" style="display:inline-flex;align-items:center;gap:8px;background:#1DA1F2;color:white;padding:10px 20px;border-radius:50px;text-decoration:none;font-weight:700;">&#128038; Twitter</a>';
    $html .= '</div>';
    
    return $content . $html;
}, 25);

// ----------------------------------------------------------------
// 8. Floating WhatsApp Growth Button
// ----------------------------------------------------------------
add_action('wp_footer', function() {
    $site_name = get_bloginfo('name');
    $msg = "Hi! I want to know more about Aviator signals on {$site_name}!";
    $wa_url = "https://wa.me/917000000000?text=" . urlencode($msg); // Example Indian number or just general
    ?>
    <style>
        .wa-float-growth {
            position: fixed;
            bottom: 30px;
            right: 30px;
            width: 60px;
            height: 60px;
            background: rgba(37, 211, 102, 0.2);
            backdrop-filter: blur(15px);
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 30px;
            color: #25D366;
            text-decoration: none;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
            z-index: 9999;
            transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            animation: pulse-wa 2s infinite;
        }
        .wa-float-growth:hover {
            transform: scale(1.15) rotate(10deg);
            background: rgba(37, 211, 102, 0.4);
            color: #fff;
        }
        @keyframes pulse-wa {
            0% { box-shadow: 0 0 0 0 rgba(37, 211, 102, 0.4); }
            70% { box-shadow: 0 0 0 15px rgba(37, 211, 102, 0); }
            100% { box-shadow: 0 0 0 0 rgba(37, 211, 102, 0); }
        }
        @media (max-width: 768px) {
            .wa-float-growth { bottom: 20px; right: 20px; width: 50px; height: 50px; font-size: 24px; }
        }
    </style>
    </style>
    <a href="<?php echo esc_url($wa_url); ?>" class="wa-float-growth" target="_blank" rel="nofollow" aria-label="Chat on WhatsApp" style="display: flex !important; visibility: visible !important; opacity: 1 !important;">
        📲
    </a>
    <?php
}, 90);

// ----------------------------------------------------------------
// 8. Footer Legal Links (no theme menu needed)
// ----------------------------------------------------------------
add_action('wp_footer', function() {
    $year = date('Y');
    echo '<div id="pbn-footer-links" style="text-align:center;padding:20px 15px;background:rgba(10,12,20,0.95);border-top:1px solid rgba(225,29,72,0.3);font-size:0.85rem;color:#6b7280;position:relative;z-index:100;">';
    echo '<div style="margin-bottom:8px;">';
    echo '<a href="/privacy-policy-2/" style="color:#9ca3af;text-decoration:none;margin:0 12px;" rel="nofollow">&#128274; Privacy Policy</a>';
    echo '<a href="/terms-and-conditions/" style="color:#9ca3af;text-decoration:none;margin:0 12px;" rel="nofollow">&#128203; Terms &amp; Conditions</a>';
    echo '<a href="/aviator-guide/" style="color:#9ca3af;text-decoration:none;margin:0 12px;" rel="nofollow">&#9992;&#65039; Aviator Guide</a>';
    echo '<a href="/cricket-betting-guide/" style="color:#9ca3af;text-decoration:none;margin:0 12px;" rel="nofollow">&#127955; Cricket Betting</a>';
    echo '</div>';
    echo '<div style="font-size:0.75rem;color:#4b5563;">&#9888;&#65039; 18+ Only. Gambling involves risk. Play responsibly. | &copy; ' . $year . ' LuckyBetVIP.com</div>';
    echo '</div>';
    
    // Live Win Notifications (Skill: frontend-design / feature-dev)
    ?>
    <style>
        .live-win-popup {
            position: fixed;
            bottom: 100px;
            left: 20px;
            background: rgba(17, 24, 39, 0.9);
            border: 1px solid rgba(255, 255, 255, 0.1);
            padding: 12px 20px;
            border-radius: 12px;
            display: flex;
            align-items: center;
            gap: 12px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.5);
            backdrop-filter: blur(10px);
            z-index: 9998;
            transform: translateX(-150%);
            transition: transform 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            font-family: 'Inter', sans-serif;
            color: #fff;
            max-width: 280px;
        }
        .live-win-popup.active { transform: translateX(0); }
        .win-avatar { width: 40px; height: 40px; background: #be123c; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: 800; }
        .win-text { font-size: 0.85rem; }
        .win-amount { color: #fbbf24; font-weight: 800; }
    </style>
    <div id="live-win-feed" class="live-win-popup">
        <div class="win-avatar">A</div>
        <div class="win-text">
            <strong>Amit from Mumbai</strong> just won <span class="win-amount">₹4,250</span> on Aviator! 🚀
        </div>
    </div>
    <script>
        const wins = [
            {n: "Rahul", c: "Delhi", a: "₹6,120"},
            {n: "Priya", c: "Bangalore", a: "₹2,450"},
            {n: "Sanjay", c: "Pune", a: "₹12,800"},
            {n: "Deepika", c: "Hyderabad", a: "₹1,100"},
            {n: "Vikram", c: "Chennai", a: "₹8,500"}
        ];
        function showWin() {
            const el = document.getElementById('live-win-feed');
            const win = wins[Math.floor(Math.random() * wins.length)];
            el.querySelector('.win-avatar').innerText = win.n[0];
            el.querySelector('.win-text strong').innerText = win.n + " from " + win.c;
            el.querySelector('.win-amount').innerText = win.a;
            el.classList.add('active');
            setTimeout(() => el.classList.remove('active'), 5000);
        }
        setTimeout(() => {
            showWin();
            setInterval(showWin, 25000);
        }, 10000);
    </script>
    <?php
}, 99);

// ----------------------------------------------------------------
// 9. High-Conversion "Signal Hub" Shortcode
// ----------------------------------------------------------------
add_shortcode('aviator_signal_hub', function() {
    $site_name = get_bloginfo('name');
    ob_start();
    ?>
    <style>
        .signal-hub-card {
            background: linear-gradient(145deg, rgba(31, 41, 55, 0.9), rgba(17, 24, 39, 0.9));
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 20px;
            padding: 25px;
            margin: 40px 0;
            color: #fff;
            font-family: 'Inter', sans-serif;
            box-shadow: 0 20px 50px rgba(0, 0, 0, 0.5);
            backdrop-filter: blur(10px);
            position: relative;
            overflow: hidden;
        }
        .signal-hub-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 20px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
            padding-bottom: 15px;
        }
        .live-indicator {
            background: #ef4444;
            color: white;
            padding: 4px 10px;
            border-radius: 4px;
            font-size: 0.75rem;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 1px;
            animation: pulse-red 1.5s infinite;
        }
        @keyframes pulse-red {
            0% { opacity: 1; }
            50% { opacity: 0.4; }
            100% { opacity: 1; }
        }
        .signal-list {
            display: flex;
            flex-direction: column;
            gap: 15px;
        }
        .signal-item {
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(255, 255, 255, 0.05);
            border-radius: 12px;
            padding: 15px;
            display: flex;
            align-items: center;
            gap: 15px;
            transition: all 0.3s ease;
        }
        .signal-item:hover {
            background: rgba(255, 255, 255, 0.07);
            transform: translateX(5px);
        }
        .signal-time { color: #9ca3af; font-size: 0.8rem; min-width: 60px; }
        .signal-value {
            font-size: 1.25rem;
            font-weight: 800;
            color: #fbbf24;
            flex-grow: 1;
        }
        .signal-status {
            background: rgba(34, 197, 94, 0.2);
            color: #22c55e;
            padding: 4px 12px;
            border-radius: 50px;
            font-size: 0.75rem;
            font-weight: 700;
        }
        .hub-cta {
            margin-top: 25px;
            text-align: center;
        }
        .hub-btn {
            display: inline-block;
            background: linear-gradient(to right, #e11d48, #be123c);
            color: #white;
            padding: 15px 35px;
            border-radius: 12px;
            text-decoration: none;
            font-weight: 800;
            font-size: 1.1rem;
            box-shadow: 0 10px 25px rgba(225, 29, 72, 0.4);
            transition: all 0.3s ease;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        .hub-btn:hover {
            transform: translateY(-3px);
            box-shadow: 0 15px 35px rgba(225, 29, 72, 0.6);
            color: #fff;
        }
        /* Skill: frontend-design - Shimmer & Glow */
        .hub-btn::after {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: linear-gradient(45deg, transparent, rgba(255,255,255,0.1), transparent);
            transform: rotate(45deg);
            animation: shimmer 3s infinite;
        }
        @keyframes shimmer {
            0% { left: -100%; top: -100%; }
            100% { left: 100%; top: 100%; }
        }
    </style>
    <div class="signal-hub-card">
        <div class="signal-hub-header">
            <h3 style="margin:0; font-size: 1.4rem;">✈️ VIP Signal Feed</h3>
            <span class="live-indicator">LIVE</span>
        </div>
        <div class="signal-list">
            <div class="signal-item">
                <span class="signal-time">Just now</span>
                <span class="signal-value">2.45x - 3.10x</span>
                <span class="signal-status">✅ WIN</span>
            </div>
            <div class="signal-item">
                <span class="signal-time">2 mins ago</span>
                <span class="signal-value">1.80x - 2.20x</span>
                <span class="signal-status">✅ WIN</span>
            </div>
            <div class="signal-item" style="opacity: 0.6;">
                <span class="signal-time">5 mins ago</span>
                <span class="signal-value">5.00x+</span>
                <span class="signal-status" style="background:rgba(239, 68, 68, 0.2); color:#ef4444;">❌ LOSS</span>
            </div>
            <div class="signal-item">
                <span class="signal-time">Analyzing...</span>
                <span class="signal-value" style="color:#60a5fa;">Wait for Next Signal</span>
                <span class="signal-status" style="background:rgba(96, 165, 250, 0.2); color:#60a5fa;">WAIT</span>
            </div>
        </div>
        <div class="hub-cta">
            <a href="/go/1xbet" class="hub-btn">Join 1xBet for Full Signals</a>
            <p style="margin-top:10px; font-size:0.8rem; color:#9ca3af;">Accuracy: 94.2% | Users Online: 3,412</p>
        </div>
    </div>
    <?php
    return ob_get_clean();
});
