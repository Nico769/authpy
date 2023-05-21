import logging

from flask import Flask, jsonify
from playwright.async_api import async_playwright, expect

app = Flask(__name__)
# Configure Flask logger
app.logger.setLevel(logging.INFO)


async def parse_mocklab():
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        await page.goto("http://localhost:8080/oauth2/authorization/mock-oauth2")
        await page.locator('input[name="email"]').fill("dev@dev.it")
        await page.locator('input[name="password"]').fill("1")
        await page.get_by_role("button", name="Login").click()
        await page.goto("http://localhost:8080/user")
        await expect(page.get_by_text("You logged in with email")).to_be_visible()

        await context.close()
        await browser.close()

        # return "email"


@app.route("/interceptor", methods=["GET"])
async def interceptor():
    # email_text = await parse_mocklab()
    await parse_mocklab()

    # if not email_text:
    #     return jsonify({"error": "Parsing failed"}, 500)

    return "OK"


if __name__ == "__main__":
    app.run()
