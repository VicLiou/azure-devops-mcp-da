from sources.func.template_source_func import (
    get_template_info_dict_func,
    get_manager_mapping_dict_func,
    get_member_mapping_dict_func,
    get_project_mapping_dict_func
)

def register_sources(mcp, config):

    @mcp.resource("templates://dict")
    def get_template_info_dict() -> dict:
        """
        從外部取得取得自定義模板資訊
        """
        return get_template_info_dict_func(config)
    
    @mcp.resource("manager://mapping")
    def get_manager_mapping_dict() -> str:
        """
        從外部取得科主管對應表資訊
        """
        return get_manager_mapping_dict_func(config)
    
    @mcp.resource("member://mapping")
    def get_member_mapping_dict() -> dict:
        """
        從外部取得部門成員對應表資訊
        """
        return get_member_mapping_dict_func(config)
    
    @mcp.resource("project://mapping")
    def get_project_mapping_dict() -> dict:
        """
        從外部取得TFS專案對應表資訊
        """
        return get_project_mapping_dict_func(config)