from mcp.server.fastmcp import FastMCP
import sys, asyncio

from init import McpConfig, initialize_global_connector
from config.logging_config import setup_logging, get_logger
from utils.init_util import get_env_variable

# Import and register tools
from tool.search_tool import register_search_tools
from tool.create_item_tool import register_create_item_tools
from tool.delete_item_tool import register_delete_item_tools
from tool.add_mapping_table_tool import register_add_mapping_table_tool

# Import and register sources
from sources.template_source import register_sources

# Import and register prompt
from prompt.prompt_template import register_prompt_templates

setup_logging()
logger = get_logger(__name__)

mcp = FastMCP("Azure Devops MCP Server")

# 取得環境變數設置
config = get_env_variable()

# 註冊 Prompt - 提供上下文資訊給 AI
register_prompt_templates(mcp)

# 註冊 Resource - 提供範本資訊
register_sources(mcp, config)

# 註冊工具 - 傳入配置
register_search_tools(mcp, config)
register_create_item_tools(mcp, config)
register_delete_item_tools(mcp, config)
register_add_mapping_table_tool(mcp, config)

def main():

    try:
        # 初始化全局 connector        
        if not initialize_global_connector(config):
            raise ConnectionError("Connect to Azure DevOps failed. Please check your settings.")
        
        logger.info("Azure DevOps MCP Server initialization successful, service started...")

        # 取得使用者資訊
        logger.info("Check user identity...")
        McpConfig.initialize()

        # 啟動 MCP 伺服器
        asyncio.run(mcp.run_stdio_async())
        
    except Exception as e:
        logger.error(f"Azure DevOps MCP Server initialization failed.")
        logger.error(f"Failed with error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()