from PyQt5 import QtWidgets, QtCore

class FileSelectionWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        # Создаем вертикальный layout
        layout = QtWidgets.QVBoxLayout()
        
        # Создаем кнопку для выбора файлов
        self.select_files_btn = QtWidgets.QPushButton('Выбрать файлы')
        self.select_files_btn.setFixedSize(150, 40)
        
        # Создаем кнопку для генерации файла
        self.generate_file_btn = QtWidgets.QPushButton('Сгенерировать файл')
        self.generate_file_btn.setFixedSize(150, 40)
        
        # Создаем метку для отображения выбранных файлов
        self.files_label = QtWidgets.QLabel('Файлы не выбраны')
        self.files_label.setAlignment(QtCore.Qt.AlignCenter)
        self.files_label.setWordWrap(True)
        
        # Создаем компактный список для отображения сгенерированного файла
        self.generated_file_list = QtWidgets.QListWidget()
        self.generated_file_list.setMaximumHeight(60)  # Уменьшаем высоту
        self.generated_file_list.setFixedWidth(250)    # Устанавливаем ширину
        
        # Создаем метку для сгенерированного файла
        generated_file_label = QtWidgets.QLabel('Сгенерированный файл:')
        generated_file_label.setAlignment(QtCore.Qt.AlignCenter)
        
        # Добавляем виджеты в layout
        layout.addWidget(self.select_files_btn, 0, QtCore.Qt.AlignCenter)
        layout.addWidget(self.generate_file_btn, 0, QtCore.Qt.AlignCenter)
        layout.addWidget(self.files_label)
        
        # Горизонтальный layout для центрирования списка файлов
        file_list_layout = QtWidgets.QHBoxLayout()
        file_list_layout.addStretch()
        file_list_layout.addWidget(self.generated_file_list)
        file_list_layout.addStretch()
        
        # Добавляем метку и центрированный список
        layout.addWidget(generated_file_label)
        layout.addLayout(file_list_layout)
        
        # Добавляем растягивающееся пространство
        layout.addStretch()
        
        # Устанавливаем layout для окна
        self.setLayout(layout)
        
        # Настраиваем окно
        self.setWindowTitle('Выбор файлов')
        self.setFixedSize(400, 350)  # Уменьшаем размер окна