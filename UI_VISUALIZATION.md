# IQRA OPTION ANALYZER - UI Visualization

Hello! Since you asked for a visualization of the application's interface, I've created this file to describe it for you.

The application is a single-page dashboard with a dark theme navigation bar at the top and a light-themed main content area. Here is a section-by-section breakdown:

---

### 1. Navigation Bar
- A simple, dark navigation bar at the very top of the page.
- On the left, it says **"IQRA OPTION ANALYZER"**.

---

### 2. Main Dashboard Title
- Below the navbar, there is a main heading: **"Market Analysis Dashboard"**.

---

### 3. Index Overview (Top Section)
- This section contains two cards side-by-side:
    - **NIFTY 50 Card:**
        - Header: "NIFTY 50"
        - Body: Shows the latest price (e.g., "23,456.78") and the daily change below it (e.g., "+50.10 (0.21%)"). The change is colored green for positive and red for negative.
    - **BANK NIFTY Card:**
        - Similar to the NIFTY 50 card, but for the "NIFTY BANK" index.

---

### 4. Symbol Input
- A full-width input field where you can type a stock symbol (e.g., "RELIANCE").
- Next to it is a blue button labeled **"Fetch Data"**.

---

### 5. Analytics Section (Appears after fetching data)
This section appears below the input field once you fetch data for a symbol. It contains:

#### a. Key Metrics
- Two cards side-by-side:
    - **PCR (Put-Call Ratio) Card:** Shows the calculated PCR value (e.g., "0.95").
    - **Max Pain Card:** Shows the calculated Max Pain strike price (e.g., "23,500").

#### b. Open Interest Chart
- A large card with the title **"Open Interest by Strike Price"**.
- Inside is a **bar chart**:
    - The x-axis shows all the different strike prices.
    - For each strike price, there are two bars:
        - A **red bar** for Call Open Interest.
        - A **green bar** for Put Open Interest.
    - You can hover over the bars to see the exact OI values.

#### c. Option Chain Table
- This is the most detailed part of the dashboard. It's a very wide table that is horizontally scrollable.
- It has two main sections, **CALLS** on the left and **PUTS** on the right, with the **Strike Price** in the center.
- The columns for both Calls and Puts are:
    - **Delta, Gamma, Vega, Theta:** The calculated Option Greeks.
    - **IV:** Implied Volatility.
    - **OI:** Open Interest.
    - **Chng in OI:** Change in Open Interest.
    - **Volume:** Total traded volume.
    - **LTP:** Last Traded Price (colored green/red based on change).

---

### 6. Weekly Watchlist (Bottom of the page)
- A table with the heading **"Weekly Watchlist"**.
- It automatically loads a list of stocks that meet a basic "positive momentum" criteria.
- The columns are: **Symbol, Reason, Current Price, Volume, OI Change**.

---

I hope this detailed description gives you a clear picture of what the "IQRA OPTION ANALYZER" looks like! You can see it live by running the provided code.
