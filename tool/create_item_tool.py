from typing import Optional

from tool.func.create_item_func import (
    # create_work_item_tool_func,
    create_special_work_item_tool_func
)

def register_create_item_tools(mcp, config):

    # @mcp.tool()
    # def create_work_item_tool(
    #     title: str,
    #     project_name: str,
    #     parent_id: Optional[int] = None,
    #     team_name: str = "",
    #     tag: Optional[str] = None,
    #     description: Optional[str]  = None,
    #     item_type: str = "Task"
    # ) -> str:
    #     """
    #     建立簡單的 User Story 或 Task 工作項目。
        
    #     ⚠️ 不適用情境：
    #     - 用戶提到「CD 管線」、「CI 管線」、「部署流程」等需要完整範本結構的需求
    #     - 這些情況請使用 create_work_item_feature_tool
        
    #     適用情境：
    #     - 建立一般性的待辦事項
    #     - 建立簡單的任務或用戶故事
    #     - 不需要範本和子任務結構的工作項目

    #     Args:
    #         title: 工作項目的標題(必填)
    #         project_name: 所屬專案名稱(必填)
    #         parent_id: 父工作項目 ID(選填）
    #         team_name: 所屬團隊名稱(選填)
    #         item_type: 工作項目的類型，限制為 User Stroy、Task 預設為 Task(選填)
    #         description: 工作項目的描述(選填)
    #         tag: 工作項目的標籤(選填)
    #     """
    #     return create_work_item_tool_func(config, title, project_name, team_name, parent_id, tag, description, item_type)
    
    @mcp.tool()
    def create_special_work_item_tool(
        project_name: str,
        template_index: int,
        template_desc: str,
        re_dict: dict
    ) -> str:
        """"        
        當使用者明確說明申請項目或開單需求時，使用此工具。
        此工具會基於預設範本自動建立完整的任務單。

        使用流程（自動化）：
        1. 先讀取 MCP Resource 'templates://dict' 取得所有範本
        2. 根據用戶需求匹配最適合的範本（檢查範本的 'template_use_description' 欄位，並從該串列中取得匹配範本的 index 及 value）
        3. 根據取得的 index ，找到 template_info 串列中鍵值為 parameter 欄位字典，根據字典向用戶收集必要參數值
        4. 建構 re_dict 參數字典，例如：{"project_name": "PROJECT-NO1", "variable_group": "VARIABLE-GROUP-NO1"}
        5. 呼叫此工具完成建立
        
        💡 參考資源（如需查詢人員或專案資訊）：
        - manager://mapping - 取得使用者的主管資訊
        - member://mapping - 取得使用者的成員資訊（包含科別資訊）
        - project://mapping - 取得對應的專案資訊
        
        ⚠️ 重要提醒：
        - 使用 member://mapping 資源無法取得成員資訊時，請呼叫 add_member_mapping_tool 新增成員資訊至 mapping_table.json 後再使用此工具
        - 範本 template_info 串列中鍵值為 parameter 欄位字典，根據字典向用戶收集必要參數值，並組成 re_dict 參數字典
        - re_dict 的 key 必須與範本中 {} 內的參數名稱相同，且所有必要參數都必須提供對應的 value，否則會導致格式化失敗

        Args:
            project_name: 來源專案名稱 (必填)
            target_project: 目標專案名稱 (必填，從 MCP Resource 'templates://dict' 取得)
            target_team: 目標團隊名稱 (必填，從 MCP Resource 'templates://dict' 取得)
            template_index: 範本索引值 (必填，從 MCP Resource 'templates://dict' 的 template_use_description 串列欄位取得)
            re_dict: 範本參數替換字典，key 是範本中 {} 內的參數名，value 是實際要填入的值(必填)
                    例如：{"project_name": "PROJECT-NO1", "variable_group": "VARIABLE-GROUP-NO1"}
        """
        
        return create_special_work_item_tool_func(
            config,
            project_name,
            template_index,
            template_desc,
            re_dict
        )