import csv
import pymysql
# Connect to the database
config = {
    'host': 'localhost',
    'user':'root',
    'password':'1234',
    'db':'test',
    'charset':'utf8mb4',
    'local_infile':1,
}
connection = pymysql.connect(**config)
cur = connection.cursor()

list_of_tables = ["department","class","department_admin","counselor","student","campus","apply_for_leave_school","apply_for_enter_school","health_report","in_out_campus","student_campus"]

for table in list_of_tables:
    with open('.\\data\\'+table+'.csv', 'r', encoding='utf-8') as f:
        file = table
        reader = csv.reader(f)
        list = [row for row in reader]
        test = 'INSERT INTO ' + file + ' ('
        test += ', '.join(list[0])
        for i in range(1, len(list)):
            sql = test + ') VALUES (\'' + '\', \''.join(list[i]) + '\');'
            cur.execute(sql)
        connection.commit()

