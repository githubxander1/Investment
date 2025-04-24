with page.expect_popup() as page4_info:
    page.get_by_role("link", name="Go to login").click()
page4 = page4_info.value
page4.get_by_role("textbox", name="Email").click()
page4.get_by_role("textbox", name="Email").fill("2@tax.com")
page4.get_by_role("textbox", name="Password").click()
page4.get_by_role("textbox", name="Password").fill("A123456@test")
page4.get_by_role("button", name="Log In").click()