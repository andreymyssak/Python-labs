import math
import sys
from random import randint

from PyQt5 import QtGui
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi


class Main(QDialog):
    def __init__(self):
        super(Main, self).__init__()
        loadUi('uis/main.ui', self)

        self.setWindowTitle('Сложные табличные вычисления в Python')

        self.setWindowIcon(QtGui.QIcon('images/logo.png'))
        self.label_img.setPixmap(QPixmap('images/task.png'))
        self.label_img.setScaledContents(True)

        self.btn_random_number.clicked.connect(self.fill_random_numbers)
        self.btn_solve.clicked.connect(self.solve)
        self.btn_clear.clicked.connect(self.clear)
        self.btn_exit.clicked.connect(self.exit)

    def fill_random_numbers(self):
        """
        заполняем таблицу случайными числами
        :return: pass
        """
        i = 0

        while i < self.tableWidget.rowCount():
            random_num = randint(0, 101)
            self.tableWidget.setItem(i, 0, QTableWidgetItem(str(random_num)))
            i += 1

    def solve(self):

        if validation_of_data(self.tableWidget):
            i = 0
            j = 1

            multiplication_of_k_i_minus_1 = 1
            sum_of_k_i = 0

            while i < self.tableWidget.rowCount():
                item = self.tableWidget.item(i, 0).text()
                sum_of_k_i += int(item)
                try:
                    # item_minus_1 выкинет исключение при первой итерации,
                    # поэтому перехватываем её и выводим none
                    item_minus_1 = self.tableWidget.item(i - 1, 0).text()
                    multiplication_of_k_i_minus_1 *= int(item_minus_1)
                    difference_of_sin_of_k_i_and_cos_of_k_minus_1 = (math.sin(
                        int(item)) ** 2 - math.cos(int(item_minus_1)) ** 2)

                    answer = (((sum_of_k_i ** 2) ** (1 / 3.0)) /
                              float(multiplication_of_k_i_minus_1)) * \
                             difference_of_sin_of_k_i_and_cos_of_k_minus_1 ** 3

                    self.tableWidget.setItem(i, j,
                                             QTableWidgetItem(str(answer)))
                except Exception:
                    self.tableWidget.setItem(i, j, QTableWidgetItem('none'))

                i += 1

            self.label_error.setText('')
        else:
            self.label_error.setText('Введены некорректные данные!')

    def clear(self):
        self.tableWidget.clearContents()

    def exit(self):
        self.close()


def validation_of_data(table_widget):
    """
    проверяем данные на валидность
    :param table_widget: таблица с числами
    :return: True - данные корректны, False - есть некорректные данные
    """
    i = 0
    while i < table_widget.rowCount():
        try:
            float(table_widget.item(i, 0).text())
            i += 1
        except Exception:
            return False

    return True


def main():
    app = QApplication(sys.argv)
    window = Main()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
