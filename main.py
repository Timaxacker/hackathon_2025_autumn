import sys
import os
import shutil
import subprocess
from PyQt5 import QtWidgets, QtCore
from front import FileSelectionWindow
import file_worker as fw

class MainWindow(FileSelectionWindow):
    def __init__(self):
        super().__init__()
        self.selected_files = []
        self.project_dir = os.path.dirname(os.path.abspath(__file__))
        self.tables_dir = os.path.join(self.project_dir, 'Tables')
        self.generated_filename = "Сравнение оценок.xlsx"
        self.connect_signals()
        self.clear_generated_file_list()  # Очищаем список при запуске
    
    def connect_signals(self):
        # Подключаем обработчики нажатия на кнопки
        self.select_files_btn.clicked.connect(self.select_files)
        self.generate_file_btn.clicked.connect(self.generate_file)
        
        # Подключаем обработчик клика по файлу в списке
        self.generated_file_list.itemClicked.connect(self.on_file_clicked)
    
    def ensure_tables_directory(self):
        """Создает папку Tables, если она не существует"""
        if not os.path.exists(self.tables_dir):
            os.makedirs(self.tables_dir)
            print(f"Создана папка: {self.tables_dir}")
    
    def clear_generated_file_list(self):
        """Очищает список сгенерированных файлов"""
        self.generated_file_list.clear()
    
    def show_generated_file(self):
        """Показывает сгенерированный файл в списке"""
        self.clear_generated_file_list()
        
        generated_file_path = os.path.join(self.tables_dir, self.generated_filename)
        
        if os.path.exists(generated_file_path):
            item = QtWidgets.QListWidgetItem(self.generated_filename)
            item.setData(QtCore.Qt.UserRole, generated_file_path)
            
            # Центрируем текст в элементе списка
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            
            self.generated_file_list.addItem(item)
    
    def on_file_clicked(self, item):
        """Обработчик клика по файлу - открывает файл"""
        file_path = item.data(QtCore.Qt.UserRole)
        
        if os.path.exists(file_path):
            try:
                # Открываем файл с помощью системного приложения по умолчанию
                if sys.platform == "win32":
                    os.startfile(file_path)
                elif sys.platform == "darwin":  # macOS
                    subprocess.run(["open", file_path])
                else:  # linux
                    subprocess.run(["xdg-open", file_path])
                    
            except Exception as e:
                QtWidgets.QMessageBox.warning(
                    self,
                    'Ошибка открытия',
                    f'Не удалось открыть файл: {str(e)}'
                )
        else:
            QtWidgets.QMessageBox.warning(
                self,
                'Файл не найден',
                f'Файл не существует: {file_path}'
            )
    
    def generate_file(self):
        """Запускает функцию создания файла и показывает его в списке"""
        try:
            # Убеждаемся, что папка Tables существует
            self.ensure_tables_directory()
            
            # Запускаем вашу функцию создания файла
            fw.create_file()
            
            # Показываем сгенерированный файл в списке
            self.show_generated_file()
            
            # Показываем сообщение об успехе
            QtWidgets.QMessageBox.information(
                self,
                'Файл создан',
                f'Файл "{self.generated_filename}" успешно создан!\n\n'
                'Кликните на него в списке чтобы открыть.'
            )
            
        except Exception as e:
            QtWidgets.QMessageBox.critical(
                self,
                'Ошибка',
                f'Не удалось создать файл: {str(e)}'
            )
    
    def select_files(self):
        # Открываем диалог выбора файлов
        files, _ = QtWidgets.QFileDialog.getOpenFileNames(
            self,
            'Выберите 2 файла',
            '',
            'Все файлы (*)'
        )
        
        if files:
            if len(files) == 2:
                self.selected_files = files
                if self.copy_files_to_tables():
                    self.update_files_label()
                    self.show_success_message()
            else:
                QtWidgets.QMessageBox.warning(
                    self, 
                    'Ошибка', 
                    'Пожалуйста, выберите ровно 2 файла'
                )
    
    def copy_files_to_tables(self):
        try:
            # Убеждаемся, что папка Tables существует
            self.ensure_tables_directory()
            
            # Формируем полные пути для новых файлов
            file1_path = os.path.join(self.tables_dir, 'file2.xlsx')
            file2_path = os.path.join(self.tables_dir, 'file1.xlsx')
            
            # Копируем первый файл как file1.xlsx
            shutil.copy2(self.selected_files[0], file1_path)
            
            # Копируем второй файл как file2.xlsx
            shutil.copy2(self.selected_files[1], file2_path)
            
            return True
            
        except Exception as e:
            QtWidgets.QMessageBox.critical(
                self,
                'Ошибка копирования',
                f'Не удалось скопировать файлы: {str(e)}'
            )
            return False
    
    def update_files_label(self):
        # Обновляем метку с именами выбранных файлов (убрали упоминание о Tables)
        file_names = [os.path.basename(file) for file in self.selected_files]
        self.files_label.setText(
            f'Выбраны файлы:\n'
            f'{file_names[0]}\n'
            f'{file_names[1]}'
        )
    
    def show_success_message(self):
        # Показываем сообщение об успешном копировании (убрали упоминание о Tables)
        QtWidgets.QMessageBox.information(
            self,
            'Файлы выбраны',
            f'Файлы успешно выбраны:\n\n'
            f'{os.path.basename(self.selected_files[0])}\n'
            f'{os.path.basename(self.selected_files[1])}'
        )

def main():
    app = QtWidgets.QApplication(sys.argv)
    
    # Устанавливаем русскую локаль
    translator = QtCore.QTranslator()
    app.setApplicationName('File Selector')
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()