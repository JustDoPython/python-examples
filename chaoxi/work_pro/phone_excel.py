#coding:utf-8
import xlwt

#读取目标文本文件
def get_str(path):
    f = open(path, encoding="utf-8")
    data = f.read()
    f.close()
    return data


def save_excel(save_path,sheetname,column_name_list,read_list):
    workbook = xlwt.Workbook()

    sheet1 = workbook.add_sheet(sheetname=sheetname)

    for i in range(0,len(column_name_list)):
        sheet1.write(0,i,column_name_list[i])
        i = 1
        for v in read_list:
            kval = v.split('：')
            for j in range(0, len(kval)):
                sheet1.write(i + 1, j, kval[j])
                print(kval[j])
            i = i + 1
#保存为Excel文件
def save_excel(save_path,sheetname,column_name_list,read_list):
    workbook = xlwt.Workbook()
    sheet1 = workbook.add_sheet(sheetname=sheetname)
    for i in range(0,len(column_name_list)):
        sheet1.write(0,i,column_name_list[i])
    i=1
    for v in read_list:
        kval=v.split('：')
        for j in range(0,len(kval)):
            sheet1.write(i+1,j,kval[j])
        i=i+1
    workbook.save(save_path)
    print('信息保存 OK，记录条数共计：'+str(len(read_list)))

if __name__ == '__main__':
    path = input("请输入文件路径：")
    save_path = input("请输入文件保存路径：")
    sheet_name = input("请输入sheetname：")
    column_name = input("请输入列名，并且使用英文逗号隔开：")
    column_name_list = column_name.split(',')

    read_str = get_str(path)
    read_list = read_str.split('\n')
    save_excel(save_path, sheet_name, column_name_list, read_list)