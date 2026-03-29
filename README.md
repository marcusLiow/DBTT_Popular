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

### Python & Analytics Files

| File | Purpose |
|---|---|
| `recommendation_engine.py` | Apriori + Collaborative Filtering recommendation model |
| `pricing_model.py` | Dynamic buy-back pricing algorithm with cross-system demand signals |
| `Popular_Demographic_Analytics.ipynb` | K-Means + Random Forest persona prediction (87% accuracy) |
| `purchases.csv` | Mock transaction data (60 records, 20 users, 14 books) |
| `books.csv` | Book metadata (title, author, genre, price, cover URL) |
| `recommendations_output.json` | Model output consumed by `recommendations.html` |
| `confusion_matrix.png` | ML output — persona classifier accuracy matrix |
| `feature_importance.png` | ML output — genre is #1 predictor (47% importance) |
| `personas.png` | ML output — 5 customer persona clusters visualisation |

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

## Subscription Flow (`subcription.html` → `book-preview.html` → `viewer.html` → `student-analysis.html`)

Demonstrates the full EduPass subscription experience from browsing to learning analytics.

### Step 1 — Browse Library & Subscribe
1. Open `subcription.html` — the full EduPass book library
2. Click **Subscribe** in the nav bar to open the plans modal
3. Select a plan (Starter / Plus / Family) — the nav updates to show "Study Pass Active"
4. Browse the library of 25 EPH assessment books by level

### Step 2 — Select a Book
1. Click any book cover to open `book-preview.html`
2. View the book details: description, table of contents, sample questions
3. Click **Open E-reader** to proceed

### Step 3 — Read & Answer Questions
1. `viewer.html` opens with the workbook rendered page-by-page
2. Use the sidebar or arrow keys to navigate pages
3. For each page with questions, type answers into the input fields below the viewer
4. On the last page, click **Check Answers** to verify all fields are filled

### Step 4 — View Learning Report
1. Open `student-analysis.html` to see the student's progress dashboard
2. Shows: overall score, topic-level strengths and weaknesses, activity timeline
3. Weak topics are flagged and matched to recommended next books

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

### Sidebar Features

**Analytics Dashboard (collapsible)**
- Shows live persona prediction: selects a book → system predicts
  whether the trader is a Parent, Student, Bookworm, Self-Improver,
  or Budget Shopper, with animated probability bars
- Dynamic pricing signals panel showing the 3 cross-system demand
  inputs (Sales Velocity, EduPass reads, Trade-In supply) with their
  weights (40%/30%/30%)
- Cross-source integration diagram showing how data from all 3
  solutions (Omnichannel, Subscription, Trade-In) feeds the page

**Hero Stats Bar**
- $0 delivery fees, 3 min drop-off, 30+ outlets, books saved
  from landfill, credits returned to families

**Confirmation Enhancements**
- Email preview toggle showing a mock confirmation email with
  book, condition, credit, outlet, and reference number
- EduPass cross-sell upsell ("Your credit covers 1 month of EduPass")
- User details form (name + mobile for QR code)

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

## Dynamic Pricing Model (`pricing_model.py`)

The buy-back pricing algorithm that powers `tradein.html`'s credit offers.

### Formula
```
final_price = base_price × demand_multiplier × condition_factor
```

Where:
- `base_price` = retail price × genre buyback rate (Assessment 35%, Fiction 30%, etc.)
- `demand_multiplier` = weighted signal from 3 cross-system sources:
  - Omnichannel POS sales velocity (40% weight)
  - EduPass digital reading trends (30% weight)
  - Trade-in supply volume (30% weight)
- `condition_factor` = Good (1.0), Fair (0.65), Worn (0.30)
- Seasonal multiplier from Singapore academic calendar (Jan back-to-school 1.30× → Jun holiday 0.80×)

### How to Run
```bash
pip install pandas numpy matplotlib --break-system-packages
python pricing_model.py
```

Generates 3 charts in the project folder:
- `tradein_price_comparison.png` — credit offers across books by condition
- `demand_signal_analysis.png` — cross-system demand signals visualisation
- `seasonal_pricing_impact.png` — how Singapore school calendar affects pricing

### Legal Compliance
- Second-Hand Dealers Act (PLRD registration: SHDA-2025-04821)
- PDPA — seller records retained for 5 years, consent-managed
- NEA EPR framework alignment for sustainability reporting

---

## Persona Prediction (`Popular_Demographic_Analytics.ipynb`)

K-Means clustering + Random Forest classifier that predicts customer
personas from trade-in behaviour.

### 5 Customer Personas
| Persona | Key Signals |
|---|---|
| Parent | Assessment books, good condition, heartland mall outlets |
| Student | Assessment books, worn condition, post-exam timing |
| Bookworm | Fiction, good condition, city centre outlets |
| Self-Improver | Self-help/business, city outlets |
| Budget Shopper | Any genre, fair/worn condition |

### Results
- Random Forest accuracy: **87%**
- #1 feature: Genre (47% importance)
- Output charts: `confusion_matrix.png`, `feature_importance.png`, `personas.png`

### How to Run
```bash
pip install pandas numpy scikit-learn matplotlib seaborn --break-system-packages
jupyter notebook Popular_Demographic_Analytics.ipynb
```

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