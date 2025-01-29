import openpyxl

def readExcel(file_path: object = 'data_excel.xlsx', sheet_name: object = 'Sheet1') -> object:
    wb = openpyxl.load_workbook(file_path)
    sh = wb[sheet_name]
    rowsData = list(sh.rows)
    row_data = []
    for item in rowsData[1:]:
        data = [i.value for i in item]
        row_data.append(data)
    return row_data

def writeExcel(data, file_path='output_excel.xlsx', sheet_name='Sheet1'):
    wb = openpyxl.Workbook()
    sh = wb.active
    sh.title = sheet_name

    # 写入标题行
    headers = ['Column1', 'Column2', 'Column3']  # 根据实际情况修改标题
    sh.append(headers)

    # 写入数据行
    for row in data:
        sh.append(row)

    wb.save(file_path)

if __name__ == '__main__':
    # 读取Excel数据
    data = readExcel()
    print("Read Data:", data)

    # 写入Excel数据
    write_data = [
        ['Data1', 'Data2', 'Data3'],
        ['Data4', 'Data5', 'Data6']
    ]
    writeExcel(write_data)
