from playwright.sync_api import sync_playwright
import time
import random


def create_linkedin_account(name, email, password):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=100)  # set headless=True later
        context = browser.new_context(
            viewport={"width": 1280, "height": 800},
            user_agent=random.choice([
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
                "Mozilla/5.0 (X11; Linux x86_64)"
            ])
        )
        page = context.new_page()

        print("Opening LinkedIn signup page...")
        page.goto("https://www.linkedin.com/signup")

        time.sleep(2)
        print("Filling email and password...")
        page.fill("input[name='email-or-phone']", email)
        page.fill("input[name='password']", password)
        page.click("button[type='submit']")

        time.sleep(3)

        print("Filling name...")
        page.fill("input#first-name", name.split()[0])
        page.fill("input#last-name", name.split()[1])
        page.click("button[type='submit']")

        time.sleep(3)

        # Stop before confirmation step
        print("Stopped at confirmation step. Complete email verification manually.")
        browser.close()
