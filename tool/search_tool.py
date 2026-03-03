from typing import Optional

from tool.func.search_func import (
    get_projects_tool_func,
    get_task_info_tool_func,
    get_project_team_func,
    get_team_iteration_func,
    get_project_templates_func,
    get_template_fields_func
)

def register_search_tools(mcp, config):
    """在 FastMCP 實例中註冊搜尋工具"""
    
    @mcp.tool()
    def get_projects_tool() -> list:
        """
        此工具用於取得 Azure DevOps 專案列表。
        """
        return get_projects_tool_func(config)

        
    @mcp.tool()
    def get_task_info_tool(
        query: Optional[str] = None,
        limit: int = 30
    ) -> list:
        """
        使用 WIQL(Work Item Query Language) 查詢 Azure Devops 工單資訊。

        這是一個類似於 SQL 的查詢語言。
        請根據使用者的需求自行建構 WIQL 語句。

        常用欄位如下：
        - [System.Id]: 工單 ID
        - [System.TeamProject]: 專案名稱
        - [System.Title]: 工單標題
        - [System.State]: 工單狀態 (例如：'New', 'Active', 'Code Review', 'Closed', 'Done')
        - [System.AssignedTo]: 指派對象 (使用 @Me 代表當前使用者，或使用完整顯示名稱如 '柳宏達')
        - [System.CreatedDate]: 建立日期
        - [System.ChangedDate]: 最後修改日期
        - [System.FinishedDate]: 完成日期
        - [System.AreaPath]: 區域路徑
        - [System.IterationPath]: 迭代路徑
        - [System.Tags]: 標籤

        查詢範例：
        1. 查詢特定人員的所有工單：
           SELECT * FROM WorkItems WHERE [System.AssignedTo] = '陳曉明'
        
        2. 查詢特定專案的工單：
           SELECT * FROM WorkItems WHERE [System.TeamProject] = 'PROJECT-NO1'
        
        3. 查詢多個專案的工單：
           SELECT * FROM WorkItems WHERE [System.TeamProject] IN ('PROJECT-NO1', 'PROJECT-NO2')
        
        4. 查詢特定人員在所有專案的工單：
           SELECT * FROM WorkItems WHERE [System.AssignedTo] = '陳曉明' ORDER BY [System.TeamProject]
        
        5. 查詢非已關閉的工單：
           SELECT * FROM WorkItems WHERE [System.AssignedTo] = @Me AND [System.State] <> 'Closed'

        Args:
            limit: 限制返回的工單數量，預設為 30 (選填)
        """
        return get_task_info_tool_func(config, query, limit)

    @mcp.tool()
    def get_project_team(
        project: str
    ) -> list:
        """
        取得 Azure DevOps 專案中的所有團隊資訊。

        Args:
            project: 專案 ID 或名稱 (必填)
        """
        return get_project_team_func(config, project)
        
    @mcp.tool()
    def get_team_iteration(
        project_name: str,
        team_name: str
    ) -> list:
        """
        取得指定團隊當前時間的迭代路徑資訊。

        Args:
            project_name: 專案名稱 (必填)
            team_name: 團隊名稱 (必填)
        """
        return get_team_iteration_func(config, project_name, team_name)
    
    @mcp.tool()
    def get_project_templates(
        project_name: str,
        team_name: Optional[str] = None,
        workitemtypename: str = "Task"
    ) -> list:
        """
        當用戶有明確說明需要查詢模板範本時，使用此工具。
        取得指定專案及團隊的工作項目範本列表。

        Args:
            project_name: 專案名稱 (必填)
            team_name: 團隊名稱 (選填)
            workitemtypename: 工作項目類型，預設為 Task (選填)
        
        Returns:
            list: 範本列表
        """
        return get_project_templates_func(config, project_name, team_name, workitemtypename
    )

    @mcp.tool()
    def get_template_fields(
        project_name: str,
        template_id: str,
        team_name: Optional[str] = None
    ) -> dict:
        """
        取得指定範本的欄位資訊。

        Args:
            project_name: 專案名稱 (必填)
            template_id: 範本 ID (必填)
            team_name: 團隊名稱 (選填)
        
        Returns:
            dict: 範本欄位資訊
        """
        return get_template_fields_func(config, project_name, template_id, team_name)