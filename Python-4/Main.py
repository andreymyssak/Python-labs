import re
import sys

from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi

list_of_numbers = []


class Main(QDialog):
    def __init__(self):
        super(Main, self).__init__()
        loadUi('uis/main.ui', self)

        self.setWindowTitle('Работа с массивами и файлами в Python')
        self.setWindowIcon(QtGui.QIcon('images/logo.png'))

        self.btn_upload_data.clicked.connect(self.upload_data_from_file)
        self.btn_process_data.clicked.connect(self.process_data)
        self.btn_save_data.clicked.connect(self.save_data_in_file)
        self.btn_clear.clicked.connect(self.clear)

    def upload_data_from_file(self):
        """
        загружаем данные из файла
        :return: pass
        """
        global path_to_file
        path_to_file = QFileDialog.getOpenFileName(self, 'Открыть файл', '',
                                                   "Text Files (*.txt)")[0]

        if path_to_file:
            file = open(path_to_file, 'r')

            data = file.read()
            # выводим считанные данные на экран
            self.plainTextEdit.appendPlainText("Полученные данные: \n" +
                                               data + "\n")

            global list_of_numbers
            list_of_numbers = []

            # \b -- ищет границы слов
            # [0-9] -- описывает что ищем
            # + -- говорит, что искать нужно минимум от 1 символа
            for num in re.findall(r'\b[0-9]+\b', data):
                list_of_numbers.append(num)

    def process_data(self):
        if validation_of_data():
            max_num = find_max()
            sum_of_first_row = find_sum_of_first_row()

            # -*- выполнение задания -*-
            if max_num != sum_of_first_row:
                increasing_max_num_of_double(max_num)

                self.plainTextEdit.appendPlainText(
                    "Данные обработаны! " + '\n')

                # выводим список на экран
                for i in list_of_numbers:
                    self.plainTextEdit.insertPlainText(str(i) + " ")
                    # чтобы текст был в виде таблицы, делаем отступ после
                    # 6 элемента
                    if int(i) % 6 == 0:
                        self.plainTextEdit.appendPlainText("")
            else:
                self.plainTextEdit.appendPlainText(
                    "Сумма элементов первой строки равна максимальному "
                    "элементу таблицы! \n")
        else:
            self.plainTextEdit.appendPlainText("Неправильно введены данные! "
                                               "Таблица должна быть размером "
                                               "5х6 и состоять из чисел! \n")

    def save_data_in_file(self):
        """
        сохраняем данные в выбранным нами файл
        :return:
        """

        try:
            if path_to_file:
                file = open(path_to_file.split(".")[0] + '-Output.txt', 'w')

                for i in list_of_numbers:
                    file.write(i + " ")
                    if int(i) % 6 == 0:
                        file.write("\n")

                file.close()

                self.plainTextEdit.appendPlainText(
                    "Файл был успешно загружен! \n")
            else:
                self.plainTextEdit.appendPlainText("Для начала загрузите файл!")
        except Exception:
            self.plainTextEdit.appendPlainText("Для начала загрузите файл!")

    def clear(self):
        self.plainTextEdit.clear()


def find_max():
    """
    находим максимальное число в списке
    :return: максимальное число
    """
    max_num = float('-inf')

    for i in list_of_numbers:
        if max_num < int(i):
            max_num = int(i)

    return max_num


def validation_of_data():
    """
    проверяем данные на валидность: всего должно быть ровно 30 ЧИСЕЛ
    :return: True - данные корректны, False - нет
    """
    if len(list_of_numbers) == 30:
        for i in list_of_numbers:
            try:
                float(i)
            except Exception:
                return False

        return True
    else:
        return False


def increasing_max_num_of_double(max_num):
    """
    увеличение максимального числа в два раза
    :param max_num: максимальное число
    :return: pass
    """
    for n, i in enumerate(list_of_numbers):
        if int(i) == max_num:
            list_of_numbers[n] = str(max_num * 2)
            break
    pass


def find_sum_of_first_row():
    """
    находим сумму чисел из первой строки таблицы
    :return: сумму чисел из первой строки
    """
    sum = 0
    i = 0

    while i < 6:  # в строке должно быть ровно 6 чисел
        sum += int(list_of_numbers[i])
        i += 1

    return sum


def main():
    app = QApplication(sys.argv)
    window = Main()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
