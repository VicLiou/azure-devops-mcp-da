import logging
import sys

def setup_logging():
    # 建立支援 UTF-8 的 StreamHandler，輸出到 stderr（MCP 使用 stdout 進行通訊）
    handler = logging.StreamHandler(sys.stderr)
    handler.setLevel(logging.INFO)
    
    # 設定 UTF-8 編碼
    handler.setStream(open(sys.stderr.fileno(), mode='w', encoding='utf-8', buffering=1, closefd=False))
    
    # 設定格式
    formatter = logging.Formatter('%(name)s - %(message)s')
    handler.setFormatter(formatter)
    
    # 配置 root logger
    logging.basicConfig(
        level=logging.INFO,
        handlers=[handler]
    )

def get_logger(name):
    return logging.getLogger(name)
