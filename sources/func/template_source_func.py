from config.decrypt_path_config import decrypt
from utils.file_loader_util import load_file
from init import McpConfig

# 取得外部檔案 - task_template.py
def get_template_info_dict_func(config):

    task_template = load_file(decrypt(config["enc_file_dict"], config["decryption_key"]))
    return task_template.TASK_TEMPLATE

# 取得外部檔案 - mapping_table.py - 主管對應表
def get_manager_mapping_dict_func(config):

    # 先取得成員對應表的使用者科別，再從主管對應表取得該科別的主管資訊
    mapping_table = load_file(decrypt(config["enc_file_json"], config["decryption_key"]))
    member_department = mapping_table["MEMBER_MAPPING"][McpConfig.USER]["department"]
    
    return mapping_table["MANAGER_MAPPING"][member_department]

# 取得外部檔案 - mapping_table.py - 成員對應表
def get_member_mapping_dict_func(config):
    
    # 直接根據使用者名稱取得對應的成員資訊
    return load_file(decrypt(config["enc_file_json"], config["decryption_key"]))["MEMBER_MAPPING"][McpConfig.USER]

# 取得外部檔案 - mapping_table.py - 專案對應表
def get_project_mapping_dict_func(config):
    return load_file(decrypt(config["enc_file_json"], config["decryption_key"]))["PROJECT_MAPPING"]