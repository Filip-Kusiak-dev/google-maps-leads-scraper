# 📍 Google Maps B2B Lead Scraper (Python + Playwright)

Advanced lead generation tool designed to extract business data from Google Maps. Unlike basic scrapers, this bot handles **Infinite Scroll (Lazy Loading)** and simulates human behavior to retrieve deep details directly from the side panel.

## 🚀 Key Features

* **Infinite Scroll Handling:** Automatically detects the feed container and scrolls via JavaScript injection until the target count is reached.
* **Deep Extraction:** Clicks into each listing to retrieve details hidden in the side panel.
* **Data Points Extracted:**
    * ✅ Business Name
    * ✅ **Verified Phone Number**
    * ✅ **Website URL**
    * ✅ Full Address
    * ✅ Rating & Review Count
* **Localization:** Forces `pl-PL` locale to ensure consistent data parsing.
* **Smart Selectors:** Uses `data-item-id` attributes to accurately identify phone numbers and addresses regardless of the UI language.

## 🛠️ Tech Stack
* Python 3.11+
* Playwright (Browser Automation)
* Pandas (Excel Export)

## 📊 Sample Output
Check the `.xlsx` file in this repository to see a sample of leads generated automatically.

---
*Developed for automated B2B Lead Generation.*
