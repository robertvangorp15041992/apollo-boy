# scraper.py
from playwright.sync_api import sync_playwright
import time

def scrape_apollo_contacts(company_url):
    contacts = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        print(f"🌐 Navigating to {company_url}")
        page.goto(company_url)

        # Login step (only once if needed)
        # page.fill("input[type='email']", "your_email")
        # page.fill("input[type='password']", "your_password")
        # page.click("button[type='submit']")
        # page.wait_for_timeout(5000)

        # Wait for contact list to load
        page.wait_for_selector("div[data-testid='contacts-section']")

        while True:
            # Scrape current page contacts
            elements = page.query_selector_all("div[data-testid='contact-row']")
            for el in elements:
                try:
                    name = el.query_selector("a[data-testid='contact-name-link']").inner_text()
                    title = el.query_selector("div[data-testid='contact-title']").inner_text()
                    email_button = el.query_selector("button[data-testid='reveal-email-button']")
                    email_button.click()
                    time.sleep(1)
                    email = el.query_selector("a[href^='mailto:']").inner_text()

                    contacts.append({
                        "Name": name,
                        "Title": title,
                        "Email": email
                    })
                except Exception as e:
                    print(f"⚠️ Skipping contact due to error: {e}")
                    continue

            # Try to go to the next page
            next_btn = page.query_selector("button[aria-label='Next Page']")
            if next_btn and not next_btn.is_disabled():
                next_btn.click()
                page.wait_for_timeout(3000)
            else:
                break

        browser.close()
    return contacts
