from PyQt5 import QtWidgets, QtCore

class FileSelectionWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        # Создаем вертикальный layout
        main_layout = QtWidgets.QVBoxLayout()
        
        # Создаем горизонтальный layout для кнопок выбора файлов
        files_layout = QtWidgets.QHBoxLayout()
        
        # Левая часть - первый файл
        left_layout = QtWidgets.QVBoxLayout()
        self.select_file1_btn = QtWidgets.QPushButton('Выбрать файл 1')
        self.select_file1_btn.setFixedSize(150, 40)
        self.file1_label = QtWidgets.QLabel('Файл 1 не выбран')
        self.file1_label.setAlignment(QtCore.Qt.AlignCenter)
        self.file1_label.setWordWrap(True)
        self.file1_label.setStyleSheet("QLabel { background-color: #f0f0f0; padding: 5px; border: 1px solid #ccc; }")
        left_layout.addWidget(self.select_file1_btn, 0, QtCore.Qt.AlignCenter)
        left_layout.addWidget(self.file1_label)
        
        # Правая часть - второй файл
        right_layout = QtWidgets.QVBoxLayout()
        self.select_file2_btn = QtWidgets.QPushButton('Выбрать файл 2')
        self.select_file2_btn.setFixedSize(150, 40)
        self.file2_label = QtWidgets.QLabel('Файл 2 не выбран')
        self.file2_label.setAlignment(QtCore.Qt.AlignCenter)
        self.file2_label.setWordWrap(True)
        self.file2_label.setStyleSheet("QLabel { background-color: #f0f0f0; padding: 5px; border: 1px solid #ccc; }")
        right_layout.addWidget(self.select_file2_btn, 0, QtCore.Qt.AlignCenter)
        right_layout.addWidget(self.file2_label)
        
        # Добавляем левую и правую части в горизонтальный layout
        files_layout.addLayout(left_layout)
        files_layout.addLayout(right_layout)
        
        # Кнопка генерации файла
        self.generate_file_btn = QtWidgets.QPushButton('Сгенерировать файл')
        self.generate_file_btn.setFixedSize(200, 40)
        
        # Создаем компактный список для отображения сгенерированного файла
        self.generated_file_list = QtWidgets.QListWidget()
        self.generated_file_list.setMaximumHeight(60)
        self.generated_file_list.setFixedWidth(250)
        
        # Создаем метку для сгенерированного файла
        generated_file_label = QtWidgets.QLabel('Сгенерированный файл:')
        generated_file_label.setAlignment(QtCore.Qt.AlignCenter)
        
        # Добавляем все виджеты в основной layout
        main_layout.addLayout(files_layout)
        main_layout.addWidget(self.generate_file_btn, 0, QtCore.Qt.AlignCenter)
        
        # Горизонтальный layout для центрирования списка файлов
        file_list_layout = QtWidgets.QHBoxLayout()
        file_list_layout.addStretch()
        file_list_layout.addWidget(self.generated_file_list)
        file_list_layout.addStretch()
        
        # Добавляем метку и центрированный список
        main_layout.addWidget(generated_file_label)
        main_layout.addLayout(file_list_layout)
        
        # Добавляем растягивающееся пространство
        main_layout.addStretch()
        
        # Устанавливаем layout для окна
        self.setLayout(main_layout)
        
        # Настраиваем окно
        self.setWindowTitle('Сравнение оценок')
        self.setFixedSize(600, 400)