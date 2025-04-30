import cv2


def compare_images(image_path1, image_path2):
    # 读取两幅图像
    image1 = cv2.imread(image_path1)
    image2 = cv2.imread(image_path2)

    # 计算图像的哈希值
    hash1 = cv2.hashImage(image1, cv2.HASH_MD5)
    hash2 = cv2.hashImage(image2, cv2.HASH_MD5)

    # 比较哈希值
    if hash1 == hash2:
        return "两幅图像相同"
    else:
        return "两幅图像不同"


image_path1 = "设计稿.png"
image_path2 = "测试图.png"

result = compare_images(image_path1, image_path2)
print(result)