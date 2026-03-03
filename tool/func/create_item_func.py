from azure.devops.v7_0.work_item_tracking.models import JsonPatchOperation

from config.logging_config import setup_logging, get_logger
from init import get_connector, McpConfig
from utils.init_util import check_user_in_member_mapping
from utils.work_item_util import find_dict_path, get_html_url
from utils.error_handler_util import handle_tool_errors

# 引用工具函式
from tool.func.search_func import (
    get_team_iteration_func
)
# 取得 MCP Resource
from sources.func.template_source_func import (
    get_template_info_dict_func, 
    get_manager_mapping_dict_func,
    get_member_mapping_dict_func,
    get_project_mapping_dict_func
)

setup_logging()
logger = get_logger(__name__)

# 工具函式 - 建立工作項目
# def create_work_item_tool_func(config, title, project_name, team_name, parent_id, tag, description, item_type) -> str:
#     try:
#         connector = DevOpsConnector(config["url"], config["token"], config["cert"])

#         if connector.connect():

#             # 取得目前迭代完整路徑
#             iteration = get_team_iteration_func(config, project_name, team_name)
#             logger.info(f"iteration info: {iteration}")
#             logger.info(f"Current iteration path: {iteration[0]['path'] if iteration else 'N/A'}")

#             # 組合 Area Path
#             if team_name:
#                 area = f"{project_name}\\{team_name}"
#             else:
#                 area = project_name
#             logger.info(f"Area path set to: {area}")

#             work_item = connector.connection.clients.get_work_item_tracking_client().create_work_item(
#                 document = set_item_info(config["url"], parent_id, title, iteration[0]["path"], area, description, tag),
#                 project = project_name,
#                 type=item_type
#             )
#             logger.info(f"Work item created successfully. URL: {work_item.url}")

#             return f"Work item created successfully. ID: {work_item.id}, Title: {work_item.fields.get('System.Title', '')}, URL: {work_item.url}"

#     except Exception as e:
#         logger.error(f"Failed to create work item: {e}")
#         import traceback
#         error_details = traceback.format_exc()
#         logger.error(f"Traceback: {error_details}")
#         return f"Error creating work item: {str(e)}\n\nDetails: {error_details}"
    
# 工具函式 - 建立特殊範本工作項目
@handle_tool_errors("create special work item")
def create_special_work_item_tool_func(config, project_name, template_index, template_desc, re_dict) -> str:
    connector = get_connector()

    # 確認使用者資訊
    if check_user_in_member_mapping():
        logger.info("User information found in MEMBER_MAPPING.")
    else:
        err_log = "User information not found in MEMBER_MAPPING. Please use 'add_member_mapping_tool' to add user information to mapping_table.json before using this tool."
        logger.error(f"Error: {err_log}")
        return err_log
    
    # 取得專案資訊
    project = project_name
    project_mapping = get_project_mapping_dict_func()
    project_info = project_mapping.get(project)

    if project_info:
        re_dict['apid'] = project_info['apid']
        re_dict['apid_name'] = project_info['apid_name']
        logger.info(f"Project info found: {project_info}")
    else:
        error_msg = "Project information not found in PROJECT_MAPPING. Please use 'add_project_mapping_tool' to add project information to mapping_table.json before using this tool."
        logger.error(f"Error: {error_msg}")
        return error_msg

    # 取得範本資訊
    templates = get_template_info_dict_func()

    # 取得工單類型
    template_full_path = find_dict_path(template_desc, templates)
    logger.info(f"Template full path: {template_full_path}")
    template_desc_parts = template_full_path.split('.')
    item_type = template_desc_parts[2] # 取得 Feature
    logger.info(f"Determined item type: {item_type}")

    # 取得目標專案和團隊
    target_project = template_desc_parts[0]  # 取得專案名稱
    target_team = template_desc_parts[1]  # 取得團隊名稱

    logger.info(f"Creating work item in project: {target_project}, team: {target_team}, using template index: {template_index}, template description: {template_desc}")
    logger.info(f"Template parameters: {re_dict}")

    # 取得目前迭代完整路徑
    iteration = get_team_iteration_func(config, target_project, target_team)
    logger.info(f"iteration info: {iteration}")
    logger.info(f"Current iteration path: {iteration[0]['path'] if iteration else 'N/A'}")

    # 組合 Area Path - 使用 target_team
    area = f"{target_project}\\{target_team}"
    logger.info(f"Area path set to: {area}")

    # 組合 user 欄位
    employee_id = McpConfig.EMPLOYEE_ID[3:]
    logger.info(f"Employee ID: {employee_id}")
    re_dict["user"] = f"NT{employee_id} {McpConfig.USER}"
    
    # 組合 Tamplate 路徑
    tamplate_path = templates.get(target_project).get(target_team).get(item_type)

    # 取得服務窗口
    item_approvals = tamplate_path.get("template_use_description")[template_index][1]

    # 格式化標題與描述
    title = tamplate_path.get("template_info")[template_index].get("title").format(**re_dict)
    description = tamplate_path.get("template_info")[template_index].get("description").format(**re_dict)

    # 取得對應 Tags（如果存在）
    tags = None
    tags_value = tamplate_path.get("template_info")[template_index].get("tags")
    
    if tags_value:
        if isinstance(tags_value, list):
            # 如果是 list，將每個元素格式化後用分號連接
            formatted_tags = [tag.format(**re_dict) if isinstance(tag, str) and '{' in tag else tag for tag in tags_value]
            tags = "; ".join(formatted_tags)
        elif isinstance(tags_value, str):
            # 如果是字串，直接格式化
            tags = tags_value.format(**re_dict)

    logger.info(f"Tags set to: {tags}")

    ###############################################
    ### 根據特殊需求，判斷 Tags 是否需取代特定內容 ###

    if "department" in tags:
        department_info = get_member_mapping_dict_func().get("department")
        tags = tags.replace("department", department_info)

        logger.info(f"Final Tags after special handling: {tags}")

    ### 根據特殊需求，判斷 Tags 是否需取代特定內容 ###
    ###############################################

    # 開立工單
    work_item = connector.connection.clients.get_work_item_tracking_client().create_work_item(
        document = set_item_info(
            title=title, 
            iteration=iteration[0]["path"], 
            area=area, 
            description=description,
            tags=tags,
            item_approvals=item_approvals,
        ),
        project = target_project,
        type=item_type
    )
        
    # 從 _links 提取 HTML URL
    browser_url = get_html_url(work_item)  # 默認使用 API URL
    
    return f"Work item created successfully. ID: {work_item.id}, Title: {work_item.fields.get('System.Title', '')}, URL: {browser_url}"
    
# 統一設定工單資訊
def set_item_info(
    organization_url: str = None, 
    parent_id: str = None, 
    title: str = None, 
    iteration: str = None, 
    area: str = None,
    description: str = None, 
    item_approvals: str = None,
    tags: str = None):

    document = []

    # 設定 assigned to
    document.append(JsonPatchOperation(
        op="add",
        path="/fields/System.AssignedTo",
        value=McpConfig.USER
    ))

    # 設定 area path
    if area is not None:
        document.append(JsonPatchOperation(
            op="add",
            path="/fields/System.AreaPath",
            value=area
        ))

    # 設定迭代路徑
    if iteration is not None:
        document.append(JsonPatchOperation(
            op="add",
            path="/fields/System.IterationPath",
            value=iteration if iteration else ""
        ))

    # 設定 parent link
    if parent_id is not None:
        document.append(JsonPatchOperation(
            op="add",
            path="/relations/-",
            value={
                "rel": "System.LinkTypes.Hierarchy-Reverse",
                "url": f"{organization_url}/_apis/wit/workItems/{parent_id}"
        }
    ))

    # 設定 title
    if iteration is not None:
        document.append(JsonPatchOperation(
            op="add",
            path="/fields/System.Title",
            value=title
        ))
    
    # 設定 description
    if iteration is not None:
        document.append(JsonPatchOperation(
            op="add",
            path="/fields/System.Description",
            value=description if description else ""
        ))

    # 設定 tag
    if iteration is not None:
        document.append(JsonPatchOperation(
            op="add",
            path="/fields/System.Tags",
            value=tags
        ))

    #####################################
    ### 根據特殊需求，是否需設定特定欄位 ###

    # 設定承辦科主管
    document.append(JsonPatchOperation(
        op="add",
        path="/fields/CUB.Field.ALMService.ReqApprovals",
        value=get_manager_mapping_dict_func()
    ))

    # 設定服務窗口
    document.append(JsonPatchOperation(
        op="add",
        path="/fields/CUB.Field.ALMService.Approvals",
        value=item_approvals
    ))

    ### 根據特殊需求，是否需設定特定欄位 ###
    #####################################

    return document