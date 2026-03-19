import requests
import pandas as pd
import time

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

BASE_URL = "https://www.reddit.com/r/{}/.json?limit=100"


def fetch_post(subreddit):
    url = BASE_URL.format(subreddit)
    response  = requests.get(url,  headers=HEADERS)
    data = response.json()
    # print(response.status_code)
    # print(response.text[:500])
    return data['data']['children']


def fetch_user_comments(username, after=None):
    url = f"https://www.reddit.com/user/{username}/comments.json?limit=100"
    if after:
        url += f"after={after}"
    response = requests.get(url, headers=HEADERS)
    data = response.json()
    return data['data']['children'], data['data']['after']
    


def parse_post(post):
    data = post['data']
    return {
        'title'       : data['title'],
        'author'      : data['author'],
        'score'       : data['score'],
        'num_comments': data['num_comments'],
        'url'         : data['url'],
        'created_utc' : pd.to_datetime(data['created_utc'], unit='s'),
        'subreddit'   : data['subreddit']
    }



def parse_comment(comment, index):
    data = comment['data']
    created = pd.to_datetime(data['created_utc'], unit='s')

    return {
        'incident_id' : f"IR-{str(index).zfill(3)}",  # IR-001, IR-002...
        'username'    : data['author'],
        'comment_text': data['body'],
        'subreddit'   : data['subreddit'],
        'date'        : created,
        'comment_url' : f"https://reddit.com{data['permalink']}",
        'is_reply'    : data['parent_id'].startswith('t1_')  # t1_ means reply to comment
    } 





def run_scraper(subreddits):
    all_post = []

    for subreddit in subreddits:
        print(f"  Scraping r/{subreddit}...")
        posts =  fetch_post(subreddit)

        for post  in posts:
            data =  parse_post(post)
            all_post.append(data)

        print(f" {len(posts)} posts scraped from r/{subreddit}")
        time.sleep(1)
    
    df = pd.DataFrame(all_post)
    print()
    print(f"\n✅ Total: {len(df)} posts scraped")
    return df

def scrape_user_comments(username, from_date="2025-10-11"):
    all_comments = []
    after = None
    index = 1
    from_date = pd.to_datetime(from_date)

    print(f"Scraping comments for u/{username} ...")

    while True:
        comments, after = fetch_user_comments(username, after)

        if not comments:
            break

        for comment in comments:
            parsed = parse_comment(comment, index)

            if parsed['date'] < from_date:
                print(f"Reached date limit - Stopping")
                return pd.DataFrame(all_comments)
            all_comments.append(parsed)
            index += 1
        
        print(f"  {len(all_comments)}  comments collected  so far")

        if not after:
            break
        time.sleep(1)
    
    df =  pd.DataFrame(all_comments)
    print(f"✅ Total: {len(df)} comments scraped")
    return df



if __name__ == '__main__':
    SUBREDDITS =  ['python', 'datascience', 'remotejobs', 'webscraping', 'dataanalyst',  'Nigeria']

    df = run_scraper(SUBREDDITS)
    df.to_csv('reddit_data.csv',  index=False)
    print("Saved to reddit_data.csv")


if __name__ == "__main__":  # was "_-main__"
    username = input("Enter Reddit username: ")
    from_date = input("Enter start date (YYYY-MM-DD) or press Enter for default: ")
    if not from_date:
        from_date = "2025-10-11"
    df = scrape_user_comments(username, from_date=from_date)
    df.to_csv(f"{username}_comments.csv", index=False)
    print(f"✅ Saved to {username}_comments.csv")