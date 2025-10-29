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
        self.file1_path = None
        self.file2_path = None
        self.project_dir = os.path.dirname(os.path.abspath(__file__))
        self.tables_dir = os.path.join(self.project_dir, 'Tables')
        self.generated_filename = "Сравнение оценок.xlsx"
        
        # Очищаем папку Tables при запуске
        self.clean_tables_directory()
        
        self.connect_signals()
        self.clear_generated_file_list()
    
    def clean_tables_directory(self):
        """Очищает папку Tables при запуске"""
        if os.path.exists(self.tables_dir):
            for filename in os.listdir(self.tables_dir):
                file_path = os.path.join(self.tables_dir, filename)
                try:
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception as e:
                    print(f"Ошибка при удалении {file_path}: {e}")
    
    def connect_signals(self):
        # Подключаем обработчики для кнопок выбора файлов
        self.select_file1_btn.clicked.connect(lambda: self.select_file(1))
        self.select_file2_btn.clicked.connect(lambda: self.select_file(2))
        self.generate_file_btn.clicked.connect(self.generate_file)
        self.generated_file_list.itemClicked.connect(self.on_file_clicked)
    
    def ensure_tables_directory(self):
        if not os.path.exists(self.tables_dir):
            os.makedirs(self.tables_dir)
    
    def clear_generated_file_list(self):
        self.generated_file_list.clear()
    
    def show_generated_file(self):
        self.clear_generated_file_list()
        
        generated_file_path = os.path.join(self.tables_dir, self.generated_filename)
        
        if os.path.exists(generated_file_path):
            item = QtWidgets.QListWidgetItem(self.generated_filename)
            item.setData(QtCore.Qt.UserRole, generated_file_path)
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.generated_file_list.addItem(item)
    
    def on_file_clicked(self, item):
        file_path = item.data(QtCore.Qt.UserRole)
        
        if os.path.exists(file_path):
            try:
                if sys.platform == "win32":
                    os.startfile(file_path)
                elif sys.platform == "darwin":
                    subprocess.run(["open", file_path])
                else:
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
    
    def validate_excel_file(self, file_path):
        """Проверяет, что файл является Excel файлом поддерживаемого формата"""
        excel_extensions = {'.xlsx', '.xls', '.xlsm', '.xlsb', '.xltx', '.xltm'}
        file_ext = os.path.splitext(file_path)[1].lower()
        return file_ext in excel_extensions
    
    def select_file(self, file_number):
        """Выбор отдельного файла (1 или 2)"""
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self,
            f'Выберите файл {file_number}',
            '',
            'Excel files (*.xlsx *.xls *.xlsm *.xlsb *.xltx *.xltm);;Все файлы (*)'
        )
        
        if file_path:
            # Проверяем формат файла
            if not self.validate_excel_file(file_path):
                QtWidgets.QMessageBox.warning(
                    self,
                    'Неподдерживаемый формат',
                    f'Выбранный файл имеет неподдерживаемый формат.\n\n'
                    f'Разрешенные форматы: xlsx, xls, xlsm, xlsb, xltx, xltm'
                )
                return
            
            # Сохраняем путь к файлу
            if file_number == 1:
                self.file1_path = file_path
                self.file1_label.setText(f'Файл 1:\n{os.path.basename(file_path)}')
                self.copy_file_to_tables(file_path, 'file1.xlsx')
            else:
                self.file2_path = file_path
                self.file2_label.setText(f'Файл 2:\n{os.path.basename(file_path)}')
                self.copy_file_to_tables(file_path, 'file2.xlsx')
            
            # Показываем сообщение об успешной загрузке
            QtWidgets.QMessageBox.information(
                self,
                'Файл загружен',
                f'Файл {file_number} успешно загружен!\n\n'
                f'{os.path.basename(file_path)}'
            )
    
    def copy_file_to_tables(self, source_path, target_filename):
        """Копирует один файл в папку Tables"""
        try:
            self.ensure_tables_directory()
            target_path = os.path.join(self.tables_dir, target_filename)
            shutil.copy2(source_path, target_path)
            return True
        except Exception as e:
            QtWidgets.QMessageBox.critical(
                self,
                'Ошибка копирования',
                f'Не удалось скопировать файл: {str(e)}'
            )
            return False
    
    def check_files_ready(self):
        """Проверяет, готовы ли оба файла для генерации"""
        messages = []
        
        # Проверяем что оба файла выбраны
        if not self.file1_path:
            messages.append("• Файл 1 не выбран")
        if not self.file2_path:
            messages.append("• Файл 2 не выбран")
        
        # Проверяем существование файлов в папке Tables
        file1_exists = os.path.exists(os.path.join(self.tables_dir, 'file1.xlsx'))
        file2_exists = os.path.exists(os.path.join(self.tables_dir, 'file2.xlsx'))
        
        if self.file1_path and not file1_exists:
            messages.append("• Файл 1 не найден в папке Tables")
        if self.file2_path and not file2_exists:
            messages.append("• Файл 2 не найден в папке Tables")
        
        if messages:
            error_msg = "Для генерации файла необходимо:\n\n" + "\n".join(messages)
            QtWidgets.QMessageBox.warning(
                self,
                'Файлы не готовы',
                error_msg
            )
            return False
        
        return True
    
    def generate_file(self):
        try:
            # Проверяем готовность файлов
            if not self.check_files_ready():
                return
            
            # Используем QProgressDialog для прогресса
            progress_dialog = QtWidgets.QProgressDialog(self)
            progress_dialog.setWindowTitle('Генерация файла')
            progress_dialog.setLabelText('Идет создание файла "Сравнение оценок.xlsx"...')
            progress_dialog.setCancelButton(None)
            progress_dialog.setRange(0, 0)
            progress_dialog.setModal(True)
            progress_dialog.show()
            
            QtWidgets.QApplication.processEvents()
            
            # Запускаем генерацию файла
            success = fw.create_file(self)
            
            # Закрываем диалог прогресса
            progress_dialog.close()
            
            if success:
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

def main():
    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationName('Сравнение оценок')
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()