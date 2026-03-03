from config.logging_config import setup_logging, get_logger
from init import get_connector, McpConfig
from utils.error_handler_util import handle_tool_errors

setup_logging()
logger = get_logger(__name__)

@handle_tool_errors("delete work item")
def delete_work_item_tool_func(config, work_item_id) -> str:
    connector = get_connector()

    # 取得要刪除的 Work Item 資訊
    delete_work_item = connector.connection.clients.get_work_item_tracking_client().get_work_item(
        id=work_item_id,
    )
    logger.info(f"Retrieved Work Item: {delete_work_item}")

    # 取得指派對象
    asign_user = delete_work_item.fields.get("System.AssignedTo")

    # 若取得的使用者為 None，則設為 Unknown User
    if asign_user == None:
        asign_user = {'displayName': "Unknown User"}

    logger.info(f"Work Item Assigned To: {asign_user['displayName']}, Current User: {McpConfig.USER}")

    # 檢查指派對象是否為當前使用者
    if asign_user['displayName'] != McpConfig.USER:
        logger.warning(f"Delete Work Item Assigned To: {asign_user['displayName']}, not current user: {McpConfig.USER}. Proceeding with deletion may violate access policies.")
        return f"Warning: The work item is assigned to {asign_user['displayName']}, not the current user {McpConfig.USER}. Deletion may violate access policies."
        
    # 確認指派人員為使用者本人，執行刪除動作
    # 未帶 destroy=false，會直接刪除 Task；若 destroy=true，則會放到回收站(可復原)
    result = connector.connection.clients.get_work_item_tracking_client().delete_work_item(
        id=work_item_id,
    )

    logger.info(f"Work item with ID {work_item_id} has been deleted successfully. Result: {result}")    
    return f"Work item with ID {work_item_id} has been deleted successfully. Result: {result}"