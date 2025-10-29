from PyQt5 import QtWidgets, QtCore, QtGui

class FileSelectionWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        # Устанавливаем красивый фон
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                                          stop: 0 #667eea, stop: 1 #764ba2);
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            
            QPushButton {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                          stop: 0 #6a11cb, stop: 1 #2575fc);
                color: white;
                border: none;
                border-radius: 15px;
                padding: 10px;
                font-size: 14px;
                font-weight: bold;
                min-width: 150px;
                min-height: 40px;
            }
            
            QPushButton:hover {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                          stop: 0 #7d1ee8, stop: 1 #3680ff);
                transform: scale(1.05);
            }
            
            QPushButton:pressed {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                          stop: 0 #5a0cb3, stop: 1 #1c68e8);
            }
            
            QPushButton:disabled {
                background: #cccccc;
                color: #666666;
            }
            
            QLabel {
                color: white;
                font-size: 13px;
                padding: 5px;
            }
            
            QListWidget {
                background: rgba(255, 255, 255, 0.9);
                border: 2px solid #6a11cb;
                border-radius: 10px;
                padding: 5px;
                font-size: 12px;
                color: #333333;
            }
            
            QListWidget::item {
                border-bottom: 1px solid #e0e0e0;
                padding: 8px;
            }
            
            QListWidget::item:selected {
                background: #6a11cb;
                color: white;
                border-radius: 5px;
            }
            
            QListWidget::item:hover {
                background: #f0f0f0;
                border-radius: 5px;
            }
        """)
        
        # Создаем вертикальный layout
        main_layout = QtWidgets.QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(30, 30, 30, 30)
        
        # Заголовок приложения
        title_label = QtWidgets.QLabel('📊 S.S.S.')
        title_label.setAlignment(QtCore.Qt.AlignCenter)
        title_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 28px;
                font-weight: bold;
                padding: 20px;
                background: rgba(106, 17, 203, 0.7);
                border-radius: 20px;
                margin: 10px;
            }
        """)
        main_layout.addWidget(title_label)
        
        # Создаем горизонтальный layout для кнопок выбора файлов
        files_layout = QtWidgets.QHBoxLayout()
        files_layout.setSpacing(30)
        
        # Левая часть - первый файл
        left_widget = QtWidgets.QWidget()
        left_widget.setStyleSheet("""
            QWidget {
                background: rgba(255, 255, 255, 0.1);
                border: 2px solid rgba(255, 255, 255, 0.3);
                border-radius: 15px;
                padding: 15px;
            }
        """)
        left_layout = QtWidgets.QVBoxLayout(left_widget)
        
        file1_icon = QtWidgets.QLabel('📊')
        file1_icon.setAlignment(QtCore.Qt.AlignCenter)
        file1_icon.setStyleSheet("font-size: 24px;")
        left_layout.addWidget(file1_icon)
        
        self.select_file1_btn = QtWidgets.QPushButton('Выбрать файл 1')
        self.select_file1_btn.setFixedSize(160, 45)
        left_layout.addWidget(self.select_file1_btn, 0, QtCore.Qt.AlignCenter)
        
        self.file1_label = QtWidgets.QLabel('Файл 1 не выбран')
        self.file1_label.setAlignment(QtCore.Qt.AlignCenter)
        self.file1_label.setWordWrap(True)
        self.file1_label.setStyleSheet("""
            QLabel {
                background: rgba(255, 255, 255, 0.9);
                color: #333333;
                padding: 10px;
                border-radius: 10px;
                border: 1px solid #6a11cb;
                font-weight: bold;
                min-height: 40px;
            }
        """)
        left_layout.addWidget(self.file1_label)
        
        # Правая часть - второй файл
        right_widget = QtWidgets.QWidget()
        right_widget.setStyleSheet("""
            QWidget {
                background: rgba(255, 255, 255, 0.1);
                border: 2px solid rgba(255, 255, 255, 0.3);
                border-radius: 15px;
                padding: 15px;
            }
        """)
        right_layout = QtWidgets.QVBoxLayout(right_widget)
        
        file2_icon = QtWidgets.QLabel('📈')
        file2_icon.setAlignment(QtCore.Qt.AlignCenter)
        file2_icon.setStyleSheet("font-size: 24px;")
        right_layout.addWidget(file2_icon)
        
        self.select_file2_btn = QtWidgets.QPushButton('Выбрать файл 2')
        self.select_file2_btn.setFixedSize(160, 45)
        right_layout.addWidget(self.select_file2_btn, 0, QtCore.Qt.AlignCenter)
        
        self.file2_label = QtWidgets.QLabel('Файл 2 не выбран')
        self.file2_label.setAlignment(QtCore.Qt.AlignCenter)
        self.file2_label.setWordWrap(True)
        self.file2_label.setStyleSheet("""
            QLabel {
                background: rgba(255, 255, 255, 0.9);
                color: #333333;
                padding: 10px;
                border-radius: 10px;
                border: 1px solid #6a11cb;
                font-weight: bold;
                min-height: 40px;
            }
        """)
        right_layout.addWidget(self.file2_label)
        
        # Добавляем левую и правую части в горизонтальный layout
        files_layout.addWidget(left_widget)
        files_layout.addWidget(right_widget)
        
        # Кнопка генерации файла
        generate_widget = QtWidgets.QWidget()
        generate_widget.setStyleSheet("""
            QWidget {
                background: rgba(255, 255, 255, 0.1);
                border: 2px solid rgba(255, 255, 255, 0.3);
                border-radius: 15px;
                padding: 15px;
            }
        """)
        generate_layout = QtWidgets.QVBoxLayout(generate_widget)
        
        generate_icon = QtWidgets.QLabel('✨')
        generate_icon.setAlignment(QtCore.Qt.AlignCenter)
        generate_icon.setStyleSheet("font-size: 28px;")
        generate_layout.addWidget(generate_icon)
        
        self.generate_file_btn = QtWidgets.QPushButton('Сгенерировать файл сравнения')
        self.generate_file_btn.setFixedSize(280, 50)  # Увеличили ширину кнопки
        self.generate_file_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                          stop: 0 #FF416C, stop: 1 #FF4B2B);
                font-size: 16px;
                min-width: 280px;
            }
            QPushButton:hover {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                          stop: 0 #FF4B7B, stop: 1 #FF5C40);
            }
        """)
        generate_layout.addWidget(self.generate_file_btn, 0, QtCore.Qt.AlignCenter)
        
        # Создаем компактный список для отображения сгенерированного файла
        result_widget = QtWidgets.QWidget()
        result_widget.setStyleSheet("""
            QWidget {
                background: rgba(255, 255, 255, 0.1);
                border: 2px solid rgba(255, 255, 255, 0.3);
                border-radius: 15px;
                padding: 15px;
            }
        """)
        result_layout = QtWidgets.QVBoxLayout(result_widget)
        
        result_icon = QtWidgets.QLabel('📁')
        result_icon.setAlignment(QtCore.Qt.AlignCenter)
        result_icon.setStyleSheet("font-size: 20px;")
        result_layout.addWidget(result_icon)
        
        generated_file_label = QtWidgets.QLabel('Сгенерированный файл:')
        generated_file_label.setAlignment(QtCore.Qt.AlignCenter)
        generated_file_label.setStyleSheet("font-size: 14px; font-weight: bold; color: white;")
        result_layout.addWidget(generated_file_label)
        
        self.generated_file_list = QtWidgets.QListWidget()
        self.generated_file_list.setMaximumHeight(70)
        self.generated_file_list.setFixedWidth(280)
        result_layout.addWidget(self.generated_file_list, 0, QtCore.Qt.AlignCenter)
        
        # Добавляем все виджеты в основной layout
        main_layout.addLayout(files_layout)
        main_layout.addWidget(generate_widget)
        main_layout.addWidget(result_widget)
        
        # Добавляем информацию о разработчике
        footer_label = QtWidgets.QLabel('Для сравнения оценок учеников • Загрузите два Excel файла')
        footer_label.setAlignment(QtCore.Qt.AlignCenter)
        footer_label.setStyleSheet("""
            QLabel {
                color: rgba(255, 255, 255, 0.7);
                font-size: 11px;
                padding: 10px;
                font-style: italic;
            }
        """)
        main_layout.addWidget(footer_label)
        
        # Устанавливаем layout для окна
        self.setLayout(main_layout)
        
        # Настраиваем окно
        self.setWindowTitle('📊 S.S.S.')
        self.setFixedSize(720, 650)  # Немного увеличили ширину для кнопки
        
        # Добавляем анимацию для кнопок
        self.setupAnimations()
    
    def setupAnimations(self):
        """Настраивает анимации для кнопок"""
        # Анимация для кнопки генерации
        self.generate_animation = QtCore.QPropertyAnimation(self.generate_file_btn, b"geometry")
        self.generate_animation.setDuration(200)
        
        # Анимация для файловых кнопок
        self.file1_animation = QtCore.QPropertyAnimation(self.select_file1_btn, b"geometry")
        self.file1_animation.setDuration(150)
        
        self.file2_animation = QtCore.QPropertyAnimation(self.select_file2_btn, b"geometry")
        self.file2_animation.setDuration(150)