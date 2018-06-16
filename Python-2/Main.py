import re
import sys

from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi


class Main(QDialog):
    def __init__(self):
        super(Main, self).__init__()
        loadUi('uis/main.ui', self)

        self.setWindowTitle('Работа со строками в Python')
        self.setWindowIcon(QtGui.QIcon('images/logo.png'))

        self.btn_solve.clicked.connect(self.solve)
        self.btn_clear.clicked.connect(self.clear)

    def solve(self):
        text = self.textEdit_text.toPlainText()  # получаем наш текст

        # для строки "СВЕТА РОЕТ РОВ, ВОВКА СЕЕТ ОВЁС"
        # получится список: ['СВЕТА', 'РОЕТ', 'РОВ', 'ВОВКА', 'СЕЕТ']
        #
        # \b -- ищет границы слов
        # [АВСТРХОНКМУЕ] -- описывает что ищем
        # + -- говорит, что искать нужно минимум от 1 символа
        for word in re.findall(r'\b[АВСТРХОНКМУЕ]+\b', text):
            self.textEdit_words.insertPlainText(word + " ")

    def clear(self):
        self.textEdit_text.clear()
        self.textEdit_words.clear()


def main():
    app = QApplication(sys.argv)
    window = Main()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
