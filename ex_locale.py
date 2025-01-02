import gettext
import locale

# 设置本地化环境
locale.setlocale(locale.LC_ALL, '')  # 使用系统默认的本地化环境
# 获取当前系统的本地化语言
loc = locale.getlocale()

# 创建一个翻译对象
trans = gettext.translation('gjh', localedir='locale', languages=[loc[0]], fallback=False)
trans.install()

# 定义问候消息
greeting_msg = _("Hello, World!")

# 输出问候消息
print(greeting_msg)