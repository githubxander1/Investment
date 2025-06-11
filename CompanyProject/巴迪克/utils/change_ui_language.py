
def change_ui_language(page, to_language):
    '''
    param: to_language:要切换成的语言
    '''
    language = page.locator(".lang-text")
    if language.text_content() != to_language:
        language.click()
        page.get_by_role("link", name=to_language).click()