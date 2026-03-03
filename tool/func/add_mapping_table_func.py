from config.logging_config import setup_logging, get_logger
from utils.mapping_table_util import (
    add_project_to_mapping_file,
    add_member_to_mapping_file
)
from utils.error_handler_util import handle_tool_errors

setup_logging()
logger = get_logger(__name__)

@handle_tool_errors("add project mapping")
def add_project_mapping_tool_func(project_name: str, apid: str, apid_name: str, config) -> str:
    """
    新增專案資訊到 mapping_table.py
    
    Args:
        project_name: 專案名稱
        apid: APID
        apid_name: APID 名稱
    """
    logger.info(f"Adding project mapping - Project: {project_name}, APID: {apid}, APID Name: {apid_name}")
    
    # 驗證輸入
    if not project_name or not apid or not apid_name:
        error_msg = "Project name, APID, and APID name are all required fields"
        logger.error(error_msg)
        return f"Error: {error_msg}"
    
    # 呼叫寫入函式
    success = add_project_to_mapping_file(project_name, apid, apid_name, config)
    
    if success:
        return f"Successfully added project information to mapping_table.py you can now continue to use the tools for creating work projects."
    else:
        return "Failed to add project information."

@handle_tool_errors("add member mapping")
def add_member_mapping_tool_func(department: str, config) -> str:
    """
    新增成員資訊到 mapping_table.py
    
    Args:
        department: 部門名稱
    """
    logger.info(f"Adding member mapping - Department: {department}")
    
    # 驗證輸入
    if not department:
        error_msg = "Department is a required field"
        logger.error(error_msg)
        return f"Error: {error_msg}"
    
    # 呼叫寫入函式
    return add_member_to_mapping_file(department=department, config=config)