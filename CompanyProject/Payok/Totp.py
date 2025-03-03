import pyotp
import time

# 这里的 secret 是你在绑定身份验证器时得到的密钥
# 通常是一个由字母和数字组成的字符串
secret = "YOUR_SECRET_KEY"

# 创建 TOTP 对象
totp = pyotp.TOTP(secret)

# 生成当前时间的 TOTP 验证码
current_code = totp.now()
print(f"当前的 TOTP 验证码是: {current_code}")

# 验证验证码是否正确
# 假设用户输入的验证码是 current_code
is_valid = totp.verify(current_code)
if is_valid:
    print("验证码验证通过")
else:
    print("验证码验证失败")

# 为了展示验证码的有效期，我们可以循环一段时间，观察验证码的变化
print("接下来的 3 个时间间隔内的验证码：")
for _ in range(3):
    code = totp.now()
    print(f"当前时间: {time.strftime('%Y-%m-%d %H:%M:%S')}, 验证码: {code}")
    # 等待 30 秒，因为 TOTP 验证码通常每 30 秒更新一次
    time.sleep(30)