import uiautomator2 as u2

# 连接设备
try:
    d = u2.connect()
except Exception as e:
    print(f"连接设备失败: {e}")
    exit(1)

def extract_text_info(element, level, printed_elements):
    # 获取元素的信息
    element_info = element.info
    element_key = (element_info.get('className'), element_info.get('resourceId'), element_info.get('text'))

    # 检查元素是否已经打印过
    if element_key in printed_elements:
        return

    # 打印元素信息，使用缩进来表示层级关系
    indent = "  " * level
    print(f"{indent}{element_info.get('className')} {element_info.get('resourceId')} {element_info.get('text')}")

    # 标记元素为已打印
    printed_elements.add(element_key)

    # 递归遍历子元素
    sub_children = element.child()
    for sub_child in sub_children:
        extract_text_info(sub_child, level + 1, printed_elements)

# 查找RecyclerView元素
recycler_view = d(resourceId="com.hexin.plat.android:id/recyclerview_id")
if recycler_view.exists:
    print("元素存在")
    # 遍历RecyclerView的子元素
    children = recycler_view.child()
    printed_elements = set()  # 用于跟踪已经打印过的元素
    for child in children:
        # 递归打印子元素及其层级结构
        extract_text_info(child, level=1, printed_elements=printed_elements)
else:
    print("元素不存在")
