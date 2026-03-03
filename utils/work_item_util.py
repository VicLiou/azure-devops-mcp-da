from jsonpath_rw import parse

from config.logging_config import setup_logging, get_logger

setup_logging()
logger = get_logger(__name__)

# 查找範本描述所在的完整路徑
def find_dict_path(template_desc: str, template: dict) -> str:
 
    # 使用遞迴深度搜尋找到所有 template_use_description 陣列
    jsonpath_expr = parse('$..template_use_description[*]')
    matches = jsonpath_expr.find(template)

    logger.info(f"Searching for template description: {template_desc}")
    
    # 找到匹配的項目並返回完整路徑
    for match in matches:
        for v in match.value:
            if v == template_desc:
                full_path = match.full_path
                logger.info(f"Found matching template description: {template_desc}")
                logger.info(f"Full path: {full_path}")

                return str(full_path)
    
    logger.info (f"Did not find '{template_desc}'")
    
    return None

# 取得可用於開啟工單的 HTML URL
def get_html_url(work_item) -> str:
    browser_url = work_item.url  # 默認使用 API URL
            
    try:
        logger.info(hasattr(work_item, '_links') and work_item._links)
        if hasattr(work_item, '_links') and work_item._links:
            links_dict = work_item._links.additional_properties
            logger.info(f"_links content: {links_dict}")

            if 'html' in links_dict and 'href' in links_dict['html']:
                browser_url = links_dict['html']['href']
                logger.info(f"Extracted HTML URL: {browser_url}")
        
    except Exception as e:
        logger.warning(f"Could not extract HTML URL from _links: {e}")
    
    return browser_url
