"""
Popular Bookstore — Book Recommendation Engine
IS215 Digital Business Transformation

Two models:
  1. Market Basket Analysis (Association Rules via Apriori)
     → "Customers who bought X also bought Y"
  2. Collaborative Filtering (User-Item Matrix + Cosine Similarity)
     → "Based on your purchase history, you might like..."

Usage:
    python recommendation_engine.py

Outputs:
    - Console report
    - recommendations_output.json  (consumed by the HTML front-end)
"""

import pandas as pd
import numpy as np
import json
import warnings
warnings.filterwarnings("ignore")

from sklearn.metrics.pairwise import cosine_similarity
from mlxtend.frequent_patterns import apriori, association_rules
from mlxtend.preprocessing import TransactionEncoder


# ─────────────────────────────────────────────
# 1. LOAD DATA
# ─────────────────────────────────────────────

print("=" * 60)
print("POPULAR BOOKSTORE — RECOMMENDATION ENGINE")
print("=" * 60)

purchases_df = pd.read_csv("purchases.csv")
books_df = pd.read_csv("books.csv")

print(f"\n[DATA] Loaded {len(purchases_df)} purchase records")
print(f"[DATA] {purchases_df['user_id'].nunique()} unique users")
print(f"[DATA] {purchases_df['book_id'].nunique()} unique books")


# ─────────────────────────────────────────────
# 2. MARKET BASKET ANALYSIS (Association Rules)
# ─────────────────────────────────────────────

print("\n" + "─" * 60)
print("MODEL 1: MARKET BASKET ANALYSIS (Apriori)")
print("─" * 60)

# Build basket: one row per user, columns = books, values = 1/0
basket = (
    purchases_df
    .groupby(["user_id", "book_title"])["book_id"]
    .count()
    .unstack(fill_value=0)
)
basket_binary = basket.map(lambda x: 1 if x > 0 else 0)

# Run Apriori — min_support tuned low because dataset is small (20 users)
frequent_itemsets = apriori(
    basket_binary,
    min_support=0.15,       # book pair appears in ≥15% of users
    use_colnames=True,
    max_len=2               # pairs only (antecedent → consequent)
)

rules = association_rules(
    frequent_itemsets,
    metric="lift",
    min_threshold=1.2       # lift > 1 means positively correlated
)

# Clean up for display
rules["antecedent"] = rules["antecedents"].apply(lambda x: list(x)[0])
rules["consequent"] = rules["consequents"].apply(lambda x: list(x)[0])
rules_clean = (
    rules[["antecedent", "consequent", "support", "confidence", "lift"]]
    .sort_values("lift", ascending=False)
    .reset_index(drop=True)
)

print(f"\nTop Association Rules (by Lift):")
print(rules_clean.head(10).to_string(index=False))

# Build a lookup: given a book title → list of recommended titles
mba_lookup = {}
for _, row in rules_clean.iterrows():
    ant = row["antecedent"]
    con = row["consequent"]
    conf = round(row["confidence"], 2)
    lift = round(row["lift"], 2)
    mba_lookup.setdefault(ant, []).append({
        "title": con,
        "confidence": conf,
        "lift": lift,
        "reason": f"{int(conf*100)}% of buyers also purchased this (lift {lift})"
    })


# ─────────────────────────────────────────────
# 3. COLLABORATIVE FILTERING
# ─────────────────────────────────────────────

print("\n" + "─" * 60)
print("MODEL 2: COLLABORATIVE FILTERING (User-Item Cosine Similarity)")
print("─" * 60)

# Build user-item rating matrix
user_item = (
    purchases_df
    .pivot_table(index="user_id", columns="book_title", values="rating", fill_value=0)
)

# Compute user-user cosine similarity
user_sim_matrix = cosine_similarity(user_item)
user_sim_df = pd.DataFrame(
    user_sim_matrix,
    index=user_item.index,
    columns=user_item.index
)

def get_collab_recommendations(user_id, n=5):
    """
    For a given user, find the K most similar users,
    then recommend books they rated highly that the target user hasn't read.
    """
    if user_id not in user_sim_df.index:
        return []

    # Similarity scores for all other users
    sim_scores = user_sim_df[user_id].drop(user_id).sort_values(ascending=False)
    top_k_users = sim_scores.head(5).index.tolist()

    # Aggregate weighted ratings from similar users
    target_books = set(user_item.loc[user_id][user_item.loc[user_id] > 0].index)
    candidate_scores = {}

    for similar_user in top_k_users:
        weight = sim_scores[similar_user]
        similar_user_ratings = user_item.loc[similar_user]
        # Only consider books the target user has NOT read
        for book, rating in similar_user_ratings.items():
            if rating > 0 and book not in target_books:
                candidate_scores[book] = candidate_scores.get(book, 0) + weight * rating

    # Sort by weighted score
    sorted_candidates = sorted(candidate_scores.items(), key=lambda x: x[1], reverse=True)
    return sorted_candidates[:n]

# ─── Demo: Current user (just purchased "The Martian") ───
DEMO_USER = "U001"
demo_user_books = purchases_df[purchases_df["user_id"] == DEMO_USER]["book_title"].tolist()
print(f"\nDemo user ({DEMO_USER}) purchased: {demo_user_books}")

collab_recs = get_collab_recommendations(DEMO_USER, n=5)
print(f"\nCollaborative Filtering Recommendations:")
for title, score in collab_recs:
    print(f"  • {title:45s} (weighted score: {score:.2f})")


# ─────────────────────────────────────────────
# 4. SEARCH + RECOMMENDATION (Smart Search)
# ─────────────────────────────────────────────

print("\n" + "─" * 60)
print("FEATURE: SMART SEARCH RECOMMENDATIONS")
print("─" * 60)

def smart_search_recommendations(search_query, n=4):
    """
    Given a search query (author name or title keyword),
    find matching books and return MBA-based 'you might also like'.
    """
    search_lower = search_query.lower()
    # Match on title or author
    matches = books_df[
        books_df["title"].str.lower().str.contains(search_lower) |
        books_df["author"].str.lower().str.contains(search_lower)
    ]

    you_might_like = set()
    for _, book in matches.iterrows():
        if book["title"] in mba_lookup:
            for rec in mba_lookup[book["title"]]:
                you_might_like.add(rec["title"])

    # Remove titles already in search results
    search_titles = set(matches["title"].tolist())
    you_might_like -= search_titles

    return {
        "search_results": matches["title"].tolist(),
        "you_might_also_like": list(you_might_like)[:n]
    }

demo_search = smart_search_recommendations("Andy Weir")
print(f"\nSearch: 'Andy Weir'")
print(f"  Results: {demo_search['search_results']}")
print(f"  You might also like: {demo_search['you_might_also_like']}")


# ─────────────────────────────────────────────
# 5. POST-PURCHASE EMAIL JOURNEY
# ─────────────────────────────────────────────

print("\n" + "─" * 60)
print("FEATURE: POST-PURCHASE EMAIL RECOMMENDATIONS")
print("─" * 60)

def get_post_purchase_recommendations(last_purchased_title, user_id=None, n=3):
    """
    Email 1: Immediately after purchase — MBA-based 'while you wait' recs
    Email 2: 3 days after — 'Readers who loved X are now reading Y'
    Email 3: 30 days after — Personalised reading list from collab filtering
    """
    email1_recs = mba_lookup.get(last_purchased_title, [])[:n]

    # For Email 3, use collaborative filtering if user_id is known
    email3_recs = []
    if user_id:
        cf_recs = get_collab_recommendations(user_id, n=5)
        email3_recs = [title for title, _ in cf_recs]

    return {
        "email_1": {
            "subject": f"Your order is confirmed! While you wait, you might enjoy...",
            "recommendations": [r["title"] for r in email1_recs]
        },
        "email_2": {
            "subject": f"How are you finding {last_purchased_title}?",
            "recommendations": [r["title"] for r in mba_lookup.get(last_purchased_title, [])[:1]]
        },
        "email_3": {
            "subject": "Your personalised reading list is ready",
            "recommendations": email3_recs
        }
    }

demo_email = get_post_purchase_recommendations("The Martian", user_id="U001")
print(f"\nPost-purchase email sequence for user who bought 'The Martian':")
for email_key, email_data in demo_email.items():
    print(f"\n  [{email_key.upper()}] {email_data['subject']}")
    for rec in email_data["recommendations"]:
        print(f"    → {rec}")


# ─────────────────────────────────────────────
# 6. WISHLIST DEMAND SIGNAL ANALYSIS
# ─────────────────────────────────────────────

print("\n" + "─" * 60)
print("FEATURE: WISHLIST DEMAND SIGNAL → SUPPLY CHAIN")
print("─" * 60)

# Simulate wishlist data (mock)
wishlist_data = [
    {"user_id": "U005", "book_title": "The Dark Forest", "book_id": "B015"},
    {"user_id": "U008", "book_title": "The Dark Forest", "book_id": "B015"},
    {"user_id": "U012", "book_title": "The Dark Forest", "book_id": "B015"},
    {"user_id": "U015", "book_title": "The Dark Forest", "book_id": "B015"},
    {"user_id": "U003", "book_title": "Death's End",     "book_id": "B016"},
    {"user_id": "U010", "book_title": "Death's End",     "book_id": "B016"},
    {"user_id": "U001", "book_title": "Death's End",     "book_id": "B016"},
    {"user_id": "U007", "book_title": "Sapiens",         "book_id": "B017"},
    {"user_id": "U009", "book_title": "Sapiens",         "book_id": "B017"},
]

wishlist_df = pd.DataFrame(wishlist_data)
demand_signals = wishlist_df.groupby("book_title").size().reset_index(name="wishlist_count")
demand_signals = demand_signals.sort_values("wishlist_count", ascending=False)
demand_signals["reorder_recommendation"] = demand_signals["wishlist_count"].apply(
    lambda x: "🔴 URGENT restock" if x >= 4 else ("🟡 Monitor closely" if x >= 2 else "🟢 Watch")
)

print("\nWishlist Demand Signals (out-of-stock titles):")
print(demand_signals.to_string(index=False))


# ─────────────────────────────────────────────
# 7. EXPORT TO JSON (for HTML front-end)
# ─────────────────────────────────────────────

# Build book metadata lookup by title
book_meta = books_df.set_index("title").to_dict(orient="index")

def enrich_with_metadata(title_list):
    enriched = []
    for t in title_list:
        meta = book_meta.get(t, {})
        enriched.append({
            "title": t,
            "author": meta.get("author", "Unknown"),
            "genre": meta.get("genre", ""),
            "price": meta.get("price", 0),
            "cover_url": meta.get("cover_url", ""),
            "description": meta.get("description", "")
        })
    return enriched

# Prepare comprehensive JSON output
output = {
    "demo_user": {
        "user_id": DEMO_USER,
        "purchased_books": demo_user_books,
        "last_purchase": demo_user_books[-1] if demo_user_books else ""
    },
    "mba_recommendations": {
        title: enrich_with_metadata([r["title"] for r in recs[:4]])
        for title, recs in mba_lookup.items()
    },
    "collab_filtering_recommendations": enrich_with_metadata(
        [t for t, _ in collab_recs[:5]]
    ),
    "smart_search": {
        "query": "Andy Weir",
        "results": enrich_with_metadata(demo_search["search_results"]),
        "you_might_also_like": enrich_with_metadata(demo_search["you_might_also_like"])
    },
    "post_purchase_emails": {
        "email_1": {
            "subject": demo_email["email_1"]["subject"],
            "recommendations": enrich_with_metadata(demo_email["email_1"]["recommendations"])
        },
        "email_2": {
            "subject": demo_email["email_2"]["subject"],
            "recommendations": enrich_with_metadata(demo_email["email_2"]["recommendations"])
        },
        "email_3": {
            "subject": demo_email["email_3"]["subject"],
            "recommendations": enrich_with_metadata(demo_email["email_3"]["recommendations"])
        }
    },
    "association_rules": rules_clean.head(15).to_dict(orient="records"),
    "wishlist_demand_signals": demand_signals.to_dict(orient="records"),
    "model_stats": {
        "total_users": int(purchases_df["user_id"].nunique()),
        "total_books": int(purchases_df["book_id"].nunique()),
        "total_transactions": int(len(purchases_df)),
        "association_rules_found": int(len(rules_clean)),
        "min_support": 0.15,
        "min_lift": 1.2
    }
}

with open("recommendations_output.json", "w") as f:
    json.dump(output, f, indent=2)

print("\n" + "=" * 60)
print("✅  recommendations_output.json written successfully")
print("    → Import this into your HTML front-end")
print("=" * 60)