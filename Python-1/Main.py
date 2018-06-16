import sys
from random import randint

from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi


class Main(QDialog):
    def __init__(self):
        super(Main, self).__init__()
        loadUi('uis/main.ui', self)  # загрузка формы в py-скрипт

        self.setWindowTitle('Работа с визуальными табличными данными в Python')
        self.setWindowIcon(QtGui.QIcon('images/logo.png'))

        self.btn_random_number.clicked.connect(self.fill_random_numbers)
        self.btn_solve.clicked.connect(self.solve)

    def fill_random_numbers(self):
        """
        заполняем таблицу случайными числами
        :return:
        """
        i = 0
        j = 0

        # заполняем таблицу случайными числами
        while i < self.tableWidget.columnCount():
            while j <= self.tableWidget.rowCount():
                random_num = randint(0, 101)
                self.tableWidget.setItem(i, j,
                                         QTableWidgetItem(str(random_num)))
                j += 1

            i += 1
            j = 0

        # находим максимальное число и его координаты
        # [0] - максимальное число, [1] - x-координата, [2] - y-координата
        list_information_max_num = find_max(table_widget=self.tableWidget)

        if not list_information_max_num:
            self.label_error.setText('Введены неправильные данные!')
        else:
            # выводим на кэран информацию о расположении максимального числа
            self.label_max_el.setText(
                'Максимальный элемент: ' + str(
                    list_information_max_num[0]) + ' [' +
                str(list_information_max_num[1]) + ';' + str(
                    list_information_max_num[2])
                + ']')

    def solve(self):
        list_information_max_num = find_max(self.tableWidget)

        if not list_information_max_num:
            self.label_error.setText('Введены некорректные данные!')
        else:
            self.label_max_el.setText(
                'Максимальный элемент: ' + str(
                    list_information_max_num[0]) + ' [' +
                str(list_information_max_num[1]) + ';' + str(
                    list_information_max_num[2])
                + ']')

            # -*- решение задания -*-
            i = 0
            j = 0

            number_of_units = 0 # количество единиц, стоящих перед нашим числом
            flag = False

            while i < self.tableWidget.columnCount():
                while j <= self.tableWidget.rowCount():
                    item = self.tableWidget.item(i, j).text()

                    # три случая:
                    # 1) элемент равен единице
                    # 2) элемент равен максимальному числу
                    #   2.1) максимальный элемент раплолагается в 1-ой ячейке
                    # 3) элемент равен иному числу
                    if str(item) == str(1):
                        number_of_units += 1
                        j += 1
                    elif float(item) == list_information_max_num[0]:
                        if i == 0 and j == 0:
                            self.tableWidget.setItem(i, j, QTableWidgetItem(
                                str(item)))
                        else:
                            self.tableWidget.setItem(i, j, QTableWidgetItem(
                                str(number_of_units)))

                        self.label_sum.setText('Сумма единиц перед '
                                               'максимальным элементом: ' +
                                               str(number_of_units))
                        flag = True
                        break
                    else:
                        self.label_sum.setText('Сумма единиц перед '
                                               'максимальным элементом: 0')
                        flag = True
                        break

                if flag:
                    break

                i += 1
                j = 0

            self.label_error.setText('')


def find_max(table_widget):
    """
    находим максимальное число из таблицы и его координаты
    :param table_widget: таблица
    :return: [max_num, x_max_number, y_max_number], если выкинуто исключение,
            то None
    """
    i = 0
    j = 0

    max_num = float('-inf')
    x_max_number = 0  # номер строки, в котором находится максимальне число
    y_max_number = 0  # номер столбца, в котором находится максимальне число

    try:
        while i < table_widget.columnCount() - 1:
            while j <= table_widget.rowCount():
                number = float(table_widget.item(i, j).text())

                if number > max_num:
                    max_num = number
                    x_max_number = j + 1
                    y_max_number = i + 1

                j += 1

            i += 1
            j = 0

        return [max_num, x_max_number, y_max_number]
    except Exception:
        return None


def main():
    app = QApplication(sys.argv)
    window = Main()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
