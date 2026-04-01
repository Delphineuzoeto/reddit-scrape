import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import sqlite3
from wordcloud import WordCloud
import os

# ============================================
# SETUP
# ============================================
conn = sqlite3.connect("beauty_in_black.db")
comments_df = pd.read_sql_query("SELECT * FROM final_bib_comments", conn)
character_df = pd.read_sql_query("SELECT * FROM character_sentiment", conn)
conn.close()

os.makedirs("charts", exist_ok=True)

print(f"✅ Loaded {len(comments_df)} comments")
print(f"✅ Loaded {len(character_df)} characters")

# ============================================
# CHART 1: OVERALL SENTIMENT BREAKDOWN
# ============================================
sentiment_counts = comments_df['sentiment'].value_counts()
colors = {'positive': '#2ecc71', 'negative': '#e74c3c', 'neutral': '#95a5a6'}
bar_colors = [colors[s] for s in sentiment_counts.index]

fig, ax = plt.subplots(figsize=(8, 5))
bars = ax.bar(sentiment_counts.index, sentiment_counts.values, color=bar_colors, edgecolor='white', linewidth=1.5)

for bar, val in zip(bars, sentiment_counts.values):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2,
            f'{val}\n({val/len(comments_df)*100:.1f}%)',
            ha='center', va='bottom', fontweight='bold', fontsize=11)

ax.set_title("Overall Sentiment — Beauty in Black Reddit Comments", fontsize=14, fontweight='bold', pad=15)
ax.set_xlabel("Sentiment", fontsize=12)
ax.set_ylabel("Number of Comments", fontsize=12)
ax.set_ylim(0, sentiment_counts.max() + 30)
sns.despine()
plt.tight_layout()
plt.savefig("charts/overall_sentiment.png", dpi=150, bbox_inches='tight')
plt.close()
print("✅ Chart 1 saved: overall_sentiment.png")

# ============================================
# CHART 2: CHARACTER SENTIMENT
# ============================================
char_colors = ['#2ecc71' if x >= 0 else '#e74c3c' for x in character_df['avg_sentiment']]

fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.barh(character_df['character'], character_df['avg_sentiment'], color=char_colors, edgecolor='white')

for bar, val in zip(bars, character_df['avg_sentiment']):
    ax.text(val + 0.01 if val >= 0 else val - 0.01,
            bar.get_y() + bar.get_height()/2,
            f'{val}', va='center',
            ha='left' if val >= 0 else 'right',
            fontweight='bold', fontsize=10)

ax.axvline(x=0, color='black', linewidth=0.8, linestyle='--')
ax.set_title("Character Sentiment — Beauty in Black", fontsize=14, fontweight='bold', pad=15)
ax.set_xlabel("Average Sentiment Score", fontsize=12)
ax.set_ylabel("Character", fontsize=12)

positive_patch = mpatches.Patch(color='#2ecc71', label='Positive')
negative_patch = mpatches.Patch(color='#e74c3c', label='Negative')
ax.legend(handles=[positive_patch, negative_patch])
sns.despine()
plt.tight_layout()
plt.savefig("charts/character_sentiment.png", dpi=150, bbox_inches='tight')
plt.close()
print("✅ Chart 2 saved: character_sentiment.png")

# ============================================
# CHART 3: SENTIMENT OVER TIME
# ============================================
comments_df['created_utc'] = pd.to_datetime(comments_df['created_utc'])
comments_df['month'] = comments_df['created_utc'].dt.to_period('M')

time_df = comments_df.groupby(['month', 'sentiment']).size().unstack(fill_value=0)
time_df.index = time_df.index.astype(str)

fig, ax = plt.subplots(figsize=(12, 5))
for sentiment, color in colors.items():
    if sentiment in time_df.columns:
        ax.plot(time_df.index, time_df[sentiment], marker='o', label=sentiment,
                color=color, linewidth=2, markersize=5)

ax.set_title("Sentiment Over Time — Beauty in Black Reddit", fontsize=14, fontweight='bold', pad=15)
ax.set_xlabel("Month", fontsize=12)
ax.set_ylabel("Number of Comments", fontsize=12)
ax.legend()
plt.xticks(rotation=45)
sns.despine()
plt.tight_layout()
plt.savefig("charts/sentiment_over_time.png", dpi=150, bbox_inches='tight')
plt.close()
print("✅ Chart 3 saved: sentiment_over_time.png")

# ============================================
# CHART 4: WORD CLOUD
# ============================================
all_text = ' '.join(comments_df['comment_text'].dropna().values)

stopwords = {'the', 'a', 'an', 'is', 'it', 'in', 'of', 'and', 'to',
             'she', 'he', 'they', 'her', 'his', 'that', 'this', 'was',
             'for', 'on', 'are', 'with', 'as', 'at', 'be', 'by', 'from',
             'or', 'but', 'not', 'have', 'had', 'has', 'was', 'were',
             'i', 'you', 'we', 'my', 'me', 'him', 'them', 'their', 'its',
             'so', 'do', 'did', 'just', 'like', 'get', 'got', 'would', 'could'}

wordcloud = WordCloud(
    width=1200, height=600,
    background_color='black',
    colormap='RdYlGn',
    stopwords=stopwords,
    max_words=100,
    collocations=False
).generate(all_text)

fig, ax = plt.subplots(figsize=(14, 7))
ax.imshow(wordcloud, interpolation='bilinear')
ax.axis('off')
ax.set_title("Most Used Words — Beauty in Black Reddit Comments",
             fontsize=14, fontweight='bold', pad=15, color='black')
plt.tight_layout()
plt.savefig("charts/wordcloud.png", dpi=150, bbox_inches='tight')
plt.close()
print("✅ Chart 4 saved: wordcloud.png")

print("\n🎉 All 4 charts saved to charts/ folder!")