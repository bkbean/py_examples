from PySide6.QtWidgets import QApplication,QMainWindow,QWidget,QLabel


if __name__ == "__main__":
    # 创建了一个 QApplication 实例，用于管理整个应用程序的事件循环和资源分配。
    app = QApplication()
    # 创建一个空白的 QWidget 或 QMainWindow 对象，它代表着我们的窗体。
    #window = QWidget()
    window = QMainWindow()
    # 设置窗体的标题为 "Simple Window"。
    window.setWindowTitle("Simple Window")
    # 将窗体的大小固定为宽度为 400 像素、高度为 300 像素。
    window.setFixedSize(400, 300)
    # 创建一个 QLabel 对象，并将其作为子组件添加到窗体上。同时，设置标签的显示文本为 "Hello PySide6!"。
    label = QLabel("Hello PySide6!", window)
    # 显示窗体
    window.show()
    # 启动应用程序的事件循环，等待事件的触发和处理，使窗体保持可响应状态。
    app.exec()