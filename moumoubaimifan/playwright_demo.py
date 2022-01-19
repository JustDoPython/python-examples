from playwright.sync_api import Playwright, sync_playwright


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()

    # Open new page
    page = context.new_page()

    # Go to https://www.jd.com/
    page.goto("https://www.jd.com/")

    # Click text=女鞋
    with page.expect_popup() as popup_info:
        page.click("text=女鞋")
    page1 = popup_info.value

    # Click div:nth-child(2) .lc-shop-logo-vertical__item-container div:nth-child(2) .lc-shop-logo-vertical__logo-cover .lc-shop-logo-vertical__logo
    with page1.expect_popup() as popup_info:
        page1.click("div:nth-child(2) .lc-shop-logo-vertical__item-container div:nth-child(2) .lc-shop-logo-vertical__logo-cover .lc-shop-logo-vertical__logo")
    page2 = popup_info.value

    # Click :nth-match(:text("每满200减30"), 2)
    with page1.expect_popup() as popup_info:
        page1.click(":nth-match(:text(\"每满200减30\"), 2)")
    page3 = popup_info.value

    # Close page
    page2.close()

    # Close page
    page3.close()

    # Close page
    page1.close()

    # Close page
    page.close()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
