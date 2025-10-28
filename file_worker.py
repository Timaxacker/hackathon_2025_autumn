import pandas as pd


def create_file():
    df1 = pd.read_excel('Tables/file1.xlsx')
    df2 = pd.read_excel('Tables/file2.xlsx')

    df1 = df1.sort_values('ученик').reset_index(drop=True)
    df2 = df2.sort_values('ученик').reset_index(drop=True)

    df1['id'] = range(1, len(df1) + 1)
    df2['id'] = range(1, len(df2) + 1)

    df1 = df1.rename(columns={'ученик': 'Фамилия', 'оценка': 'Первая оценка'})
    df2 = df2.rename(columns={'ученик': 'Фамилия', 'оценка': 'Вторая оценка'})

    result_df = pd.merge(df1, df2, on='id', how='outer')


    mismatch_surname = result_df['Фамилия_x'] != result_df['Фамилия_y']
    if mismatch_surname.any():
        print("Обнаружены расхождения в фамилиях для следующих ID:")
        mismatches = result_df[mismatch_surname][['id', 'Фамилия_x', 'Фамилия_y']]
        print(mismatches)
        print(f"Всего расхождений: {mismatch_surname.sum()}")

    #else:
        #print("Расхождений в фамилиях не обнаружено")


    final_df = pd.DataFrame({
        'id': result_df['id'],
        'Фамилия': result_df['Фамилия_x'],
        'Первая оценка': result_df['Первая оценка'],
        'Вторая оценка': result_df['Вторая оценка']
    })


    final_df['Первая оценка'] = final_df['Первая оценка'].astype(int)
    final_df['Вторая оценка'] = final_df['Вторая оценка'].astype(int)


    final_df = final_df.sort_values('Фамилия').reset_index(drop=True)



    with pd.ExcelWriter('Tables/Сравнение оценок.xlsx', engine='xlsxwriter') as writer:
        final_df.to_excel(writer, sheet_name='Оценки учеников', index=False)
        
        workbook = writer.book
        worksheet = writer.sheets['Оценки учеников']


        green = workbook.add_format({'bg_color': '#90EE90'})
        yellow = workbook.add_format({'bg_color': '#FFFFE0'})
        red = workbook.add_format({'bg_color': '#FFB6C1'})
        

        for row_num in range(1, len(final_df) + 1):
            first_mark = final_df.iloc[row_num-1]['Первая оценка']
            second_mark = final_df.iloc[row_num-1]['Вторая оценка']
            
            if first_mark != 2 and second_mark == 2:
                cell_format = red

            elif second_mark > first_mark:
                cell_format = green

            elif second_mark < first_mark:
                cell_format = yellow

            else:
                cell_format = None
            
            if cell_format:
                worksheet.set_row(row_num, cell_format=cell_format)
        

        worksheet.autofilter(0, 0, len(final_df), 3)
        

        worksheet.set_column('A:A', 7)
        worksheet.set_column('B:B', 13)
        worksheet.set_column('C:C', 18)
        worksheet.set_column('D:D', 18)
        


        legend_sheet = workbook.add_worksheet('Легенда')
        
        legend_sheet.write('A2', 'Цвет')
        legend_sheet.write('B2', 'Значение')
        
        legend_data = [
            ('Зеленый', 'Оценка улучшилась'),
            ('Желтый', 'Оценка ухудшилась'),
            ('Красный', 'Оценка стала 2 (была не 2)'),
            ('Белый', 'Оценка не изменилась')
        ]
        

        for i, (color, description) in enumerate(legend_data, 3):
            if color == 'Зеленый':
                legend_sheet.write(i, 0, color, green)
            elif color == 'Желтый':
                legend_sheet.write(i, 0, color, yellow)
            elif color == 'Красный':
                legend_sheet.write(i, 0, color, red)
            else:
                legend_sheet.write(i, 0, color)
            legend_sheet.write(i, 1, description)
        

        legend_sheet.set_column('A:A', 15)
        legend_sheet.set_column('B:B', 30)



    print("\nФайл успешно создан: Сравнение оценок.xlsx")