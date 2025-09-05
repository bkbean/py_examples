import ffmpeg
import logging
import multiprocessing
import sys
import time

# ===============================
# 配置区
# ===============================

# 输入流（例如某平台直播源）
INPUT_STREAM_URL = 'https://cn-hbsjz-cm-02-09.bilivideo.com/live-bvc/825988/live_222103174_4331333_bluray/index.m3u8'

# 输出流（可同时推送到多个平台）
OUTPUT_STREAM_URLS = [
    'rtmp://your.server.com/live/stream1',
    'rtmp://youtube.com/live/stream2',
    'rtmp://bilibili.com/live/stream3'
]

# 重试间隔（秒）
RETRY_INTERVAL = 5

# ===============================
# 日志配置
# ===============================

logger = logging.getLogger(__name__)  # 使用模块级logger，便于区分日志来源
logger.setLevel(logging.INFO)
formatter = logging.Formatter(
    "%(asctime)s [%(processName)s] %(levelname)s: %(message)s"
)

# 输出到文件
file_handler = logging.FileHandler('stream_relay.log')
file_handler.setFormatter(formatter)

# 输出到控制台
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)

# ===============================
# 核心逻辑
# ===============================

def build_ffmpeg_cmd(input_stream_url: str, output_stream_url: str):
    """
    构建单路推流任务的 ffmpeg 命令
    
    Parameters:
        input_stream_url:  输入流地址 (RTMP/HLS/SRT等)
        output_stream_url: 输出目标地址 (RTMP)

    Returns:
        ffmpeg-python 构建的命令对象
    """
    return (
        ffmpeg
        .input(input_stream_url)                  # 输入流
        .output(
            output_stream_url,
            format='flv',                         # RTMP 协议必须是 FLV 封装
            c='copy'                              # 拷贝原有编码，避免转码（低延迟、低CPU占用）
        )
    )

def run_relay(input_stream_url: str, output_stream_url: str, retry_interval: int = 5):
    """
    单路推流任务（独立进程），支持自动重连
    
    Parameters:
        input_stream_url:  输入流地址
        output_stream_url: 输出目标地址
        retry_interval:    失败后重试间隔（秒）
    """
    while True:
        try:
            logger.info(f'开始推流到: {output_stream_url}')
            cmd = build_ffmpeg_cmd(input_stream_url, output_stream_url)
            cmd.run(quiet=False)  # 阻塞运行，直到流断开或出错
        except Exception as e:
            logger.error(f'推流异常: {output_stream_url}, 错误: {e}')

        logger.warning(f'流中断，{retry_interval} 秒后重试: {output_stream_url}')
        time.sleep(retry_interval)

def main():
    """
    为每个目标输出地址启动一个独立进程
    
    优点:
        每个推流任务相互独立，某一路失败不会影响其他任务
        使用 multiprocessing.Process，保证隔离性和健壮性
    """
    processes = []

    for output_stream_url in OUTPUT_STREAM_URLS:
        p = multiprocessing.Process(
            target=run_relay,
            args=(INPUT_STREAM_URL, output_stream_url, RETRY_INTERVAL),
            daemon=True  # 设置为守护进程，主进程退出时自动清理
        )
        processes.append(p)
        p.start()
        logger.info(f'推流进程已启动: {output_stream_url}')

    # 等待所有子进程运行（不会退出，除非手动终止）
    for p in processes:
        p.join()

# ===============================
# 程序入口
# ===============================
if __name__ == '__main__':
    main()
