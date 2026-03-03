
def register_prompt_templates(mcp):
    
    @mcp.prompt()
    def azure_devops_context():
        """
        提供 Azure DevOps 連線和專案上下文資訊
        """

        return f"""
        Azure DevOps 環境資訊:
        - Organization URL: 
        - 連線狀態: 已配置
        - 可用功能: 專案查詢、工作項目查詢、工作項目建立
        
        使用提示:
        1. 查詢工作項目時會返回指派給特定人員的任務
        2. 在使用 @mcp.tool 時，需查看 Args 列表以確認所需參數
        3. 當使用者提到「前N筆」、「最新N筆」、「top N」時，請將 N 作為 limit 參數傳遞給 get_task_info_tool
        例如：「前10筆」→ limit=10，「最新5筆」→ limit=5
        4. 工作項目類型為 Task，parent_id 為必填參數
        5. 工作項目類型為 User Story，parent_id 為選填參數
        """