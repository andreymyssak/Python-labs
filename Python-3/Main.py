import sys
from PyQt5 import QtCore, QtWidgets, uic, QtGui
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QRadioButton, QCheckBox, QTableWidgetItem, \
    QAbstractItemView

answers = ['', '', '']  # 1 - childhood, 2 - boyhood, 3 - youthfulness


class Welcome(QtWidgets.QMainWindow):
    # аргумент str говорит о том, что сигнал должен быть сторокового типа
    switch_window = QtCore.pyqtSignal(str)

    def __init__(self):
        super(Welcome, self).__init__()
        uic.loadUi('uis/welcome.ui', self)

        self.setWindowTitle('Приветствие')
        self.setWindowIcon(QtGui.QIcon('images/logo.png'))

        self.btn_exit.clicked.connect(self.close)
        self.btn_begin.clicked.connect(self.next)

    def next(self):
        self.switch_window.emit('next')


class Childhood(QtWidgets.QMainWindow):
    switch_window = QtCore.pyqtSignal(str)

    def __init__(self):
        super(Childhood, self).__init__()
        uic.loadUi('uis/childhood.ui', self)

        self.setWindowTitle('Детство')

        self.setWindowIcon(QtGui.QIcon('images/logo.png'))
        # устанавливаем картинку label_img
        self.label_img.setPixmap(QPixmap('images/cereal.png'))
        # подгоняем картинку под размер label_img
        self.label_img.setScaledContents(True)

        # если ранее ответ был уже выбран, то показываем его заново
        if answers[0] is not None:
            self.label_selected.setText('Выбрано: ' + answers[0])

        # ставим события на radioButtons
        self.radioButton_1.toggled.connect(
            lambda: self.onToggled(self.radioButton_1))
        self.radioButton_2.toggled.connect(
            lambda: self.onToggled(self.radioButton_2))
        self.radioButton_3.toggled.connect(
            lambda: self.onToggled(self.radioButton_3))
        self.radioButton_4.toggled.connect(
            lambda: self.onToggled(self.radioButton_4))

        self.btn_back.clicked.connect(self.back)
        self.btn_next.clicked.connect(self.next)

    def onToggled(self, radiobutton):
        if radiobutton.isChecked():
            answers[0] = radiobutton.text()
            self.label_selected.setText('Выбрано: ' + answers[0])

    def back(self):
        self.switch_window.emit('back')

    def next(self):
        self.switch_window.emit('next')


class Boyhood(QtWidgets.QMainWindow):
    switch_window = QtCore.pyqtSignal(str)

    def __init__(self):
        super(Boyhood, self).__init__()
        uic.loadUi('uis/boyhood.ui', self)

        self.setWindowTitle('Отрочество')

        self.setWindowIcon(QtGui.QIcon('images/logo.png'))
        self.label_img.setPixmap(QPixmap('images/books.png'))
        self.label_img.setScaledContents(True)

        if answers[1] is not None:
            self.label_selected.setText('Выбрано: ' + answers[1])

        self.listWidget.itemClicked.connect(self.item_click)
        self.btn_back.clicked.connect(self.back)
        self.btn_next.clicked.connect(self.next)

    def item_click(self, item):
        answers[1] = item.text()
        self.label_selected.setText('Выбрано: ' + answers[1])

    def back(self):
        self.switch_window.emit('back')

    def next(self):
        self.switch_window.emit('next')


class Youthfulness(QtWidgets.QMainWindow):
    switch_window = QtCore.pyqtSignal(str)

    def __init__(self):
        super(Youthfulness, self).__init__()
        uic.loadUi('uis/youthfulness.ui', self)

        self.setWindowTitle('Юность')

        self.setWindowIcon(QtGui.QIcon('images/logo.png'))
        self.label_img.setPixmap(QPixmap('images/education.png'))
        self.label_img.setScaledContents(True)

        if answers[2] is not None:
            self.label_selected.setText('Выбрано: ' + answers[2])

        self.comboBox.activated.connect(self.handleActivated)
        self.btn_back.clicked.connect(self.back)
        self.btn_next.clicked.connect(self.next)

    def handleActivated(self, index):
        answers[2] = self.comboBox.itemText(index)
        self.label_selected.setText('Выбрано: ' + answers[2])

    def back(self):
        self.switch_window.emit('back')

    def next(self):
        self.switch_window.emit('next')


class Result(QtWidgets.QMainWindow):
    switch_window = QtCore.pyqtSignal(str)

    def __init__(self):
        super(Result, self).__init__()
        uic.loadUi('uis/result.ui', self)

        self.setWindowTitle('Результаты')
        self.setWindowIcon(QtGui.QIcon('images/logo.png'))

        # запрещаем редактирование таблицы
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)

        # присваиваем значение ячейкам таблицы
        self.tableWidget.setItem(0, 0,
                                 QTableWidgetItem('Выберите любимую кашу'))
        self.tableWidget.setItem(0, 1, QTableWidgetItem(answers[0]))

        self.tableWidget.setItem(1, 0,
                                 QTableWidgetItem('Как вы учились в 5 классе'))
        self.tableWidget.setItem(1, 1, QTableWidgetItem(answers[1]))

        self.tableWidget.setItem(2, 0,
                                 QTableWidgetItem('Какое у вас образование'))
        self.tableWidget.setItem(2, 1, QTableWidgetItem(answers[2]))

        self.btn_back.clicked.connect(self.back)
        self.btn_exit.clicked.connect(self.close)

    def back(self):
        self.switch_window.emit("back")


class Controller:
    """
    Данный контроллер получает сигналы при нажатии на кнопку с помощью switch_window
    Полученный сигнал передаётся в следующее окно:
    приветствие -> детство, детство -> отрочество, отрочество -> юность

    Рассмотрим на примере:
    Программа запускается с метода show_welcome и следовательно из метода
    октрывает окно 'Приветствие'. Когда мы жмём на кнопку 'вперед', то подаётся
    сигнал 'next' в метод show_childhood, в котором закрываем окно 'Приветствие'
     и открываем окно 'Детство'. Теперь нажмём на кнопку 'Назад'. Сигнал 'back'
     подаётся в метод show_boyhood, который закрывает окно 'Детство' и
     открывает окно 'Приветсввие'.

     Строка 'self.welcome.switch_window.connect(self.show_childhood)' говорит
     о том в какой метод дальше пойдёт сигнал
    """
    def __init__(self):
        pass

    def show_welcome(self):
        self.welcome = Welcome()
        self.welcome.switch_window.connect(self.show_childhood)
        self.welcome.show()

    def show_childhood(self, text):
        if text == 'next':
            self.childhood = Childhood()
            self.childhood.switch_window.connect(self.show_boyhood)
            self.welcome.close()
            self.childhood.show()
        else:
            self.childhood = Childhood()
            self.childhood.switch_window.connect(self.show_welcome)
            self.boyhood.close()
            self.childhood.show()

    def show_boyhood(self, text):
        if text == 'next':
            self.boyhood = Boyhood()
            self.boyhood.switch_window.connect(self.show_youthfulness)
            self.childhood.close()
            self.boyhood.show()
        else:
            self.welcome = Welcome()
            self.welcome.switch_window.connect(self.show_childhood)
            self.childhood.close()
            self.welcome.show()

    def show_youthfulness(self, text):
        if text == 'next':
            self.youthfulness = Youthfulness()
            self.youthfulness.switch_window.connect(self.show_result)
            self.boyhood.close()
            self.youthfulness.show()
        else:
            self.childhood = Childhood()
            self.childhood.switch_window.connect(self.show_boyhood)
            self.boyhood.close()
            self.childhood.show()

    def show_result(self, text):
        if text == 'back':
            self.boyhood = Boyhood()
            self.boyhood.switch_window.connect(self.show_youthfulness)
            self.youthfulness.close()
            self.boyhood.show()
        else:
            self.result = Result()
            self.result.switch_window.connect(self.trow_last_back)
            self.youthfulness.close()
            self.result.show()

    def trow_last_back(self, text):
        if text == 'back':
            self.youthfulness = Youthfulness()
            self.youthfulness.switch_window.connect(self.show_result)
            self.result.close()
            self.youthfulness.show()


def main():
    app = QtWidgets.QApplication(sys.argv)
    # программа начинается с класса Controller и его метода show_welcome()
    controller = Controller()
    controller.show_welcome()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
