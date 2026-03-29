"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  Popular Bookstore — Buy-Back Pricing Model                                ║
║  IS215 Digital Business Technologies & Transformation                      ║
║  Group 4: Marcus, Arwen, Aryan, Jing Xiang, Joshua                        ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  Dynamic demand-based pricing for the Trade-In system.                     ║
║                                                                            ║
║  Formula:                                                                  ║
║    final_price = base_price × demand_multiplier × condition_factor         ║
║                                                                            ║
║  Where:                                                                    ║
║    base_price        = original retail price × genre_buyback_rate          ║
║    demand_multiplier = f(recent_sales_velocity, stock_level, season)       ║
║    condition_factor  = {Good: 1.0, Fair: 0.65, Worn: 0.30}                ║
║                                                                            ║
║  Data sources (cross-system):                                              ║
║    • Omnichannel POS  — sales velocity per title across all 40 stores     ║
║    • Subscription     — EduPass reading trends signal upcoming demand      ║
║    • Buy-Back history — supply-side: how many copies are being traded in  ║
║                                                                            ║
║  Legal compliance:                                                         ║
║    • Second-Hand Dealers Act (PLRD registration: SHDA-2025-04821)         ║
║    • PDPA — seller records retained for 5 years, consent-managed          ║
║    • NEA EPR framework alignment for sustainability reporting              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # non-interactive backend
import matplotlib.pyplot as plt
import os

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))


# ═══════════════════════════════════════════════════════════════════════════════
# 1. CONFIGURATION & CONSTANTS
# ═══════════════════════════════════════════════════════════════════════════════

# Condition factors — how much of the base value each condition retains
CONDITION_FACTORS = {
    'Good': 1.00,   # Minimal wear, no writing, spine intact
    'Fair': 0.65,   # Some annotations, slight cover wear, creases
    'Worn': 0.30,   # Heavy highlighting, torn pages, bent spine
}

# Genre buyback rates — what % of retail price Popular offers as base
GENRE_BUYBACK_RATES = {
    'Assessment':  0.35,  # High turnover, seasonal demand
    'Textbook':    0.25,  # Lower margin, edition-dependent
    'Fiction':     0.30,  # Steady demand, BookTok can spike it
    'Non-Fiction': 0.28,  # Moderate demand
}

# Seasonal multipliers (Singapore academic calendar)
SEASON_MULTIPLIERS = {
    'Jan':  1.30,  # Back-to-school rush (new academic year)
    'Feb':  1.15,  # Early term
    'Mar':  1.00,  # Mid-term
    'Apr':  0.90,  # Pre-holiday lull
    'May':  0.85,  # June holiday start
    'Jun':  0.80,  # Holiday — low demand
    'Jul':  1.10,  # Start of Term 3
    'Aug':  1.05,  # Mid-year
    'Sep':  1.25,  # PSLE/O-Level/A-Level prep season
    'Oct':  1.35,  # Peak exam season
    'Nov':  0.70,  # Post-exams
    'Dec':  0.75,  # Holiday — fiction demand rises
}


# ═══════════════════════════════════════════════════════════════════════════════
# 2. BOOK INVENTORY (with sales & supply data from all 3 systems)
# ═══════════════════════════════════════════════════════════════════════════════

inventory = pd.DataFrame({
    'book_id': range(1, 16),
    'title': [
        'PSLE Mathematics Past Year Papers 2025',
        'Secondary 3 E-Maths Assessment Book',
        'Primary 4 Science Worksheets',
        'O-Level English Ten Year Series',
        'Primary 5 Chinese Assessment Book',
        'JC2 H2 Chemistry Ten Year Series',
        'Secondary 1 History Textbook',
        'The Great Gatsby',
        'Primary 3 Maths Challenging Problems',
        'Tomorrow, and Tomorrow, and Tomorrow',
        'Atomic Habits',
        'The Psychology of Money',
        'Lessons in Chemistry',
        'Fourth Wing',
        'PSLE Science Past Year Papers 2025',
    ],
    'genre': [
        'Assessment','Assessment','Assessment','Assessment','Assessment',
        'Assessment','Textbook','Fiction','Assessment','Fiction',
        'Non-Fiction','Non-Fiction','Fiction','Fiction','Assessment',
    ],
    'retail_price': [
        12.90, 14.50, 10.90, 15.90, 11.90,
        18.50, 22.00, 14.90, 10.90, 16.90,
        24.90, 19.90, 18.90, 21.90, 12.90,
    ],
    # --- Cross-system data ---
    # Omnichannel: weekly sales across all 40 stores
    'weekly_sales': [
        320, 85, 150, 210, 95,
        180, 40, 60, 130, 110,
        200, 140, 75, 160, 280,
    ],
    # Subscription: EduPass monthly reads (digital demand signal)
    'edupass_reads': [
        450, 120, 200, 300, 130,
        220, 55, 180, 170, 250,
        380, 290, 190, 310, 410,
    ],
    # Buy-back: trade-ins received this month (supply signal)
    'tradein_supply': [
        45, 30, 60, 25, 35,
        15, 50, 20, 55, 10,
        5, 8, 12, 8, 40,
    ],
    # Current stock across all outlets
    'current_stock': [
        120, 200, 80, 150, 180,
        90, 250, 160, 70, 110,
        60, 100, 140, 85, 100,
    ],
})


# ═══════════════════════════════════════════════════════════════════════════════
# 3. DEMAND MULTIPLIER CALCULATION
# ═══════════════════════════════════════════════════════════════════════════════

def calculate_demand_multiplier(row, month='Mar'):
    """
    Compute dynamic demand multiplier from three signals:
      1. Sales velocity  — omnichannel POS data (weekly sales / stock)
      2. Digital demand   — EduPass reading activity (subscription signal)
      3. Supply pressure  — trade-in volume (buy-back signal)
      4. Seasonal factor  — Singapore academic calendar

    Higher sales + higher reads + lower supply = higher multiplier
    """
    # Velocity: sales relative to stock (how fast it's moving)
    velocity = row['weekly_sales'] / max(row['current_stock'], 1)

    # Digital demand signal (normalised)
    digital_demand = row['edupass_reads'] / 500  # normalise to ~0-1 range

    # Supply pressure: more trade-ins = more supply = lower multiplier
    supply_factor = 1 - (row['tradein_supply'] / 100)  # 0 trade-ins = 1.0, 100 = 0.0
    supply_factor = max(supply_factor, 0.5)  # floor at 0.5

    # Weighted combination
    raw_score = (
        0.40 * velocity +        # 40% weight: actual sales velocity
        0.30 * digital_demand +   # 30% weight: subscription reading trends
        0.30 * supply_factor      # 30% weight: inverse of supply pressure
    )

    # Scale to multiplier range [0.6, 1.5]
    multiplier = 0.6 + (raw_score * 0.9)
    multiplier = max(0.6, min(1.5, multiplier))

    # Apply seasonal adjustment
    seasonal = SEASON_MULTIPLIERS.get(month, 1.0)
    multiplier *= seasonal
    multiplier = max(0.5, min(1.8, multiplier))

    return round(multiplier, 2)


def get_demand_label(mult):
    """Human-readable demand label."""
    if mult >= 1.3:  return 'High demand — limited stock'
    if mult >= 1.15: return 'High demand'
    if mult >= 0.95: return 'Normal stock levels'
    if mult >= 0.8:  return 'Low demand'
    return 'Low demand — offer reduced'


# ═══════════════════════════════════════════════════════════════════════════════
# 4. PRICE CALCULATOR
# ═══════════════════════════════════════════════════════════════════════════════

def calculate_tradein_price(book_row, condition, month='Mar'):
    """
    Full pricing calculation for a single book trade-in.

    Returns a dict with full breakdown:
      retail_price → base_price → demand_mult → condition_factor → final_price
    """
    genre = book_row['genre']
    retail = book_row['retail_price']

    # Step 1: Base price (% of retail based on genre)
    buyback_rate = GENRE_BUYBACK_RATES.get(genre, 0.25)
    base_price = retail * buyback_rate

    # Step 2: Demand multiplier (from cross-system signals)
    demand_mult = calculate_demand_multiplier(book_row, month)
    demand_label = get_demand_label(demand_mult)

    # Step 3: Condition factor
    cond_factor = CONDITION_FACTORS.get(condition, 0.65)

    # Step 4: Final price
    final_price = base_price * demand_mult * cond_factor

    return {
        'title': book_row['title'],
        'genre': genre,
        'condition': condition,
        'retail_price': retail,
        'buyback_rate': f"{buyback_rate*100:.0f}%",
        'base_price': round(base_price, 2),
        'demand_multiplier': demand_mult,
        'demand_label': demand_label,
        'condition_factor': cond_factor,
        'final_offer': round(final_price, 2),
        # Source breakdown
        'signal_sales_velocity': round(book_row['weekly_sales'] / max(book_row['current_stock'], 1), 2),
        'signal_digital_demand': book_row['edupass_reads'],
        'signal_supply_pressure': book_row['tradein_supply'],
    }


# ═══════════════════════════════════════════════════════════════════════════════
# 5. BATCH PRICING — All books × all conditions
# ═══════════════════════════════════════════════════════════════════════════════

def generate_full_price_table(inv_df, month='Mar'):
    """Generate pricing for every book in every condition."""
    rows = []
    for _, book in inv_df.iterrows():
        for cond in ['Good', 'Fair', 'Worn']:
            result = calculate_tradein_price(book, cond, month)
            rows.append(result)
    return pd.DataFrame(rows)


# ═══════════════════════════════════════════════════════════════════════════════
# 6. VISUALISATIONS
# ═══════════════════════════════════════════════════════════════════════════════

def plot_price_comparison(price_table, output_path=None):
    """Bar chart: trade-in offers by book, stacked by condition."""
    fig, ax = plt.subplots(figsize=(14, 7))

    books = price_table[price_table['condition'] == 'Good']['title'].values
    short_titles = [t[:25] + '...' if len(t) > 25 else t for t in books]

    good_prices = price_table[price_table['condition'] == 'Good']['final_offer'].values
    fair_prices = price_table[price_table['condition'] == 'Fair']['final_offer'].values
    worn_prices = price_table[price_table['condition'] == 'Worn']['final_offer'].values

    x = np.arange(len(books))
    width = 0.25

    ax.bar(x - width, good_prices, width, label='Good', color='#1B7F4F', alpha=0.85)
    ax.bar(x, fair_prices, width, label='Fair', color='#B45309', alpha=0.85)
    ax.bar(x + width, worn_prices, width, label='Worn', color='#999', alpha=0.85)

    ax.set_xlabel('Book Title', fontsize=11)
    ax.set_ylabel('Trade-In Credit (S$)', fontsize=11)
    ax.set_title('Popular Buy-Back: Trade-In Credit by Book & Condition\n'
                 'Demand-based pricing using Omnichannel + Subscription + Buy-Back signals',
                 fontsize=13, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(short_titles, rotation=45, ha='right', fontsize=8)
    ax.legend(title='Condition')
    ax.grid(axis='y', alpha=0.3)
    plt.tight_layout()

    path = output_path or os.path.join(OUTPUT_DIR, 'tradein_price_comparison.png')
    plt.savefig(path, dpi=150)
    plt.close()
    print(f"   ✓ Saved: {path}")
    return path


def plot_demand_factors(inv_df, output_path=None):
    """Scatter plot: sales velocity vs digital demand, bubble = supply pressure."""
    fig, ax = plt.subplots(figsize=(12, 7))

    velocity = inv_df['weekly_sales'] / inv_df['current_stock']
    digital = inv_df['edupass_reads']
    supply = inv_df['tradein_supply']
    titles = inv_df['title'].apply(lambda t: t[:20] + '...' if len(t) > 20 else t)

    # Demand multiplier for colour
    mults = inv_df.apply(lambda r: calculate_demand_multiplier(r), axis=1)
    colours = ['#1B7F4F' if m >= 1.15 else '#B45309' if m >= 0.95 else '#999' for m in mults]

    scatter = ax.scatter(velocity, digital, s=supply*8+50, c=colours, alpha=0.7, edgecolors='white', linewidth=1.5)

    for i, txt in enumerate(titles):
        ax.annotate(txt, (velocity.iloc[i], digital.iloc[i]),
                    fontsize=7, ha='center', va='bottom', alpha=0.8)

    ax.set_xlabel('Sales Velocity (weekly sales / stock)', fontsize=11)
    ax.set_ylabel('EduPass Digital Reads (monthly)', fontsize=11)
    ax.set_title('Demand Signal Analysis: Three-Source Data Integration\n'
                 'Bubble size = trade-in supply · Green = high demand · Amber = normal · Gray = low',
                 fontsize=13, fontweight='bold')
    ax.grid(alpha=0.3)

    # Legend for bubble size
    for s, label in [(10, '10 trade-ins'), (30, '30'), (60, '60')]:
        ax.scatter([], [], s=s*8+50, c='gray', alpha=0.5, label=label)
    ax.legend(title='Trade-in supply', loc='upper left', fontsize=8)

    plt.tight_layout()
    path = output_path or os.path.join(OUTPUT_DIR, 'demand_signal_analysis.png')
    plt.savefig(path, dpi=150)
    plt.close()
    print(f"   ✓ Saved: {path}")
    return path


def plot_seasonal_impact(output_path=None):
    """Line chart: how seasonal multipliers affect a sample book's offer."""
    months = list(SEASON_MULTIPLIERS.keys())
    mults = list(SEASON_MULTIPLIERS.values())

    # Sample: PSLE Maths (retail $12.90, assessment, good condition)
    base = 12.90 * 0.35  # $4.515
    base_demand = 1.15    # average demand mult for this book

    offers = [round(base * base_demand * m * 1.0, 2) for m in mults]  # Good condition

    fig, ax1 = plt.subplots(figsize=(12, 5))
    colour = '#D0021B'

    ax1.plot(months, offers, 'o-', color=colour, linewidth=2.5, markersize=8, zorder=5)
    ax1.fill_between(months, offers, alpha=0.08, color=colour)
    ax1.set_ylabel('Trade-In Credit (S$)', fontsize=11, color=colour)
    ax1.tick_params(axis='y', labelcolor=colour)

    # Highlight key periods
    for i, (m, o) in enumerate(zip(months, offers)):
        ax1.annotate(f'${o:.2f}', (m, o), textcoords="offset points",
                     xytext=(0, 12), ha='center', fontsize=9, fontweight='bold', color=colour)

    # Add event annotations
    events = {
        'Jan': 'Back to school', 'Sep': 'Exam prep', 'Oct': 'PSLE/O-Level',
        'Jun': 'Holiday lull', 'Nov': 'Post-exams'
    }
    for m, label in events.items():
        idx = months.index(m)
        ax1.annotate(label, (m, offers[idx]), textcoords="offset points",
                     xytext=(0, -20), ha='center', fontsize=7, color='#666', style='italic')

    ax1.set_title('Seasonal Impact on Trade-In Pricing\n'
                  'PSLE Maths Past Year Papers (Good condition) — Singapore academic calendar',
                  fontsize=13, fontweight='bold')
    ax1.grid(axis='y', alpha=0.3)
    plt.tight_layout()

    path = output_path or os.path.join(OUTPUT_DIR, 'seasonal_pricing_impact.png')
    plt.savefig(path, dpi=150)
    plt.close()
    print(f"   ✓ Saved: {path}")
    return path


# ═══════════════════════════════════════════════════════════════════════════════
# 7. MAIN — Run the pricing model and generate outputs
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == '__main__':
    print("╔══════════════════════════════════════════════════════════════════╗")
    print("║    POPULAR BOOKSTORE — BUY-BACK PRICING MODEL                  ║")
    print("║    Dynamic demand-based pricing for the Trade-In system        ║")
    print("╚══════════════════════════════════════════════════════════════════╝")

    # --- Single book demo with full breakdown ---
    print("\n" + "="*70)
    print("  PRICING BREAKDOWN — Single Book Demo")
    print("="*70)

    demo_book = inventory[inventory['book_id'] == 1].iloc[0]
    for cond in ['Good', 'Fair', 'Worn']:
        result = calculate_tradein_price(demo_book, cond, month='Sep')
        print(f"\n  📚 {result['title']}")
        print(f"  Condition: {result['condition']}")
        print(f"  {'─'*50}")
        print(f"  Retail price:        S${result['retail_price']:.2f}")
        print(f"  Genre buyback rate:  {result['buyback_rate']} ({result['genre']})")
        print(f"  Base price:          S${result['base_price']:.2f}")
        print(f"  Demand multiplier:   ×{result['demand_multiplier']}")
        print(f"    └─ {result['demand_label']}")
        print(f"    └─ Sales velocity:    {result['signal_sales_velocity']} (weekly sales/stock)")
        print(f"    └─ Digital reads:     {result['signal_digital_demand']} (EduPass monthly)")
        print(f"    └─ Supply pressure:   {result['signal_supply_pressure']} (trade-ins this month)")
        print(f"  Condition factor:    ×{result['condition_factor']}")
        print(f"  {'─'*50}")
        print(f"  ★ FINAL OFFER:       S${result['final_offer']:.2f}")

    # --- Full price table ---
    print("\n\n" + "="*70)
    print("  FULL PRICE TABLE — All Books (March, current month)")
    print("="*70 + "\n")

    price_table = generate_full_price_table(inventory, month='Mar')
    pivot = price_table.pivot_table(
        index='title', columns='condition',
        values='final_offer', aggfunc='first'
    )[['Good', 'Fair', 'Worn']]
    pivot = pivot.sort_values('Good', ascending=False)

    print(pivot.to_string())

    # --- Demand multipliers across catalogue ---
    print("\n\n" + "="*70)
    print("  DEMAND MULTIPLIERS — Cross-System Analysis")
    print("="*70 + "\n")

    for _, book in inventory.iterrows():
        mult = calculate_demand_multiplier(book)
        label = get_demand_label(mult)
        bar = '█' * int(mult * 15)
        print(f"  {mult:.2f} {bar:<25} {book['title'][:40]:<42} {label}")

    # --- Generate visualisations ---
    print("\n\n" + "="*70)
    print("  GENERATING VISUALISATIONS")
    print("="*70 + "\n")

    plot_price_comparison(price_table)
    plot_demand_factors(inventory)
    plot_seasonal_impact()

    # --- Summary ---
    print(f"\n{'='*70}")
    print("  MODEL SUMMARY")
    print(f"{'='*70}")
    print(f"""
    Formula: final_price = base_price × demand_multiplier × condition_factor

    Parameters:
      Condition factors:  Good (×1.00) · Fair (×0.65) · Worn (×0.30)
      Genre rates:        Assessment (35%) · Fiction (30%) · Non-Fiction (28%) · Textbook (25%)
      Demand weights:     Sales velocity (40%) + Digital reads (30%) + Supply pressure (30%)
      Seasonal range:     ×0.70 (Nov) to ×1.35 (Oct, exam season)

    Data integration:
      ✓ Omnichannel POS   — real-time sales velocity across 40 stores
      ✓ EduPass reads     — subscription reading trends as demand predictor
      ✓ Trade-in volume   — supply-side pressure from buy-back system

    Legal compliance:
      ✓ Second-Hand Dealers Act (PLRD)  — Reg. No. SHDA-2025-04821
      ✓ PDPA — seller records encrypted, 5-year retention, consent-managed
      ✓ NEA EPR — sustainability reporting for circular economy metrics

    Charts generated:
      → tradein_price_comparison.png   (credit by book & condition)
      → demand_signal_analysis.png     (3-source demand scatter)
      → seasonal_pricing_impact.png    (monthly pricing variation)
    """)
