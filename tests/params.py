from favicon_finder.favicons import check_basic_url, get_favicon_url

get_fav_url_params = [
    ("1. Ensure False", "homedepot.com", False),
    ("2. 200, not found", "momoshop.com.tw", (200, "link not found")),
    (
        "3. Requires unparse",
        "discord.com",
        "http://discord.com/assets/847541504914fd33810e70a0ea73177e.ico",
    ),
]
get_fav_url_ids = [x[0] for x in get_fav_url_params]

check_domain_params = [
    (
        "1. Run check_basic",
        check_basic_url,
        {
            "facebook.com": "http://facebook.com/favicon.ico",
            "amazon.com": "http://amazon.com/favicon.ico",
            "yahoo.com": "http://yahoo.com/favicon.ico",
        },
    ),
    (
        "2. Run get_favicon_url",
        get_favicon_url,
        {
            "amazon.com": False,
            "facebook.com": "https://static.xx.fbcdn.net/rsrc.php/yb/r/hLRJ1GG_y0J.ico",
            "yahoo.com": "https://s.yimg.com/cv/apiv2/default/icons/favicon_y19_32x32_custom.svg",
        },
    ),
]
check_domain_ids = [x[0] for x in check_domain_params]
