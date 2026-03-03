from tool.func.delete_item_func import (
    delete_work_item_tool_func
)

def register_delete_item_tools(mcp, config):

    @mcp.tool()
    def delete_work_item_tool(
        work_item_id: int
    ) -> str:
        """
        提供 Azure DevOps 專案 User Story、Bug、Task 刪除功能 (僅支援刪除自己的項目)。
        這個 MCP Tool 會自行確認刪除單的 AssignTo 人員，確認為自己再進行刪除動作。

        Args:
            work_item_id: 要刪除的工作項目 ID(必填)
        """
        return delete_work_item_tool_func(config, work_item_id)