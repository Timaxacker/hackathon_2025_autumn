import pandas as pd
import os
import re
from PyQt5 import QtWidgets, QtCore


def show_error_message(message, parent=None):
    """Показывает сообщение об ошибке в отдельном окне"""
    msg = QtWidgets.QMessageBox(parent)
    msg.setIcon(QtWidgets.QMessageBox.Critical)
    msg.setWindowTitle("Ошибка")
    msg.setText(message)
    msg.exec_()


def is_valid_name(name):
    """Проверяет, что фамилия состоит из букв и допустимых символов"""
    if pd.isna(name):
        return False
    # Разрешаем буквы, дефисы, апострофы и пробелы (для двойных фамилий)
    pattern = r'^[a-zA-Zа-яА-ЯёЁ\-"\'\s]+$'
    return bool(re.match(pattern, str(name).strip()))


def create_file(parent=None):
    try:
        # Даем GUI обновиться перед началом обработки
        if parent:
            QtWidgets.QApplication.processEvents()

        # Проверяем существование файлов
        file1_path = 'Tables/file1.xlsx'
        file2_path = 'Tables/file2.xlsx'
        
        if not os.path.exists(file1_path) or not os.path.exists(file2_path):
            show_error_message("Файлы для генерации не найдены", parent)
            return False

        # Проверяем размеры файлов
        if os.path.getsize(file1_path) == 0 or os.path.getsize(file2_path) == 0:
            show_error_message("Один из файлов пустой", parent)
            return False

        if parent:
            QtWidgets.QApplication.processEvents()

        # Загружаем данные
        try:
            df1 = pd.read_excel(file1_path)
            df2 = pd.read_excel(file2_path)
        except Exception as e:
            show_error_message(f"Ошибка при чтении Excel файлов: {str(e)}", parent)
            return False

        if parent:
            QtWidgets.QApplication.processEvents()

        # Проверяем что файлы не пустые
        if df1.empty:
            show_error_message("Файл 1 не содержит данных", parent)
            return False
        if df2.empty:
            show_error_message("Файл 2 не содержит данных", parent)
            return False

        # Проверяем наличие необходимых колонок
        missing_columns_1 = []
        missing_columns_2 = []
        
        if 'ученик' not in df1.columns:
            missing_columns_1.append("'ученик'")
        if 'оценка' not in df1.columns:
            missing_columns_1.append("'оценка'")
        if 'ученик' not in df2.columns:
            missing_columns_2.append("'ученик'")
        if 'оценка' not in df2.columns:
            missing_columns_2.append("'оценка'")
            
        error_messages = []
        if missing_columns_1:
            error_messages.append(f"В файле 1 отсутствуют колонки: {', '.join(missing_columns_1)}")
        if missing_columns_2:
            error_messages.append(f"В файле 2 отсутствуют колонки: {', '.join(missing_columns_2)}")
            
        if error_messages:
            show_error_message("\n".join(error_messages), parent)
            return False

        if parent:
            QtWidgets.QApplication.processEvents()

        # ПРОВЕРЯЕМ КОРРЕКТНОСТЬ ДАННЫХ ФАМИЛИЙ
        invalid_names_1 = []
        invalid_names_2 = []
        
        for idx, name in enumerate(df1['ученик'], 1):
            if not is_valid_name(name):
                invalid_names_1.append(f"Строка {idx}: '{name}'")
                
        for idx, name in enumerate(df2['ученик'], 1):
            if not is_valid_name(name):
                invalid_names_2.append(f"Строка {idx}: '{name}'")
        
        name_error_messages = []
        if invalid_names_1:
            name_error_messages.append(f"Файл 1 - некорректные фамилии:\n" + "\n".join(invalid_names_1[:10]))  # Показываем первые 10 ошибок
            if len(invalid_names_1) > 10:
                name_error_messages[-1] += f"\n... и еще {len(invalid_names_1) - 10} ошибок"
                
        if invalid_names_2:
            name_error_messages.append(f"Файл 2 - некорректные фамилии:\n" + "\n".join(invalid_names_2[:10]))
            if len(invalid_names_2) > 10:
                name_error_messages[-1] += f"\n... и еще {len(invalid_names_2) - 10} ошибок"
        
        if name_error_messages:
            show_error_message("Обнаружены некорректные данные в колонке 'ученик':\n\n" + 
                             "\n\n".join(name_error_messages) + 
                             "\n\nФамилии должны состоять только из букв, дефисов, апострофов и пробелов.", 
                             parent)
            return False

        # ПРОВЕРЯЕМ КОРРЕКТНОСТЬ ДАННЫХ ОЦЕНОК
        try:
            df1['оценка'] = pd.to_numeric(df1['оценка'], errors='coerce')
            df2['оценка'] = pd.to_numeric(df2['оценка'], errors='coerce')
            
            invalid_marks_1 = []
            invalid_marks_2 = []
            
            # Проверяем файл 1
            for idx, (mark, is_na) in enumerate(zip(df1['оценка'], df1['оценка'].isna()), 1):
                if is_na:
                    invalid_marks_1.append(f"Строка {idx}: не является числом")
                elif mark < 2 or mark > 5:
                    invalid_marks_1.append(f"Строка {idx}: {mark} (допустимый диапазон: 2-5)")
            
            # Проверяем файл 2
            for idx, (mark, is_na) in enumerate(zip(df2['оценка'], df2['оценка'].isna()), 1):
                if is_na:
                    invalid_marks_2.append(f"Строка {idx}: не является числом")
                elif mark < 2 or mark > 5:
                    invalid_marks_2.append(f"Строка {idx}: {mark} (допустимый диапазон: 2-5)")
            
            mark_error_messages = []
            if invalid_marks_1:
                mark_error_messages.append(f"Файл 1 - некорректные оценки:\n" + "\n".join(invalid_marks_1[:10]))
                if len(invalid_marks_1) > 10:
                    mark_error_messages[-1] += f"\n... и еще {len(invalid_marks_1) - 10} ошибок"
                    
            if invalid_marks_2:
                mark_error_messages.append(f"Файл 2 - некорректные оценки:\n" + "\n".join(invalid_marks_2[:10]))
                if len(invalid_marks_2) > 10:
                    mark_error_messages[-1] += f"\n... и еще {len(invalid_marks_2) - 10} ошибок"
            
            if mark_error_messages:
                show_error_message("Обнаружены некорректные данные в колонке 'оценка':\n\n" + 
                                 "\n\n".join(mark_error_messages) + 
                                 "\n\nОценки должны быть числами от 2 до 5.", 
                                 parent)
                return False
                
        except Exception as e:
            show_error_message(f"Ошибка при обработке данных оценок: {str(e)}", parent)
            return False

        if parent:
            QtWidgets.QApplication.processEvents()

        # СОЗДАЕМ УНИКАЛЬНЫЙ КЛЮЧ ДЛЯ КАЖДОГО УЧЕНИКА
        def add_occurrence_number(df):
            df = df.copy()
            df['occurrence'] = df.groupby('ученик').cumcount() + 1
            df['unique_key'] = df['ученик'] + '_' + df['occurrence'].astype(str)
            return df

        df1_with_key = add_occurrence_number(df1)
        df2_with_key = add_occurrence_number(df2)

        # Переименовываем колонки
        df1_with_key = df1_with_key.rename(columns={'ученик': 'Фамилия', 'оценка': 'Первая оценка'})
        df2_with_key = df2_with_key.rename(columns={'ученик': 'Фамилия', 'оценка': 'Вторая оценка'})

        # Объединяем по уникальному ключу (outer join чтобы сохранить всех учеников)
        result_df = pd.merge(df1_with_key, df2_with_key, on='unique_key', how='outer', suffixes=('_x', '_y'))

        # Создаем финальный DataFrame
        final_df = pd.DataFrame({
            'id': range(1, len(result_df) + 1),
            'Фамилия': result_df['Фамилия_x'].combine_first(result_df['Фамилия_y']),
            'Первая оценка': result_df['Первая оценка'],
            'Вторая оценка': result_df['Вторая оценка']
        })

        # Сортируем по фамилии для красивого отображения
        final_df = final_df.sort_values('Фамилия').reset_index(drop=True)
        final_df['id'] = range(1, len(final_df) + 1)  # Пересчитываем ID после сортировки

        # РАССЧИТЫВАЕМ СТАТИСТИКУ ДЛЯ АНАЛИТИКИ
        stats = calculate_statistics(final_df)

        if parent:
            QtWidgets.QApplication.processEvents()

        # Создание Excel файла
        with pd.ExcelWriter('Tables/Сравнение оценок.xlsx', engine='xlsxwriter') as writer:
            # Лист с оценками учеников
            final_df.to_excel(writer, sheet_name='Оценки учеников', index=False)
            
            workbook = writer.book
            worksheet = writer.sheets['Оценки учеников']

            green = workbook.add_format({'bg_color': '#90EE90'})
            yellow = workbook.add_format({'bg_color': '#FFFFE0'})
            red = workbook.add_format({'bg_color': '#FFB6C1'})
            gray = workbook.add_format({'bg_color': '#D3D3D3'})
            
            for row_num in range(1, len(final_df) + 1):
                first_mark = final_df.iloc[row_num-1]['Первая оценка']
                second_mark = final_df.iloc[row_num-1]['Вторая оценка']
                
                has_both_marks = pd.notna(first_mark) and pd.notna(second_mark)
                has_only_first = pd.notna(first_mark) and pd.isna(second_mark)
                has_only_second = pd.isna(first_mark) and pd.notna(second_mark)
                
                if has_only_first or has_only_second:
                    cell_format = gray
                elif has_both_marks:
                    first_mark = int(first_mark)
                    second_mark = int(second_mark)
                    
                    if first_mark != 2 and second_mark == 2:
                        cell_format = red
                    elif second_mark > first_mark:
                        cell_format = green
                    elif second_mark < first_mark:
                        cell_format = yellow
                    else:
                        cell_format = None
                else:
                    cell_format = None
                
                if cell_format:
                    worksheet.set_row(row_num, cell_format=cell_format)
            
            worksheet.autofilter(0, 0, len(final_df), 3)
            worksheet.set_column('A:A', 7)
            worksheet.set_column('B:B', 13)
            worksheet.set_column('C:C', 18)
            worksheet.set_column('D:D', 18)
            
            # Лист с аналитикой
            # Лист с аналитикой
            analytics_sheet = workbook.add_worksheet('Аналитика')

            # Форматы для аналитики
            header_format = workbook.add_format({
                'bold': True, 
                'font_size': 14,
                'align': 'center',
                'valign': 'vcenter',
                'bg_color': '#366092',
                'font_color': 'white'
            })

            title_format = workbook.add_format({
                'bold': True,
                'font_size': 12,
                'bg_color': '#D9E1F2'
            })

            value_format = workbook.add_format({'font_size': 11})
            percent_format = workbook.add_format({'font_size': 11, 'num_format': '0.00%'})
            change_format_positive = workbook.add_format({'font_size': 11, 'font_color': 'green'})
            change_format_negative = workbook.add_format({'font_size': 11, 'font_color': 'red'})
            change_format_neutral = workbook.add_format({'font_size': 11})

            # ЦВЕТНЫЕ ФОРМАТЫ ДЛЯ ДИНАМИКИ ОЦЕНОК
            improved_format = workbook.add_format({'font_size': 11, 'bg_color': '#90EE90', 'bold': True})  # Зеленый
            worsened_format = workbook.add_format({'font_size': 11, 'bg_color': '#FFFFE0', 'bold': True})  # Желтый
            unchanged_format = workbook.add_format({'font_size': 11, 'bg_color': '#FFFFFF', 'bold': True})  # Белый
            became_two_format = workbook.add_format({'font_size': 11, 'bg_color': '#FFB6C1', 'bold': True})  # Красный

            # Заголовок
            analytics_sheet.merge_range('A1:D1', 'АНАЛИТИКА СРАВНЕНИЯ ОЦЕНОК', header_format)

            # Основная статистика
            row = 3
            analytics_sheet.write(row, 0, 'ОБЩАЯ СТАТИСТИКА', title_format)
            row += 1
            analytics_sheet.write(row, 0, 'Всего учеников:', title_format)
            analytics_sheet.write(row, 1, stats['total_students'], value_format)
            row += 1
            analytics_sheet.write(row, 0, 'Учеников с двумя оценками:', title_format)
            analytics_sheet.write(row, 1, stats['students_with_both_marks'], value_format)
            analytics_sheet.write(row, 2, f"{stats['students_with_both_marks_pct']:.1%}", percent_format)
            row += 1
            analytics_sheet.write(row, 0, 'Учеников только в первом файле:', title_format)
            analytics_sheet.write(row, 1, stats['only_first_file'], value_format)
            row += 1
            analytics_sheet.write(row, 0, 'Учеников только во втором файле:', title_format)
            analytics_sheet.write(row, 1, stats['only_second_file'], value_format)

            row += 2

            # Динамика оценок - С ЦВЕТНЫМ ОФОРМЛЕНИЕМ
            analytics_sheet.write(row, 0, 'ДИНАМИКА ОЦЕНОК', title_format)
            row += 1
            analytics_sheet.write(row, 0, 'Улучшили оценку:', title_format)
            analytics_sheet.write(row, 1, stats['improved'], improved_format)  # Зеленый
            analytics_sheet.write(row, 2, f"{stats['improved_pct']:.1%}", improved_format)  # Зеленый
            row += 1
            analytics_sheet.write(row, 0, 'Ухудшили оценку:', title_format)
            analytics_sheet.write(row, 1, stats['worsened'], worsened_format)  # Желтый
            analytics_sheet.write(row, 2, f"{stats['worsened_pct']:.1%}", worsened_format)  # Желтый
            row += 1
            analytics_sheet.write(row, 0, 'Оценка не изменилась:', title_format)
            analytics_sheet.write(row, 1, stats['unchanged'], unchanged_format)  # Белый
            analytics_sheet.write(row, 2, f"{stats['unchanged_pct']:.1%}", unchanged_format)  # Белый
            row += 1
            analytics_sheet.write(row, 0, 'Появилась оценка 2:', title_format)
            analytics_sheet.write(row, 1, stats['became_two'], became_two_format)  # Красный
            analytics_sheet.write(row, 2, f"{stats['became_two_pct']:.1%}", became_two_format)  # Красный

            row += 2

            # Средние баллы
            analytics_sheet.write(row, 0, 'СРЕДНИЕ БАЛЛЫ', title_format)
            row += 1
            analytics_sheet.write(row, 0, 'Средний балл (первая оценка):', title_format)
            analytics_sheet.write(row, 1, f"{stats['avg_first']:.2f}", value_format)
            row += 1
            analytics_sheet.write(row, 0, 'Средний балл (вторая оценка):', title_format)
            analytics_sheet.write(row, 1, f"{stats['avg_second']:.2f}", value_format)
            row += 1
            analytics_sheet.write(row, 0, 'Изменение среднего балла:', title_format)
            change = stats['avg_change']
            change_format = change_format_positive if change > 0 else change_format_negative if change < 0 else change_format_neutral
            change_sign = "+" if change > 0 else ""
            analytics_sheet.write(row, 1, f"{change_sign}{change:.2f}", change_format)

            row += 1
            analytics_sheet.write(row, 0, 'Количество оценок (первый файл):', title_format)
            analytics_sheet.write(row, 1, stats['total_first_marks'], value_format)
            row += 1
            analytics_sheet.write(row, 0, 'Количество оценок (второй файл):', title_format)
            analytics_sheet.write(row, 1, stats['total_second_marks'], value_format)

            row += 2

            # Распределение оценок
            analytics_sheet.write(row, 0, 'РАСПРЕДЕЛЕНИЕ ОЦЕНОК', title_format)
            row += 1
            for i, (mark, count_first, count_second) in enumerate(stats['mark_distribution']):
                analytics_sheet.write(row + i, 0, f'Оценка {mark}:', title_format)
                analytics_sheet.write(row + i, 1, f"Первая: {count_first}", value_format)
                analytics_sheet.write(row + i, 2, f"Вторая: {count_second}", value_format)

            row += len(stats['mark_distribution']) + 1

            # Самые улучшившиеся и ухудшившиеся
            if stats['most_improved']:
                analytics_sheet.write(row, 0, 'НАИБОЛЬШЕЕ УЛУЧШЕНИЕ', title_format)
                row += 1
                for i, (name, improvement) in enumerate(stats['most_improved']):
                    analytics_sheet.write(row + i, 0, name, value_format)
                    analytics_sheet.write(row + i, 1, f"+{improvement}", improved_format)  # Зеленый

            row += len(stats['most_improved']) + 1 if stats['most_improved'] else 1

            if stats['most_worsened']:
                analytics_sheet.write(row, 0, 'НАИБОЛЬШЕЕ УХУДШЕНИЕ', title_format)
                row += 1
                for i, (name, worsening) in enumerate(stats['most_worsened']):
                    analytics_sheet.write(row + i, 0, name, value_format)
                    analytics_sheet.write(row + i, 1, f"{worsening}", worsened_format)  # Желтый

            # Настройка ширины колонок
            analytics_sheet.set_column('A:A', 40)
            analytics_sheet.set_column('B:B', 15)
            analytics_sheet.set_column('C:C', 15)
            
            # Лист с легендой
            legend_sheet = workbook.add_worksheet('Легенда')
            legend_sheet.write('A2', 'Цвет')
            legend_sheet.write('B2', 'Значение')
            
            legend_data = [
                ('Зеленый', 'Оценка улучшилась'),
                ('Желтый', 'Оценка ухудшилась'),
                ('Красный', 'Оценка стала 2 (была не 2)'),
                ('Серый', 'Ученик есть только в одном файле'),
                ('Белый', 'Оценка не изменилась')
            ]
            
            for i, (color, description) in enumerate(legend_data, 3):
                if color == 'Зеленый':
                    legend_sheet.write(i, 0, color, green)
                elif color == 'Желтый':
                    legend_sheet.write(i, 0, color, yellow)
                elif color == 'Красный':
                    legend_sheet.write(i, 0, color, red)
                elif color == 'Серый':
                    legend_sheet.write(i, 0, color, gray)
                else:
                    legend_sheet.write(i, 0, color)
                legend_sheet.write(i, 1, description)
            
            legend_sheet.set_column('A:A', 15)
            legend_sheet.set_column('B:B', 30)

        return True
        
    except Exception as e:
        show_error_message(f"Неожиданная ошибка при создании файла: {str(e)}", parent)
        return False


def calculate_statistics(final_df):
    """Рассчитывает статистику для аналитики"""
    stats = {}
    
    # Общая статистика
    stats['total_students'] = len(final_df)
    
    # Ученики с обеими оценками
    students_with_both = final_df.dropna(subset=['Первая оценка', 'Вторая оценка'])
    stats['students_with_both_marks'] = len(students_with_both)
    stats['students_with_both_marks_pct'] = len(students_with_both) / len(final_df) if len(final_df) > 0 else 0
    
    # Ученики только в одном файле
    stats['only_first_file'] = len(final_df[final_df['Вторая оценка'].isna()])
    stats['only_second_file'] = len(final_df[final_df['Первая оценка'].isna()])
    
    # Динамика оценок (только для учеников с обеими оценками)
    improved = 0
    worsened = 0
    unchanged = 0
    became_two = 0
    
    most_improved = []
    most_worsened = []
    
    for _, row in students_with_both.iterrows():
        first = int(row['Первая оценка'])
        second = int(row['Вторая оценка'])
        change = second - first
        
        if first != 2 and second == 2:
            became_two += 1
        elif second > first:
            improved += 1
            most_improved.append((row['Фамилия'], change))
        elif second < first:
            worsened += 1
            most_worsened.append((row['Фамилия'], change))
        else:
            unchanged += 1
    
    total_with_both = len(students_with_both)
    
    stats['improved'] = improved
    stats['improved_pct'] = improved / total_with_both if total_with_both > 0 else 0
    stats['worsened'] = worsened
    stats['worsened_pct'] = worsened / total_with_both if total_with_both > 0 else 0
    stats['unchanged'] = unchanged
    stats['unchanged_pct'] = unchanged / total_with_both if total_with_both > 0 else 0
    stats['became_two'] = became_two
    stats['became_two_pct'] = became_two / total_with_both if total_with_both > 0 else 0
    
    # Топ улучшившихся и ухудшившихся
    stats['most_improved'] = sorted(most_improved, key=lambda x: x[1], reverse=True)[:5]
    stats['most_worsened'] = sorted(most_worsened, key=lambda x: x[1])[:5]
    
    # СРЕДНИЕ БАЛЛЫ - СЧИТАЕМ ПО ВСЕМ ИМЕЮЩИМСЯ ОЦЕНКАМ
    first_marks = final_df['Первая оценка'].dropna()
    second_marks = final_df['Вторая оценка'].dropna()
    
    stats['avg_first'] = first_marks.mean() if not first_marks.empty else 0
    stats['avg_second'] = second_marks.mean() if not second_marks.empty else 0
    stats['avg_change'] = stats['avg_second'] - stats['avg_first']
    
    # РАСПРЕДЕЛЕНИЕ ОЦЕНОК - СЧИТАЕМ ПО ВСЕМ ИМЕЮЩИМСЯ ОЦЕНКАМ
    mark_distribution = []
    for mark in [2, 3, 4, 5]:
        # Считаем для первого файла
        count_first = len(first_marks[first_marks == mark])
        # Считаем для второго файла
        count_second = len(second_marks[second_marks == mark])
        mark_distribution.append((mark, count_first, count_second))
    
    stats['mark_distribution'] = mark_distribution
    
    # Дополнительная статистика по файлам
    stats['total_first_marks'] = len(first_marks)
    stats['total_second_marks'] = len(second_marks)
    
    return stats