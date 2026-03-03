import json

from config.decrypt_path_config import decrypt
from config.logging_config import setup_logging, get_logger
from init import McpConfig

setup_logging()
logger = get_logger(__name__)

# 新增專案資訊到 mapping_table.json
def add_project_to_mapping_file(project_name: str, apid: str, apid_name: str, config) -> bool:
    """
    將新專案資訊新增到 mapping_table.json
    
    Args:
        project_name: 專案名稱
        apid: APID
        apid_name: APID 名稱
    
    Returns:
        bool: 新增成功返回 True，新增失敗返回 False
    """

    mapping_file = decrypt(config["enc_file_json"], config["decryption_key"])
    
    try:
        # 讀取現有的 JSON 檔案
        with open(mapping_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        logger.info(f"Loaded existing mapping data from {mapping_file}")
        
        # 確保 PROJECT_MAPPING 欄位存在
        if 'PROJECT_MAPPING' not in data:
            data['PROJECT_MAPPING'] = {}
            logger.warning("PROJECT_MAPPING not found, created new one")
        
        # 檢查專案是否已存在
        if project_name in data['PROJECT_MAPPING']:
            logger.warning(f"Project '{project_name}' already exists in mapping file")
            return False
        
        # 新增專案資訊
        data['PROJECT_MAPPING'][project_name] = {
            "apid": apid,
            "apid_name": apid_name
        }
        
        # 寫回 JSON 檔案（格式化輸出，便於閱讀）
        with open(mapping_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        
        logger.info(f"Successfully added project '{project_name}' to mapping file")
        logger.info(f"Added data: apid={apid}, apid_name={apid_name}")
        return True
        
    except FileNotFoundError:
        logger.error(f"Mapping file not found: {mapping_file}")
        return False
    
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON format in mapping file: {e}")
        return False
    
    except Exception as e:
        logger.error(f"Failed to add project to mapping file: {e}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        return False
    
# 新增成員資訊到 mapping_table.json
def add_member_to_mapping_file(department: str, config) -> str:
    """
    將新成員資訊新增到 mapping_table.json
    
    Args:
        department: 部門名稱
    
    Returns:
        bool: 新增成功返回 True，新增失敗返回 False
    """

    mapping_file = decrypt(config["enc_file_json"], config["decryption_key"])

    try:
        with open(mapping_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        logger.info(f"Loaded existing mapping data from {mapping_file}")

        department_options = data["MANAGER_MAPPING"].keys()
        logger.info(f"Department options: {department_options}")

        if department not in department_options:
            return "Error: Invalid department. Please choose from the following options: " + ", ".join(department_options)
        
        else:
            if 'MEMBER_MAPPING' not in data:
                data['MEMBER_MAPPING'] = {}
                logger.warning("MEMBER_MAPPING not found, created new one")
            
            if McpConfig.USER in data['MEMBER_MAPPING']:
                logger.warning(f"{McpConfig.USER} already exists in MEMBER_MAPPING")
                return "Error: User already exists in MEMBER_MAPPING"
            
            data['MEMBER_MAPPING'][McpConfig.USER] = {
                "department": department
            }

            with open(mapping_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)

            logger.info(f"Successfully added member {McpConfig.USER} to MEMBER_MAPPING.")
            return "Successfully added member to mapping file"

    except FileNotFoundError:
        logger.error(f"Mapping file not found: {mapping_file}")
        return "Error: Mapping file not found"
    
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON format in mapping file: {e}")
        return "Error: Invalid JSON format in mapping file"
    
    except Exception as e:
        logger.error(f"Failed to add project to mapping file: {e}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        return "Error: Failed to add member to mapping file"
