import importlib.util
import json
from pathlib import Path
from config.logging_config import setup_logging, get_logger

setup_logging()
logger = get_logger(__name__)

# 取得外部檔案（支援 .py 和 .json）
def load_file(path: str):
    """
    載入外部檔案，支援 Python 模組和 JSON 檔案
    
    Args:
        path: 檔案路徑
        
    Returns:
        對於 .py 檔案：返回模組物件
        對於 .json 檔案：返回可用屬性存取的物件
    """
    external_file = Path(path)
    logger.info(f"Loading external file from: {external_file}")
    
    # 根據副檔名決定載入方式
    if external_file.suffix == '.json':
        # JSON 檔案處理
        try:
            with open(external_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            logger.info(f"Successfully loaded JSON file: {external_file}")
            return data
        
        except Exception as e:
            logger.error(f"Failed to load JSON file {external_file}: {e}")
            raise
    else:
        # Python 檔案處理（原有邏輯）
        spec = importlib.util.spec_from_file_location("file", external_file)
        file_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(file_module)
        logger.info(f"Successfully loaded Python module: {external_file}")
        return file_module
