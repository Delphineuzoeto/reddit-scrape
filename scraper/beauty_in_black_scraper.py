import requests
import pandas as pd
import time
import os

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

SUBREDDITS = [
    "BeautyInBlack",
    "netflix",
    "TylerPerry",
    "blacktv"
]

CHARACTERS = [
    "kimmie",
    "mallory",
    "horace",
    "olivia",
    "charles",
    "rain",
    "jules",
    "roy",
    "varney",
    "body",
    "norman",
    "calvin",
    "delinda",
    "angel"
]

def fetch_posts(subreddit, category="hot", limit=100):
    url = f"https://www.reddit.com/r/{subreddit}/{category}.json?limit={limit}"
    response = requests.get(url, headers=HEADERS)
    
    if response.status_code != 200:
        print(f"❌ Failed to fetch r/{subreddit} — Status: {response.status_code}")
        return []
    
    data = response.json()
    return data['data']['children']


def parse_post(post):
    data = post['data']
    return {
        'post_id'     : data['id'],
        'title'       : data['title'],
        'author'      : data['author'],
        'score'       : data['score'],
        'num_comments': data['num_comments'],
        'url'         : data['url'],
        'created_utc' : pd.to_datetime(data['created_utc'], unit='s'),
        'subreddit'   : data['subreddit'],
        'post_text'   : data.get('selftext', '')
    }


def fetch_comments(post_id, subreddit):
    url = f"https://www.reddit.com/r/{subreddit}/comments/{post_id}.json"
    response = requests.get(url, headers=HEADERS)
    
    if response.status_code != 200:
        print(f"❌ Failed to fetch comments for post {post_id} — Status: {response.status_code}")
        return []
    
    data = response.json()
    return data[1]['data']['children']

def parse_comment(comment):
    data = comment['data']
    
    if not data.get('body'):
        return None
    
    return {
        'comment_id'  : data['id'],
        'post_id'     : data['link_id'].replace('t3_', ''),
        'author'      : data['author'],
        'comment_text': data['body'],
        'score'       : data['score'],
        'created_utc' : pd.to_datetime(data['created_utc'], unit='s'),
        'subreddit'   : data['subreddit'],
        'is_reply'    : data['parent_id'].startswith('t1_')
    }

def run_scraper(subreddits, categories=["hot", "new", "top"]):
    all_posts = []
    all_comments = []

    for subreddit in subreddits:
        for category in categories:
            print(f"📌 Scraping r/{subreddit} — {category}...")
            posts = fetch_posts(subreddit, category=category)

            for post in posts:
                parsed_post = parse_post(post)
                all_posts.append(parsed_post)

                print(f"   💬 Fetching comments for: {parsed_post['title'][:50]}...")
                comments = fetch_comments(parsed_post['post_id'], subreddit)

                for comment in comments:
                    parsed_comment = parse_comment(comment)
                    if parsed_comment:
                        all_comments.append(parsed_comment)

                time.sleep(3)

    posts_df = pd.DataFrame(all_posts)
    comments_df = pd.DataFrame(all_comments)

    print(f"\n✅ Total posts: {len(posts_df)}")
    print(f"✅ Total comments: {len(comments_df)}")

    return posts_df, comments_df


if __name__ == "__main__":
    posts_df, comments_df = run_scraper(SUBREDDITS)

    posts_df.to_csv("bib_posts.csv", mode='a', index=False, header=not os.path.exists("bib_posts.csv"))
    comments_df.to_csv("bib_comments.csv", mode='a', index=False, header=not os.path.exists("bib_comments.csv"))

    print("✅ Saved to bib_posts.csv and bib_comments.csv")