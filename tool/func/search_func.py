from azure.devops.v7_0.work_item_tracking.models import Wiql
from azure.devops.v7_0.work.models import TeamContext

from init import get_connector
from config.logging_config import setup_logging, get_logger
from utils.work_item_util import get_html_url
from utils.error_handler_util import handle_query_errors

setup_logging()
logger = get_logger(__name__)

# 工具函式 - 取得專案列表
@handle_query_errors("retrieve projects", default_return=[])
def get_projects_tool_func(config):
    connector = get_connector()
    projects = connector.connection.clients.get_core_client().get_projects()

    if projects:
        return [{"name": project.name, "id": str(project.id)} for project in projects]
    
    return []

# 工具函式 - 取得工單資訊
@handle_query_errors("execute WIQL query", default_return=[])
def get_task_info_tool_func(config, query: str, limit: int =30) -> list:
    # 如果沒有提供 query，使用預設查詢
    if not query:
        query = "SELECT * FROM WorkItems WHERE [System.AssignedTo] = @Me AND [System.State] <> 'Closed'"

    logger.info(f"Execute a WIQL query: {query}")

    connector = get_connector()
    wit_client = connector.connection.clients.get_work_item_tracking_client()

    wiql_object = Wiql(query=query)
    query_result = wit_client.query_by_wiql(wiql_object).work_items

    if not query_result:
        logger.info("No work items found for the query.")
        return []

    ids = [item.id for item in query_result]
    ids = ids[:limit]  # 限制返回數量

    # 取得 WIQL 語法所有查詢項目
    full_work_items = wit_client.get_work_items(ids, expand="links")
    logger.info(f"full_work_items Length: {len(full_work_items)}")
    logger.info(f"full_work_items: {full_work_items}")
    logger.info(f"Full item Fields: {[item.fields for item in full_work_items]}")

    # 整理資料僅回覆 Taks id、title、state、assign to、description、effort、task url 給 LLM
    clean_work_items =[{"id": item.id,
                        "title": item.fields.get("System.Title", ""),
                        "state": item.fields.get("System.State", ""),
                        "assigned_to": item.fields.get("System.AssignedTo", {}).get("displayName", ""),
                        "description": item.fields.get("System.Description", ""),
                        "effort": item.fields.get("Microsoft.VSTS.Scheduling.Effort", ""),
                        "url": get_html_url(item)} for item in full_work_items]
    logger.info(f"Cleaned work items: {clean_work_items}")

    return clean_work_items

# 工具函式 - 取得專案團隊列表
@handle_query_errors("retrieve teams", default_return=[])
def get_project_team_func(config, project: str) -> list:
    connector = get_connector()
    core_client = connector.connection.clients.get_core_client()
    teams = core_client.get_teams(project_id=project)

    if teams:
        return [{"project_name": team.project_name, 
                    "team_name": team.name} for team in teams]
    
    return []

# 工具函式 - 取得團隊迭代路徑
@handle_query_errors("retrieve team iterations", default_return=[])
def get_team_iteration_func(config, project: str, team: str) -> list:
    connector = get_connector()
    work_client = connector.connection.clients.get_work_client()

    project = TeamContext(project=project, team=team)
    iterations = work_client.get_team_iterations(project, "Current")

    for iteration in iterations:
        logger.info(f"Iteration: {iteration.name}, Path: {iteration.path}")

    if iterations:
        return [{"name": iteration.name, "path": iteration.path} for iteration in iterations]
    
    return []

# 工具函式 - 取得專案範本列表
@handle_query_errors("retrieve project templates", default_return=[])
def get_project_templates_func(config, project_name: str, team_name: str = None, workitemtypename: str = "Task") -> list:
    connector = get_connector()

    if not team_name:
        team_name = project_name

    team_context = TeamContext(project=project_name, team=team_name)
    templates = connector.connection.clients.get_work_item_tracking_client().get_templates(
        team_context = team_context,
        workitemtypename = workitemtypename
    )
    
    logger.info(f"Templates Length: {len(templates)}")
    for template in templates:
        logger.info(f"{template.name}, ID: {template.id}")

    if templates:
        return [{"name": template.name, "description": template.description} for template in templates]
    
    return []

# 工具函式 - 取得範本欄位資訊
@handle_query_errors("retrieve template fields", default_return={})
def get_template_fields_func(config, project_name: str, template_id: str, team_name: str = None) -> dict:
    connector = get_connector()

    if not team_name:
        team_name = project_name

    team_context = TeamContext(project=project_name, team=team_name)
    template = connector.connection.clients.get_work_item_tracking_client().get_template(
        team_context = team_context,
        template_id = template_id
    )

    # 取得必要資訊，並放入字典
    template_dict = {
        "title": template.fields.get("System.Title", ""),
        "activity": template.fields.get("Microsoft.VSTS.Common.Activity", ""),
        "effort": template.fields.get("Microsoft.VSTS.Scheduling.Effort", ""),
        "description": template.fields.get("System.Description", "")
    }
    
    logger.info(f"Template info: {template_dict}")
    
    return template_dict