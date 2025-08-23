import re
from playwright.sync_api import Playwright, sync_playwright
from pathlib import Path
import os
import time
import pyperclip
from prompt_toolkit.layout import to_container

# 获取当前脚本所在目录
script_dir = os.path.dirname(os.path.abspath(__file__))
auth_file = os.path.join(script_dir, "deepseek_login_state.json")

class DeepSeekClient:
    def __init__(self, headless=False):
        self.headless = headless
        self.browser = None
        self.context = None
        self.page = None

    def start_browser(self):
        """启动浏览器"""
        self.browser = playwright.chromium.launch(headless=self.headless)
        return self.browser

    def load_or_create_context(self):
        """加载或创建浏览器上下文"""
        if Path(auth_file).exists():
            # 如果存在登录状态文件，则加载已保存的登录状态
            self.context = self.browser.new_context(storage_state=auth_file)
            print("已加载登录状态")
        else:
            # 如果不存在，则创建新的上下文
            self.context = self.browser.new_context()
            print("创建新的浏览器上下文")
        return self.context

    def login_if_needed(self):
        """如果需要则进行登录"""
        if not Path(auth_file).exists():
            print("正在登录...")
            page = self.context.new_page()
            page.goto("https://chat.deepseek.com/sign_in")
            page.get_by_text("密码登录").click()
            page.get_by_role("textbox", name="请输入手机号/邮箱地址").click()
            page.get_by_role("textbox", name="请输入手机号/邮箱地址").fill("19918754473")
            page.get_by_role("textbox", name="请输入密码").click()
            page.get_by_role("textbox", name="请输入密码").fill("ds0520@xl")
            page.get_by_role("button", name="登录").click()

            # 等待跳转到主页
            page.wait_for_url("https://chat.deepseek.com/", timeout=30000)

            # 保存登录状态
            self.context.storage_state(path=auth_file)
            print("登录状态已保存")
            page.close()

    def navigate_to_chat(self):
        """导航到聊天页面"""
        self.page = self.context.new_page()
        self.page.goto("https://chat.deepseek.com/")
        # 等待页面加载完成
        # self.page.wait_for_load_state("networkidle")
        print("已导航到聊天页面")
        return self.page

    def activate_deep_thinking(self):
        """激活深度思考模式"""
        try:
            deep_thinking_button = self.page.get_by_role("button", name="深度思考")
            if deep_thinking_button.is_visible():
                deep_thinking_button.click()
                print("✅ 已点击深度思考按钮")
            else:
                print("⚠️ 深度思考按钮不可见")
        except Exception as e:
            print(f"⚠️ 点击深度思考按钮时出错: {e}")

    def enable_web_search(self):
        """启用联网搜索"""
        try:
            search_button = self.page.get_by_role("button", name="联网搜索")
            if search_button.is_visible():
                search_button.click()
                print("✅ 已点击联网搜索按钮")
        except Exception as e:
            print(f"⚠️ 点击联网搜索按钮时出错: {e}")

    def send_message(self, message):
        """发送消息"""
        # 输入问题
        self.page.get_by_role("textbox", name="给 DeepSeek 发送消息").fill(message)
        print(f"📤 已输入问题: {message}")

        # 点击发送按钮
        try:
            # send_buttons = self.page.query_selector_all("button")
            send_button = self.page.get_by_role("button").filter(has_text=re.compile(r"^$"))
            # send_button = None
            # for btn in send_buttons:
            #     if btn.is_visible() and (btn.get_attribute("aria-label") == "发送" or
            #                            "发送" in btn.text_content() or
            #                            not btn.text_content().strip()):
            #         # 空文本或发送按钮
            #         send_button = btn
            #         break

            if send_button:
                send_button.click()
            else:
                # 使用回车键发送
                self.page.get_by_role("textbox", name="给 DeepSeek 发送消息").press("Enter")
            print("🚀 已发送问题")
        except Exception as e:
            print(f"⚠️ 发送问题时出错，尝试使用回车键: {e}")
            self.page.get_by_role("textbox", name="给 DeepSeek 发送消息").press("Enter")

    def wait_and_extract_content(self):
        """等待并提取回答内容"""
        print("等待回答完成...")
        # self.page.pause()

        try:
            # 等待深度思考完成或复制按钮出现
            print("⏳ 等待AI回答完成...")
            start_time = time.time()

            # 等待深度思考完成标识出现或者复制按钮出现
            max_wait_time = 90  # 最大等待时间90秒
            check_interval = 2   # 每2秒检查一次

            while time.time() - start_time < max_wait_time:
                elapsed_time = int(time.time() - start_time)
                print(f"\r⏰ 已等待 {elapsed_time} 秒", end="", flush=True)

                # 检查是否出现"已深度思考"
                try:
                    deep_thinking_element = self.page.get_by_text("已深度思考")
                    if deep_thinking_element.is_visible():
                        print(f"\n✅ 检测到'已深度思考'标识，用时 {elapsed_time} 秒")
                        break
                except:
                    pass

                # 检查是否出现复制按钮（SVG图标）
                try:
                    # 查找复制按钮，通过SVG图标定位
                    copy_button = self.page.locator(".ds-flex > .ds-flex > div > .ds-icon > svg").first
                    if copy_button.is_visible():
                        print(f"\n✅ 检测到复制按钮，AI回答已完成，用时 {elapsed_time} 秒")
                        break
                except:
                    pass

                # 等待下次检查
                time.sleep(check_interval)
            else:
                print(f"\n⚠️ 等待超时 ({max_wait_time} 秒)，继续尝试提取内容...")

            self.page.wait_for_timeout(75000)
            print("🔍 尝试查找复制按钮...")
            # 尝试多种方式找到复制按钮
            copy_button = self.page.locator(".ds-flex > .ds-flex > div > .ds-icon > svg")


            if copy_button:
                # 点击复制按钮
                copy_button.click()
                print("📌 已点击复制按钮")

                # 等待一小段时间确保复制完成
                time.sleep(1)

                # 尝试从剪贴板获取内容
                try:
                    clipboard_content = pyperclip.paste()
                    print(f"📋 剪贴板内容: {clipboard_content}")
                    return clipboard_content
                except Exception as e:
                    print(f"⚠️ 无法读取剪贴板内容: {e}")
                    # 如果无法读取剪贴板，尝试直接提取页面内容
                    try:
                        # 尝试提取页面上的回答内容
                        content = self.page.evaluate("""
                            () => {
                                // 查找所有消息元素
                                const messageElements = Array.from(document.querySelectorAll('div[class*="message"]'));
                                if (messageElements.length >= 2) {
                                    // 通常第二个消息元素是AI的回答
                                    const lastMessage = messageElements[messageElements.length - 1];
                                    // 移除一些不必要的元素（如按钮等）
                                    const clone = lastMessage.cloneNode(true);
                                    const buttons = clone.querySelectorAll('button, svg, [aria-label]');
                                    buttons.forEach(btn => btn.remove());
                                    return clone.textContent || '';
                                }
                                return '';
                            }
                        """)
                        if content and content.strip():
                            print(f"📄 从页面提取到的内容: {content}")
                            return content
                        else:
                            return None
                    except Exception as e2:
                        print(f"❌ 从页面提取内容时出错: {e2}")
                        return None
            else:
                print("❌ 未找到复制按钮，尝试直接提取内容")
                # 尝试使用JavaScript直接获取内容
                try:
                    content = self.page.evaluate("""
                        () => {
                            // 查找所有消息元素
                            const messageElements = Array.from(document.querySelectorAll('div[class*="message"]'));
                            if (messageElements.length >= 2) {
                                // 通常第二个消息元素是AI的回答
                                const lastMessage = messageElements[messageElements.length - 1];
                                // 移除一些不必要的元素（如按钮等）
                                const clone = lastMessage.cloneNode(true);
                                const buttons = clone.querySelectorAll('button, svg, [aria-label]');
                                buttons.forEach(btn => btn.remove());
                                return clone.textContent || '';
                            }
                            return '';
                        }
                    """)
                    if content and content.strip():
                        print(f"📄 提取到的内容: {content}")
                        return content
                    else:
                        print("❌ 无法提取内容")
                        return None
                except Exception as e:
                    print(f"❌ 提取内容时出错: {e}")
                    return None

        except TimeoutError as e:
            print(f"❌ 超时：未找到相关元素 - {str(e)}")
            return None
        except Exception as e:
            print(f"❌ 等待过程中出现错误: {str(e)}")
            return None

    def save_content(self, content, filename="deepseek_response.txt"):
        """保存内容到文件"""
        if content:
            filepath = os.path.join(script_dir, filename)
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"💾 回答内容已保存到 {filename}")
            return filepath
        return None

    def close(self):
        """关闭浏览器"""
        if self.context:
            self.context.close()
        if self.browser:
            self.browser.close()

def run(playwright: Playwright) -> None:
    # 创建DeepSeek客户端实例
    client = DeepSeekClient(headless=False)

    try:
        # 启动浏览器
        client.start_browser()

        # 加载或创建上下文
        client.load_or_create_context()

        # 登录（如果需要）
        client.login_if_needed()

        # 导航到聊天页面
        client.navigate_to_chat()

        # 登录后暂停，方便调试
        # print("🔍 登录完成，进入调试模式...")
        # client.page.pause()  # 在这里暂停，您可以调试页面

        # 激活深度思考模式
        client.activate_deep_thinking()

        # 启用联网搜索
        client.enable_web_search()

        # 发送问题
        # question = "机器学习系统学习路径"
        question = "计算1+2="
        client.send_message(question)

        # client.page.pause()
        # 等待并提取回答内容
        # client.page.pause()
        extracted_content = client.wait_and_extract_content()

        # 保存内容
        client.save_content(extracted_content)

        if extracted_content:
            print("✅ 成功提取回答内容")
        else:
            print("❌ 未能提取回答内容")

        # 保持浏览器打开一段时间以便观察
        print("⏳ 保持浏览器打开10秒以便观察...")
        time.sleep(10)

    finally:
        # 关闭浏览器
        client.close()

if __name__ == "__main__":
    with sync_playwright() as playwright:
        run(playwright)
