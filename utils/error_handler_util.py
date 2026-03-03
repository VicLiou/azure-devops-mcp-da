import traceback
from functools import wraps
from config.logging_config import get_logger

logger = get_logger(__name__)

def handle_tool_errors(operation_name: str = "operation"):
    """
    統一的錯誤處理裝飾器
    
    Args:
        operation_name: 操作名稱，用於錯誤訊息
    
    使用範例:
        @handle_tool_errors("delete work item")
        def delete_work_item_tool_func(config, work_item_id):
            # 函式邏輯
            return result
    """
    def decorator(func):

        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            
            except Exception as e:
                # 取得完整的 traceback 資訊
                error_details = traceback.format_exc()
                
                # 記錄錯誤日誌
                logger.error(f"Failed to {operation_name}: {e}")
                logger.error(f"Traceback: {error_details}")
                
                # 返回統一格式的錯誤訊息
                return f"Error during {operation_name}: {str(e)}\n\nDetails: {error_details}"
        
        return wrapper
    
    return decorator


def handle_query_errors(operation_name: str = "query", default_return=None):
    """
    用於查詢類函式的錯誤處理裝飾器（返回空結果而不是錯誤字串）
    
    Args:
        operation_name: 操作名稱
        default_return: 錯誤時的默認返回值（list函式用[]，dict函式用{}）
    
    使用範例:
        @handle_query_errors("retrieve projects", default_return=[])
        def get_projects_tool_func(config):
            # 函式邏輯
            return projects
    """
    def decorator(func):

        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            
            except Exception as e:
                # 取得完整的 traceback 資訊
                error_details = traceback.format_exc()
                
                # 記錄錯誤日誌
                logger.error(f"Failed to {operation_name}: {e}")
                logger.error(f"Traceback: {error_details}")
                
                # 返回默認值
                return default_return if default_return is not None else []
        
        return wrapper
    
    return decorator
