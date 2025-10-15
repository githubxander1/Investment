"""
活动工作队列接口
封装applications.work_queue.ActiveWork中的功能
"""

from applications.work_queue.ActiveWork import ActiveWork


def create_active_work():
    """
    创建活动工作队列实例
    
    Returns:
        ActiveWork: 活动工作队列实例
    """
    return ActiveWork()


def get_next_work_item(active_work):
    """
    获取队列中下一个未执行的工作项
    
    Args:
        active_work (ActiveWork): 活动工作队列实例
        
    Returns:
        pandas.Series or None: 下一个工作项，如果没有则返回None
    """
    return active_work.get_Queue_the_one()


def update_work_item_status(active_work, key):
    """
    更新工作项状态
    
    Args:
        active_work (ActiveWork): 活动工作队列实例
        key (str): 工作项的唯一标识
        
    Returns:
        bool: 更新是否成功
    """
    try:
        active_work.edit_queue_the_one_status(key)
        return True
    except Exception as e:
        print(f"更新工作项状态失败: {e}")
        return False