from azure.devops.connection import Connection
from msrest.authentication import BasicAuthentication
import os

from config.logging_config import setup_logging, get_logger

setup_logging()
logger = get_logger(__name__)

class DevOpsConnector:
    def __init__(self, organization_url, personal_access_token, cert_path):
        self.organization_url = organization_url
        self.personal_access_token = personal_access_token
        self.cert_path = cert_path
        self.connection = None

    def connect(self):
        try:
            # 如果有指定證書路徑，設定環境變數
            if self.cert_path:
                os.environ['REQUESTS_CA_BUNDLE'] = self.cert_path
            else:
                logger.error("Certificate path is not provided. Please set the TFS_CERT environment variable to the path of your certificate file.")
                return False
            
            credentials = BasicAuthentication('', self.personal_access_token)
            self.connection = Connection(
                base_url=self.organization_url,
                creds=credentials
            )
            logger.info("Connection established successfully.")
            return True
        
        except Exception as e:
            logger.error(f"Failed to connect: {e}")
            return False

# 全局 connector 實例
_global_connector = None

def initialize_global_connector(config: dict) -> bool:
    """初始化全局 connector（僅在 server.py 啟動時調用一次）"""
    global _global_connector
    try:
        _global_connector = DevOpsConnector(
            config["url"], 
            config["token"], 
            config["cert"]
        )
        if _global_connector.connect():
            logger.info("Global DevOps connector initialized successfully.")
            return True
        else:
            logger.error("Failed to initialize global connector.")
            return False
    except Exception as e:
        logger.error(f"Error initializing global connector: {e}")
        return False

def get_connector() -> DevOpsConnector:
    """取得全局 connector 實例"""
    if _global_connector is None:
        raise RuntimeError(
            "DevOps connector has not been initialized. "
            "Please call initialize_global_connector() first."
        )
    return _global_connector

# 取得 USER 名稱
class ReadOnlyMeta(type):
    """元類：防止修改指定的類別屬性"""
    
    _readonly_attrs = {'USER', 'EMPLOYEE_ID'}
    
    def __setattr__(cls, name, value):
        if name in cls._readonly_attrs and hasattr(cls, '_initialized') and cls._initialized:
            raise AttributeError(
                f"Cannot modify read-only attribute '{name}'. "
                f"Use McpConfig.initialize() to set user information."
            )
        super().__setattr__(name, value)


class McpConfig(metaclass=ReadOnlyMeta):
    """
    單例配置類別，儲存當前連線使用者資訊
    
    類別屬性：
        USER (str): 使用者顯示名稱（唯讀，初始化後不可修改）
        EMPLOYEE_ID (str): 使用者員工編號（唯讀，初始化後不可修改）
    
    使用方式：
        # 初始化（僅在系統啟動時調用一次）
        McpConfig.initialize()
        
        # 讀取使用者資訊
        user_name = McpConfig.USER
        emp_id = McpConfig.EMPLOYEE_ID
        
        # 或使用方法
        user_info = McpConfig.get_user_info()
    """
    USER: str = "Unknown User"
    EMPLOYEE_ID: str = "N/A"
    _initialized: bool = False
    
    def __init__(self):
        """防止直接實例化（保留用於向後兼容，但會發出警告）"""
        logger.warning(
            "McpConfig should not be instantiated. "
            "Use McpConfig.initialize() instead. "
            "This instantiation is ignored."
        )
    
    @classmethod
    def initialize(cls) -> None:
        """
        初始化使用者資訊（僅應在系統啟動時調用一次）
        初始化後，USER 和 EMPLOYEE_ID 將變為唯讀屬性
        """
        if cls._initialized:
            logger.warning("McpConfig has already been initialized. Skipping re-initialization.")
            return
            
        try:
            connector = get_connector()

            # 嘗試使用 Location API 取得連線資料
            try:
                location_client = connector.connection.clients.get_location_client()
                connection_data = location_client.get_connection_data()
                
                if connection_data and hasattr(connection_data, 'authenticated_user'):
                    user = connection_data.authenticated_user
                    display_name = user.provider_display_name if hasattr(user, 'provider_display_name') else 'Unknown User'
                    
                    # 嘗試從 properties 取得 employee ID
                    employee_id = user.properties.get('Account', {}).get('$value', 'N/A') if (hasattr(user, 'properties') and user.properties) else 'N/A'

                    logger.info(f"Connected as: {display_name} ({employee_id})")
                    
                    # 更新類別變數（初始化階段允許修改）
                    type.__setattr__(cls, 'USER', display_name)
                    type.__setattr__(cls, 'EMPLOYEE_ID', employee_id)
                    type.__setattr__(cls, '_initialized', True)
                    
            except Exception as e:
                logger.warning(
                    f"Failed to retrieve authenticated user information from Azure DevOps "
                    f"Location API for organization '{connector.organization_url}': {e}"
                )
                type.__setattr__(cls, '_initialized', True)

        except (KeyError, TypeError) as e:
            logger.error(f"Error retrieving user profile due to invalid configuration: {e}")
            type.__setattr__(cls, '_initialized', True)

        except Exception as e:
            logger.error(f"Error retrieving user profile: {e}")
            logger.warning("Service will continue...")
            type.__setattr__(cls, '_initialized', True)
    
    @classmethod
    def get_user_info(cls) -> dict:
        """
        取得使用者資訊字典
        
        Returns:
            dict: 包含 user 和 employee_id 的字典
        """
        return {
            "user": cls.USER,
            "employee_id": cls.EMPLOYEE_ID
        }