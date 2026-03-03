import os

from config.logging_config import setup_logging, get_logger
from sources.func.template_source_func import get_member_mapping_dict_func
from init import McpConfig

setup_logging()
logger = get_logger(__name__)

# 確認使用者資訊是否已存在 mapping_table.json 的 MEMBER_MAPPING 中
def check_user_in_member_mapping() -> bool:
    
    if get_member_mapping_dict_func():
        return True
    else:
        return False

# 取得環境變數資訊
def get_env_variable() -> dict:

    TFS_URL = os.getenv("TFS_URL")
    TFS_CERT = os.getenv("TFS_CERT")
    USER_TOKEN = os.getenv("USER_TOKEN")
    DECRYPTION_KEY = os.getenv("DECRYPTION_KEY")
    ENC_FILE_DICT = os.getenv("ENC_FILE_DICT")
    ENC_FILE_JSON = os.getenv("ENC_FILE_JSON")

    env_config = {
        "url": TFS_URL,
        "cert": TFS_CERT,
        "token": USER_TOKEN,
        "decryption_key": DECRYPTION_KEY,
        "enc_file_dict": ENC_FILE_DICT,
        "enc_file_json": ENC_FILE_JSON,
    }

    return env_config