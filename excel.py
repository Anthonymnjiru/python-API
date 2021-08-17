import xlsxwriter
workbook=xlsxwriter.workbook('transactions.xlsx')
worksheet=workbook.add_worksheet()
transactions =(
    {'rent',200},
    {'Gas', 500},
)
row=0
col=0
for item, cost in(transactions);
worksheet.write(row,col, item)
worksheet.write(row,col+1, cost)
row +=1
worksheet.write(row,0, 'total')
worksheet.write(row, 1, '=SUM(B1:B4')
workbook.close()
