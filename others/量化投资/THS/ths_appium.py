from appium import webdriver
import time

# 定义设备的Desired Capabilities
desired_caps = {
    "platformName": "Android",
    # 模拟器的平台版本，可在模拟器设置中查看
    "platformVersion": "9",
    # 模拟器的设备名称，可通过adb devices命令查看
    "deviceName": "127.0.0.1:21503",
    "appPackage": "com.hexin.plat.android",
    # "appActivity": ".Settings"
}

# 启动Appium会话，连接到模拟器
driver = webdriver.Remote("http://127.0.0.1:4723/wd/hub", desired_caps)

# 等待5秒，以便观察操作
time.sleep(5)

# 关闭Appium会话
driver.quit()