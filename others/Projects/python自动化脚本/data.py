#使用excel管理数据
import xlrd  #第三方库   用来读取excel表格
def readExcel(sheet,startRow,endRow):
    a=xlrd.open_workbook('data .xls')  #打开文件  括号路径
    b=a.sheet_by_name(sheet)           #读取sheet表
    #row =b.nrows                    #获取表行数
    cols=b.ncols                     #获取列数
    #print(row,cols)
    lst=[]                          #读取表中数据添加到列表中作为用例参数化的数据
    for i in range(startRow,endRow):
        if cols>1:
            lst1 = []
            for j in range(cols):
                c=b.cell_value(i,j)   #读取单元格

                if type(c)==float:
                    c=int(c)
                lst1.append(c)

            lst.append(lst1)
        elif cols==1:
            c=b.cell_value(i,0)
            if type(c) == float:
                c = int(c)
            lst.append(c)
    return  lst

#print(readExcel("login",0,3))