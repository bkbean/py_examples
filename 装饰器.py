# Python 装饰器（Decorator）是一种用于增强函数或方法功能的语法结构，本质上是一个高阶函数（即：以函数作为参数或返回值的函数）。
# 装饰器常用于在不修改原函数代码的情况下添加功能，如日志记录、性能测试、权限验证等。


# 打印日志
def log_decorator(func):
    def wrapper(*args, **kwargs):
        # 在函数执行前添加操作
        print(f'[LOG] 正在调用函数：{func.__name__}')
        result = func(*args, **kwargs)
        # 在函数执行后添加操作
        return result
    return wrapper

@log_decorator
def say_hello(name):
    print(f'你好，{name}！')

say_hello("张三")


# 带参数的装饰器
def repeat(n):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for _ in range(n):
                func(*args, **kwargs)
        return wrapper
    return decorator

@repeat(3)
def greet(name):
    print(f"你好，{name}！")

greet("李四")


# 权限验证
def require_admin(func):
    def wrapper(user, *args, **kwargs):
        if user != 'admin':
            print("无权限操作")
            return
        return func(user, *args, **kwargs)
    return wrapper

@require_admin
def delete_user(user, target):
    print(f'{user} 删除了用户 {target}')

delete_user('guest', '张三')  # 无权限
delete_user('admin', '张三')  # 成功


# 函数执行时间统计
import time
def timing(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f'执行时间：{end - start:.4f}秒')
        return result
    return wrapper

@timing
def slow_func():
    time.sleep(1)

slow_func()