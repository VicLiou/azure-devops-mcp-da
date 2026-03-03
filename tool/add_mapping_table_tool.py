from tool.func.add_mapping_table_func import (
    add_project_mapping_tool_func,
    add_member_mapping_tool_func
)

def register_add_mapping_table_tool(mcp, config):
    
    @mcp.tool()
    def add_project_mapping_tool(
        project_name: str,
        apid: str,
        apid_name: str
    ) -> str:
        """
        當執行 create_special_work_item_tool 建立 work item 時發現專案資訊不存在 PROJECT_MAPPING 時，使用此工具新增。

        例如：
        - project_name: "PROJECT-NO1"
        - apid: "APID-NO1"
        - apid_name: "系統名稱"
        
        Args:
            project_name: Azure DevOps 專案名稱 (必填)
            apid: 系統 APID 代碼 (必填)
            apid_name: APID 對應的系統名稱 (必填)
        """

        return add_project_mapping_tool_func(
            project_name=project_name,
            apid=apid,
            apid_name=apid_name,
            config=config
        )

    @mcp.tool()
    def add_member_mapping_tool(
        department: str
    ) -> str:
        """
        當查詢 mapping_table.json 發現使用者資訊不存在 MEMBER_MAPPING 時，使用此工具新增。

        Args:
            department: 部門名稱 (必填)
        """
        
        return add_member_mapping_tool_func(
            department=department,
            config=config
        )
