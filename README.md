# POPULAR Bookstore — Prototype User Guide

This is a multi-page interactive prototype for POPULAR Bookstore's digital 
transformation strategy. Open any `.html` file directly in a browser.
No server or installation required.

---

## Pages Overview

| File | Page | Initiative |
|---|---|---|
| `index.html` | Homepage / Landing | Omnichannel |
| `click-collect.html` | Click & Collect | Omnichannel |
| `recommendations.html` | Personalised Recommendations | Omnichannel |
| `subcription.html` | EduPass Subscription | Subscription |
| `book-preview.html` | Book Preview / Reader | Subscription |
| `viewer.html` | Document Viewer | Subscription |
| `tradein.html` | Book Trade-In Flow | Trade-In |
| `student-analysis.html` | Student Progress Analysis | Subscription |

---

## Homepage (`index.html`)

The main landing page demonstrating Popular's omnichannel digital storefront.

### Key Features

**Announcement Bar**
- Clickable banner linking to `tradein.html` for the Trade-In programme
- Displays current promotions and member benefits

**Header & Search**
- Search bar for books, stationery, and gadgets
- Sign In and Cart buttons with live cart count badge
- Cart modal shows items added and links to Click & Collect checkout

**Navigation**
- Dropdown menus for all product categories: Assessment, Stationery, 
  English Books, Chinese Books, Gadgets, Titbits & Snacks
- Quick links to On Sale and Trade-In pages

**Hero Banner**
- "Shop Now" button scrolls to product grid
- "Click & Collect" button scrolls to the service carousel
- "Trade In Books" button links to `tradein.html`

**Category Filter Pills**
- Filter the product grid by: All, Assessment, Stationery, English Books,
  Chinese Books, Gadgets, Titbits & Snacks, On Sale
- Grid updates instantly on selection

**Product Grid**
- 10 featured products with real book cover images
- Click any product card to open a product modal showing:
  - Book cover, category, title, price
  - Description
  - Add to Cart button (updates cart badge)
  - Add to Wishlist button
- "Add to Cart" button on each card adds directly without opening modal

**Service Carousel (Click & Collect + Subscription)**
- Two-slide auto-advancing carousel (advances every 5 seconds)
- Slide 1: Click & Collect — includes a live stock checker:
  1. Enter a book or product title
  2. Select an outlet from the dropdown
  3. Click "Check Availability" — shows simulated stock status 
     (In Stock / Low Stock) for that outlet and a nearby alternative
  4. Click "Reserve Now" to trigger a confirmation toast
- Slide 2: EduPass Study Pass — links to `subcription.html`
- Navigation: arrow buttons, dot indicators, swipe on mobile
- Progress bar at the bottom shows time until auto-advance
- Hover over carousel to pause auto-advance

**Trade-In Strip**
- Highlights the trade-in programme with key stats
- Links to `tradein.html`

**Membership Banner**
- Lists member perks including Trade-In credits
- "Join Free Today" opens a membership sign-up modal

**Footer**
- Links to all key pages including Click & Collect, Trade-In, and 
  store locator

---

## Click & Collect (`click-collect.html`)

Demonstrates the full 4-step Click & Collect reservation flow.

### Step 1 — Browse & Add to Cart
1. The page opens on the stock checker panel
2. Enter a book or product title in the search field
3. Select your preferred outlet from the dropdown (8 outlets available)
4. Click **Check Availability** — shows real-time simulated stock status:
   - Green badge: In Stock
   - Amber badge: Low Stock (2 left)
   - Nearby alternative outlet is also shown
5. Click **Reserve Now** to confirm

### Step 2 — Select Click & Collect at Checkout
1. Three fulfilment options are shown side by side:
   - Standard Delivery — $3.99, 3–5 days
   - Same-Day Delivery — $6.99, order before 12pm
   - **Free 2-Hour Click & Collect** 
2. Select Click & Collect to proceed

### Step 3 — Choose Outlet
1. Map view shows nearby Popular outlets with stock availability
2. Select your preferred outlet
3. Confirm collection time window (within 2 hours)

### Step 4 — Confirmation
1. Order confirmation screen shows:
   - Order reference number
   - Selected outlet and collection window
   - SMS notification confirmation
2. Links back to `index.html` to continue browsing

---

## Recommendations (`recommendations.html`)

Demonstrates the AI-powered book recommendation engine.
This page is the front-end output of `recommendation_engine.py`.
It uses Market Based Association & Collaborative Filtering.

### How It Works
The Python model (`recommendation_engine.py`) reads from two CSV files:
- `purchases.csv` — 60 mock transactions across 20 users and 14 books
- `books.csv` — book metadata (title, author, genre, price, cover)

It outputs `recommendations_output.json` which this page reads directly.

### Tabs

**Overview Tab**
- Shows model statistics: 20 users, 14 books, 60 transactions, 
  14 association rules generated
- Architecture diagram showing both models and all four 
  recommendation touchpoints

**Market Basket Analysis Tab**
- Select any book title from the trigger buttons
- The page shows which books customers who bought that title 
  also purchased, based on Apriori association rules
- Full rules table at the bottom shows all 14 rules with:
  - Support, Confidence, and Lift values
  - Confidence bar visualisation
  - Lift colour-coded: green (≥3×), amber (≥2×)

**Collaborative Filtering Tab**
- Shows demo user U001's purchase history
- Displays 5 personalised recommendations generated by 
  cosine similarity on the user-item rating matrix
- Explains the formula and methodology

**Smart Search Tab**
- Type any author or title in the search bar (e.g. "Andy Weir", 
  "Atomic Habits", "Dune")
- Search results appear with matching books
- "You might also like" strip appears below results — powered 
  by MBA association rules on the search results

**Post-Purchase Emails Tab**
- Shows the 3-email post-purchase sequence for demo user U001
- Click any email card to expand it and see the full mock email:
  - Email 1 (immediate): MBA-powered "while you wait" recommendations
  - Email 2 (3 days later): "Readers who loved X are now reading Y"
  - Email 3 (30 days later): Collaborative filtering personalised 
    reading list of 5 books
- Each email shows book covers, author, price, and a Shop Now CTA

**Wishlist Demand Signal Tab**
- Shows out-of-stock titles aggregated from wishlist data
- Demand bar and urgency flag (Urgent Restock / Monitor Closely)
- Connects customer-facing wishlist feature to Popular's 
  supply chain procurement decisions
- Sample push notification mock-up showing what the 
  restock alert looks like on a customer's phone

---

## Homepage (`index.html`) — ML Integration Points

The recommendation engine connects to the homepage in 6 places:

| Location | Feature | Model Used |
|---|---|---|
| Product grid | "Customers also bought" row on product modal | MBA |
| Search results | "You might also like" strip | MBA |
| Cart modal | Trade-In nudge for books in cart | — |
| Announcement bar | Personalised promotion | — |
| Post-purchase | Email sequence trigger | MBA + CF |
| Wishlist | Out-of-stock alert + restock notification | Demand signal |

---

## Student Analysis (`student-analysis.html`)

> _Section to be filled in by subscription team_

---

## Subscription Page (`subcription.html`)

> _Section to be filled in by subscription team_

---

## Book Preview (`book-preview.html`)

> _Section to be filled in by subscription team_

---

## Viewer (`viewer.html`)

> _Section to be filled in by subscription team_

---

## Trade-In Page (`tradein.html`)

Full walkthrough of the 4-step book trade-in flow.

### Step 1 — Scan & Value

1. **Scan barcode** — Click the camera zone to simulate a barcode scan. 
   It auto-fills with a sample book.
2. **Or type manually** — Type a book title (e.g. `PSLE Mathematics`) 
   or ISBN into the text field, then click **Get Credit Estimate →**.
3. A book card appears with the title, publisher, and tags.
4. **Select a condition** — Choose Good, Fair, or Worn. Each shows a 
   different credit value.
   - Click **"See condition examples"** to expand a guide showing what 
     each condition looks like.
5. A **credit offer box** appears showing:
   - Your offer amount in SGD
   - A demand meter (Low / Normal / High)
   - Click **"How is this price calculated?"** to see the base price 
     and demand multiplier breakdown.
6. Click **Accept Offer & Choose Outlet →** to proceed.

---

### Step 2 — Choose Outlet

1. **Search** by outlet name or area (e.g. `Tampines`, `Orchard`).
2. **Filter by region** using the tabs: All / Central / North / East / 
   West / North-East.
3. Click any outlet row to select it — a red tick appears.
4. Click **Confirm Outlet →** to proceed.

---

### Step 3 — Confirm

1. Review the trade-in summary: book, condition, credit amount, 
   outlet details.
2. Click **Generate TradeIn QR →** to proceed.

---

### Step 4 — QR Code

1. A QR code is shown. In a real scenario, the customer shows this 
   to staff at the counter.
2. **To simulate the staff scan** — click the QR code.
3. The page transitions to the **Credits Confirmed** screen showing:
   - Amount credited to Popular Wallet
   - Updated wallet balance
   - EduPass subscription recommendation banner — click 
     **Subscribe now →** to go to `subcription.html`
4. Click **Trade In Another Book** to restart, or **Back to Home** 
   to return to `index.html`.

---

## Python Analytics (`recommendation_engine.py`)

The recommendation engine that powers `recommendations.html`.

### Requirements
```
pip install pandas numpy scikit-learn mlxtend --break-system-packages
```

### Files
| File | Purpose |
|---|---|
| `recommendation_engine.py` | Main Python model |
| `purchases.csv` | Mock transaction data (60 records, 20 users, 14 books) |
| `books.csv` | Book metadata (title, author, genre, price, cover URL) |
| `recommendations_output.json` | Model output consumed by `recommendations.html` |

### How to Run
```bash
cd path/to/project
python recommendation_engine.py
```
Output is printed to console and written to 
`recommendations_output.json` automatically.

### Models
**Model 1 — Market Basket Analysis (Apriori)**
- Builds binary user-item matrix from purchase data
- Parameters: min_support=0.15, min_lift=1.2
- Output: Association rules ranked by lift
- Powers: product page "also bought" row, Email 1, Smart Search

**Model 2 — Collaborative Filtering (Cosine Similarity)**
- Builds user-item rating matrix
- Finds top-5 most similar users via pairwise cosine similarity
- Recommends unread books from similar users weighted by score
- Powers: Email 3 personalised reading list, Collab tab

**Demand Signal (Wishlist Aggregation)**
- Aggregates wishlist counts for out-of-stock titles
- Flags titles with 4+ wishlists as urgent restock
- Powers: Wishlist tab demand table, supply chain procurement signal

---

## Navigating Between Pages

| From | To | How |
|---|---|---|
| `index.html` | `click-collect.html` | Click & Collect button in carousel or nav |
| `index.html` | `tradein.html` | Announcement bar, nav, Trade-In strip, cart modal |
| `index.html` | `subcription.html` | Subscription slide in carousel, membership modal |
| `index.html` | `recommendations.html` | Via browser directly (IS215 demo) |
| `tradein.html` | `subcription.html` | EduPass banner after trade-in completion |
| `tradein.html` | `index.html` | "Back to Home" button on confirmation screen |
| `click-collect.html` | `index.html` | Header logo |
| `recommendations.html` | `index.html` | Header logo, nav Home link |