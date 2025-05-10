# -*- coding: utf-8 -*-
import sys,time
from PySide6.QtCore import Signal,Slot,QMetaObject,QThread
from PySide6.QtGui import *
from PySide6.QtWidgets import *

from functools import partial


class SignalSlotDemo(QWidget):
    signal1 = Signal()
    signal2 = Signal(str)
    signal3 = Signal(str,int,list,dict)
    signal4 = Signal(str,int,list,dict)

    def __init__(self, *args, **kwargs):
        super(SignalSlotDemo, self).__init__(*args, **kwargs)
        self.setWindowTitle('信号与槽')
        self.resize(600, 400)
        layout = QGridLayout()
        self.setLayout(layout)

        self.checkBox = QCheckBox('显示点击状态')
        layout.addWidget(self.checkBox)
        self.label = QLabel('用来显示信息', self)
        layout.addWidget(self.label,1,0,1,2)

        # 信号-槽组合
        button1 = QPushButton("1 - 内置信号+内置槽", self)
        layout.addWidget(button1)
        button1.clicked.connect(self.checkBox.toggle)

        self.button2 = QPushButton("2 - 内置信号+自定义槽", self)
        layout.addWidget(self.button2)
        self.connect1 = self.button2.clicked.connect(self.button2Click)

        button3 = QPushButton("3 - 自定义信号+内置槽", self)
        self.signal1.connect(self.checkBox.toggle)
        layout.addWidget(button3)
        button3.clicked.connect(lambda: self.signal1.emit())

        button4 = QPushButton("4 - 自定义信号+自定义槽", self)
        self.signal2[str].connect(self.button4Click)
        layout.addWidget(button4)
        button4.clicked.connect(lambda: self.signal2.emit('我是参数'))

        button5 = QPushButton('5 - 断开连接 "2 - 内置信号+自定义槽"', self)
        layout.addWidget(button5)
        button5.clicked.connect(self.button5Click)


        button6 = QPushButton('6 - 恢复连接 "2 - 内置信号+自定义槽"', self)
        layout.addWidget(button6)
        button6.clicked.connect(self.button6Click)

        self.button7 = QPushButton("7 - 装饰器信号与槽", self)
        self.button7.setObjectName("button7Slot")
        layout.addWidget(self.button7)
        QMetaObject.connectSlotsByName(self)

        self.button8 = QPushButton("8 - 多线程信号与槽", self)
        layout.addWidget(self.button8)
        self.button8.clicked.connect(self.button8Click)
    
        # 信号参数组合
        self.button11 = QPushButton("11 - 内置信号+默认参数", self)
        self.button11.setCheckable(True)
        layout.addWidget(self.button11)
        self.button11.clicked[bool].connect(self.button11Click)

        button12 = QPushButton("12 - 自定义信号+默认参数", self)
        self.signal2[str].connect(self.button12Click)
        layout.addWidget(button12)
        button12.clicked.connect(lambda: self.signal2.emit('我是参数'))

        self.button13 = QPushButton("13 - 内置信号+自定义参数lambda", self)
        self.button13.setCheckable(True)
        layout.addWidget(self.button13)
        self.button13.clicked[bool].connect(lambda bool1:self.button13_14Click(bool1,button=self.button13,a=5,b='botton13'))

        self.button14 = QPushButton("14 - 内置信号+自定义参数partial", self)
        self.button14.setCheckable(True)
        layout.addWidget(self.button14)
        self.button14.clicked[bool].connect(partial(self.button13_14Click,*args,button=self.button14,a=7,b='button14'))

        self.button15 = QPushButton("15 - 自定义信号+自定义参数lambda", self)
        self.signal3[str,int,list,dict].connect(lambda a1,a2,a3,a4:self.button15_16Click(a1,a2,a3,a4,button=self.button15,a=7,b='button15'))
        layout.addWidget(self.button15)
        self.button15.clicked.connect(lambda: self.signal3.emit('参数1',2,[1,2,3,4],{'a':1,'b':2}))

        self.button16 = QPushButton("16 - 自定义信号+自定义参数partial", self)
        self.signal4[str,int,list,dict].connect(partial(self.button15_16Click,*args,button=self.button16,a=7,b='button16'))
        layout.addWidget(self.button16)
        self.button16.clicked.connect(lambda: self.signal4.emit('参数1',2,[1,2,3,4],{'a':1,'b':2}))

    @Slot()
    def button2Click(self):
        self.checkBox.toggle()
        sender = self.sender()
        self.label.setText(f'时间：{time.strftime('%H:%M:%S')}，触发了 "{sender.text()}"。')

    @Slot()
    def button4Click(self, _str):
        self.checkBox.toggle()
        self.label.setText(f'时间：{time.strftime('%H:%M:%S')}，触发了 "4 - 自定义信号+自定义槽"，并传递了一个参数：{_str}。')

    @Slot()
    def button5Click(self):
        if self.isSignalConnect_(self.button2,'clicked()'):
            self.button2.clicked.disconnect()
            #self.button2.disconnect(self.connect1)
            #self.button2.clicked.disconnect(self.button2Click)
            self.label.setText(f'时间：{time.strftime('%H:%M:%S')}，断开连接："2 - 内置信号+自定义槽"')
        else:
            self.label.setText(f'时间：{time.strftime('%H:%M:%S')}，"2- 内置信号+自定义槽"已经断开连接，不用重复断开。"')

    @Slot()
    def button6Click(self):
        if self.isSignalConnect_(self.button2,'clicked()'):
            self.button2.clicked.disconnect(self.button2Click)
        self.button2.clicked.connect(self.button2Click)
        self.label.setText(f'时间：{time.strftime('%H:%M:%S')}，重新连接了："2 - 内置信号+自定义槽"')

    @Slot()
    def on_button7Slot_clicked(self):
        self.checkBox.toggle()
        sender = self.sender()
        self.label.setText(f'时间：{time.strftime('%H:%M:%S')}，触发了 "{sender.text()}"。')

    @Slot()
    def button8Click(self):
        self.checkBox.toggle()
        if hasattr(self,'backend'):
            self.label.setText(f'时间：{time.strftime('%H:%M:%S')}，已经开启线程，不用重复开启。')
        else:
            # 创建线程
            self.backend = BackendThread()
            # 连接信号
            self.backend.update_date.connect(self.display_time)
            # 开始线程
            self.backend.start()

    @Slot()
    def button11Click(self,bool1):
        sender = self.sender()
        if bool1 == True:
            _str = f'时间：{time.strftime('%H:%M:%S')}，触发了 "{sender.text()}"。\n传递一个信号的默认参数：{bool1}，表示该按钮被按下。'
        else:
            _str = f'时间：{time.strftime('%H:%M:%S')}，触发了 "{sender.text()}"。\n传递一个信号的默认参数：{bool1}，表示该按钮没有被按下。'
        self.label.setText(_str)


    @Slot()
    def button12Click(self,_str):
        self.label.setText(f'时间：{time.strftime('%H:%M:%S')}，触发了 "12-自定义信号+默认参数"，传递一个信号的默认参数：{_str}。')

    @Slot()
    def button13_14Click(self,bool1,button,a,b):
        if bool1 == True:
            _str = (
                f'时间：{time.strftime('%H:%M:%S')}，触发了 "{button.text()}"。\n'
                f'传递一个信号的默认参数：{bool1}，表示该按钮被按下。\n'
                f'三个自定义参数\nbutton={button}\na={a}\nb="{b}"'
                )
        else:
            _str = (
                f'时间：{time.strftime('%H:%M:%S')}，触发了 "{button.text()}"。\n'
                f'传递一个信号的默认参数：{bool1}，表示该按钮没有被按下。\n'
                f'三个自定义参数\nbutton={button}\na={a}\nb="{b}"'
                )
        self.label.setText(_str)

    @Slot()
    def button15_16Click(self,*args,button,a,b):
        _str = (
            f'时间：{time.strftime('%H:%M:%S')}，触发了 "{button.text()}"。\n'
            f'传递信号的默认参数：{args}\n'
            f'三个自定义参数\nbutton={button}\na={a}\nb="{b}"'
            )
        self.label.setText(_str)

    @Slot()
    def display_time(self,tim):
        self.button8.setText(f'8 - 多线程，时间：{tim}')

    def isSignalConnect_(self, obj, signal_name):
        index = obj.metaObject().indexOfMethod(signal_name)
        if index > -1:
            method = obj.metaObject().method(index)
            if method:
                return obj.isSignalConnected(method)
        return False

class BackendThread(QThread):
    # 通过类成员对象定义信号对象
    update_date = Signal(str)
    # 处理要做的业务逻辑
    def run(self):
        while True:
            self.update_date.emit(time.strftime('%H:%M:%S'))
            time.sleep(1)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = SignalSlotDemo()
    demo.show()
    app.exec()