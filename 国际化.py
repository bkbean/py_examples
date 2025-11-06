import gettext
import locale

# 设置本地化环境
locale.setlocale(locale.LC_ALL, '')  # 使用系统默认的本地化环境
# 获取当前系统的本地化语言
# lang = locale.getlocale()[0]
lang = 'zh_CN'      # 强制指定

# 创建一个翻译对象
trans = gettext.translation('sc', localedir='data/locale', languages=[lang], fallback=False)
trans.install()

# 定义问候消息
greeting_msg = _("Hello, World!")
# 输出问候消息
print(greeting_msg)