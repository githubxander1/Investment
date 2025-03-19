from playwright.sync_api import Playwright, sync_playwright, expect

def run(playwright: Playwright, email) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("http://paylabs-test.com/merchant/paylabs-register-register.html#")
    page.locator("span").filter(has_text="id").first.click()
    page.get_by_role("link", name="EN", exact=True).click()

    page.get_by_role("textbox", name="E-mail *", exact=True).fill(email)
    page.get_by_role("textbox", name="Email Verification Code *").fill("652266")
    page.locator("#phone").fill("15318544125")
    page.locator("#phoneCode").fill("652266")
    page.get_by_role("textbox", name="Secure Email for fund account").fill(email)
    page.get_by_role("textbox", name="Please enter contact").fill(email)#PIC名字
    page.get_by_role("textbox", name="Password *" , exact=True).fill("Abc@123456789")
    page.get_by_role("textbox", name="Confirm password *", exact=True).fill("Abc@123456789")
    page.locator("#invitation_code").fill("123456")
    page.get_by_role("button", name="Register").click()
    # page.pause()
    page.get_by_role("button", name="I have read and agree to the").click()#同意

    page.wait_for_timeout(5000)

    if not expect(page.locator("#inputEmail")).to_contain_text("The E-mail has been registered"):
        print("注册失败：邮箱已被注册")
    else:
        print("注册成功")


    # ---------------------
    context.close()
    browser.close()
if __name__ == '__main__':

    with sync_playwright() as playwright:
        run(playwright, 'paylabs4@test.com')
