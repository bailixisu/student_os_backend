import datetime
import time

from sqlalchemy.orm import Session

import models
import schemas


# 添加学生
def create_student(db: Session, student: schemas.Student):
    print(student)
    print(models.Student(**student.dict()))
    db_student = models.Student(**student.dict())
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student


# 添加健康日报
def create_health_report(db: Session, health_report: schemas.HealthReport):
    db_health_report = models.HealthReport(**health_report.dict())
    db.add(db_health_report)
    db.commit()
    db.refresh(db_health_report)
    return


# 添加院系
def create_department(db: Session, department: schemas.Department):
    db_department = models.Department(**department.dict())
    db.add(db_department)
    db.commit()
    db.refresh(db_department)
    return db_department


# 添加院系管理员
def create_department_admin(db: Session, department_admin: schemas.DepartmentAdmin):
    db_department_admin = models.DepartmentAdmin(**department_admin.dict())
    db.add(db_department_admin)
    db.commit()
    db.refresh(db_department_admin)
    return db_department_admin


# 添加班级
def create_class(db: Session, class_: schemas.Class):
    db_class = models.Class(**class_.dict())
    db.add(db_class)
    db.commit()
    db.refresh(db_class)
    return db_class


# 添加辅导员
def create_counselor(db: Session, counselor: schemas.Counselor):
    db_counselor = models.Counselor(**counselor.dict())
    db.add(db_counselor)
    db.commit()
    db.refresh(db_counselor)
    return db_counselor


# 添加校区
def create_campus(db: Session, campus: schemas.Campus):
    db_campus = models.Campus(**campus.dict())
    db.add(db_campus)
    db.commit()
    db.refresh(db_campus)
    return db_campus


# 添加学生校区连接表
def create_student_campus(db: Session, student_campus: schemas.StudentCampus):
    db_student_campus = models.StudentCampus(**student_campus.dict())
    db.add(db_student_campus)
    db.commit()
    db.refresh(db_student_campus)
    return db_student_campus


# 添加进出校园
def create_in_out_campus(db: Session, in_out_campus: schemas.InOutCampus):
    db_in_out_campus = models.InOutCampus(**in_out_campus.dict())
    db.add(db_in_out_campus)
    db.commit()
    db.refresh(db_in_out_campus)
    return db_in_out_campus


# 获取所有学生的学号和姓名
def get_all_student_health_report_of_n_days(days: int, db: Session):
    data = []
    n_days_ago = datetime.datetime.now() - datetime.timedelta(days=days)
    for stu_number, stu_name in db.query(models.Student.stu_number, models.Student.stu_name).all():
        health_report_of_n_days = schemas.StudentHealthReport(stu_number=stu_number, stu_name=stu_name, infoList=[])
        health_report_of_n_days.infoList = db.query(models.HealthReport.date, models.HealthReport.temperature,
                                                    models.HealthReport.location, models.HealthReport.report_time,
                                                    models.HealthReport.other_message) \
            .filter(models.HealthReport.stu_number == stu_number).order_by(models.HealthReport.date.desc()).all()
        health_report_of_n_days.infoList = list(filter(lambda x: x.report_time.timestamp() > n_days_ago.timestamp(),
                                                       health_report_of_n_days.infoList))
        #将datetime转换为str
        new_info_list = []
        for info in health_report_of_n_days.infoList:
            new_info = schemas.HealthReportInfo(date=info.date.strftime('%Y-%m-%d'), temperature=info.temperature,
                                            location=info.location, report_time=info.report_time.strftime('%Y-%m-%d %H:%M:%S'),
                                            other_message=info.other_message)
            new_info_list.append(new_info)
        health_report_of_n_days.infoList = new_info_list
        data.append(health_report_of_n_days)
    return data


# 获取所有学生的入校权限
def get_all_student_right_of_campus(db: Session):
    data = []
    for student in db.query(models.Student).all():
        right_of_campus = schemas.StudentRightOfCampus(stu_number=student.stu_number, stu_name=student.stu_name, access='')
        print(student.campus)
        for i in range(len(student.campus)):
            if i == len(student.campus) - 1:
                right_of_campus.access += student.campus[i].campus_name
            else:
                right_of_campus.access += student.campus[i].campus_name + ', '
        data.append(right_of_campus)
    return data
