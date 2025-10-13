import logging
import sys


def setup_logging(log_level=logging.INFO):
    """集中配置日志系统"""
    root_logger = logging.getLogger()
    # 日志系统总阀门, 按照设定级别将日志记录传递给各个handler
    root_logger.setLevel(log_level)
    
    formatter = logging.Formatter(
        '%(asctime)s [%(levelname)s] %(name)s: %(message)s (%(filename)s:%(lineno)d)'
    )
    
    # 控制台Handler
    console_handler = logging.StreamHandler(sys.stdout)
    # 日志系统支路阀门, 只输出高于设定级别的日志记录
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)

    # 避免重复添加 handler
    if not root_logger.handlers:
        root_logger.addHandler(console_handler)


# 初始化日志配置
setup_logging()

# 获取模块日志记录器
logger = logging.getLogger(__name__)

# 测试日志输出
logger.debug('Debug message (should not appear with INFO level)')
logger.info('Informational message')
logger.warning('Warning message')
logger.error('Error message')
logger.critical('Critical message')