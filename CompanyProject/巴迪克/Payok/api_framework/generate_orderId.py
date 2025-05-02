import datetime
import random

def generate_order_id(merchant_id):
    """
    生成订单号
    :param merchant_id: 商户 ID
    :return: 生成的订单号
    """
    # 获取当前时间
    now = datetime.datetime.now()
    # 格式化时间戳，精确到毫秒
    timestamp_str = now.strftime("%Y%m%d%H%M%S%f")[:-3]
    # 生成 3 位随机数
    random_num = "{:03d}".format(random.randint(0, 999))
    # 组合商户 ID、时间戳和随机数生成订单号
    order_id = f"{timestamp_str}{random_num}"
    return order_id

# 示例使用
merchant_id = "010095"
order_id = generate_order_id(merchant_id)
print("生成的订单号:", order_id)