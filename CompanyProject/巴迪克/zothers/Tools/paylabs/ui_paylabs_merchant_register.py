#paylabs商户注册
from playwright.sync_api import Playwright, expect

def paylabs_merchant_register(playwright: Playwright, email) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    # page.goto("http://paylabs-test.com/merchant/paylabs-register-register.html#")
    page.goto("https://sitch-merchant.paylabs.co.id/paylabs-register-register.html")
    page.locator("span").filter(has_text="id").first.click()
    page.get_by_role("link", name="EN", exact=True).click()

    page.get_by_role("textbox", name="E-mail *", exact=True).fill(email)
    page.get_by_role("textbox", name="Email Verification Code *").fill("652266")
    page.locator("#phone").fill("15318544125")
    page.locator("#phoneCode").fill("652266")
    page.get_by_role("textbox", name="Secure Email for fund account").fill(email)
    page.get_by_role("textbox", name="Please enter contact").fill(email)#PIC名字
    # page.get_by_role("textbox", name="Password *" , exact=True).fill("Abc@123456789")
    page.get_by_role("textbox", name="Password *" , exact=True).fill("A123456@test")
    page.get_by_role("textbox", name="Confirm password *", exact=True).fill("A123456@test")
    page.locator("#invitation_code").fill("123456")
    page.get_by_role("button", name="Register").click()

    page.get_by_role("button", name="I have read and agree to the").click()#同意
    gologin = page.locator("#gologin")

    try:
        # 检查邮箱是否已注册
        expect(page.locator("#inputEmail")).to_contain_text("The E-mail has been registered")
        print("邮箱已注册！")
    except AssertionError:
        gologin.wait_for(state='visible',timeout=10000)
        if gologin.is_visible():
            print("注册成功")
        else:
            print("未找到 'gologin' 元素或其不可见")
    except Exception as e:
        print(f"发生未知错误: {e}")

    # ---------------------
    context.close()
    browser.close()
