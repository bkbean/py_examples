import subprocess
import time
import requests


def get_bilibili_live_url(room_id, headers):
    # 获取直播间信息
    room_info_url = f'https://api.live.bilibili.com/room/v1/Room/get_info?room_id={room_id}'
    response = requests.get(room_info_url, headers=headers)
    if response.status_code != 200:
        print('无法获取直播间信息，请检查网络或房间号是否正确。')
        return None
    
    room_data = response.json()
    if room_data['code'] != 0:
        print(f"错误：{room_data['message']}")
        return None

    # 检查房间是否正在直播
    live_status = room_data['data']['live_status']
    if live_status != 1:
        print('该房间当前未开播。')
        return None

    # 获取直播流地址
    play_url_api = f'https://api.live.bilibili.com/room/v1/Room/playUrl?cid={room_id}&quality=4&platform=web'
    play_response = requests.get(play_url_api, headers=headers)
    if play_response.status_code != 200:
        print('无法获取直播流地址，请稍后重试。')
        return None
    
    play_data = play_response.json()
    if play_data['code'] != 0:
        print(f"错误：{play_data['message']}")
        return None

    # 提取直播地址
    live_url = play_data['data']['durl'][0]['url']
    return live_url

def play_live_stream(url, headers):
    # 将 headers 字典转换为 ffplay 可用的字符串格式
    headers_str = '\r\n'.join(f'{key}: {value}' for key, value in headers.items())
    p = None
    try:
        # 启动一个新的进程来播放指定的媒体URL, 播放结束后自动退出, 发生错误时输出日志信息, 并传递自定义请求头。
        p = subprocess.Popen(['ffplay', '-autoexit', '-loglevel', 'error', '-headers', headers_str, url])
        print('正在播放直播流，请稍候...')
    except Exception as e:
        print(f'播放失败：{e}')
    return p

if __name__ == '__main__':
    # 设置请求头，模拟浏览器访问
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
        'Referer': 'https://www.bilibili.com/',
        'Origin': 'https://www.bilibili.com'
    }

    room_id = 1865939779        # 替换成你的直播间号
    refresh_interval = 1200     # 每20分钟刷新一次（单位：秒）
    player = None

    try:
        while True:
            print(f'正在获取房间 {room_id} 最新直播流地址...')
            url = get_bilibili_live_url(room_id, headers)
            if url:
                print(f'获取成功: {url}')
                if player:
                    player.terminate()
                player = play_live_stream(url, headers)
            else:
                print('获取失败')
            time.sleep(refresh_interval)
    except KeyboardInterrupt:
        print('退出程序')
        if player:
            player.terminate()
