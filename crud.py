import datetime
import time

from sqlalchemy import func
from sqlalchemy.orm import Session

import models
import schemas
from sqlalchemy.sql import distinct


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


# 添加入校申请
def create_in_campus_application(db: Session, in_campus_application: schemas.ApplyForEnterSchoolSchema):
    db_in_campus_application = models.ApplyForEnterSchool(**in_campus_application.dict())
    db.add(db_in_campus_application)
    db.commit()
    db.refresh(db_in_campus_application)
    return db_in_campus_application


# 添加出校申请
def create_out_campus_application(db: Session, out_campus_application: schemas.ApplyForLeaveSchoolSchema):
    db_out_campus_application = models.ApplyForLeaveSchool(**out_campus_application.dict())
    db.add(db_out_campus_application)
    db.commit()
    db.refresh(db_out_campus_application)
    return db_out_campus_application


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
        # 将datetime转换为str
        new_info_list = []
        for info in health_report_of_n_days.infoList:
            new_info = schemas.HealthReportInfo(date=info.date.strftime('%Y-%m-%d'), temperature=info.temperature,
                                                location=info.location,
                                                report_time=info.report_time.strftime('%Y-%m-%d %H:%M:%S'),
                                                other_message=info.other_message)
            new_info_list.append(new_info)
        health_report_of_n_days.infoList = new_info_list
        data.append(health_report_of_n_days)
    return data


# 获取所有学生的入校权限
def get_all_student_right_of_campus(db: Session):
    data = []
    for student in db.query(models.Student).all():
        right_of_campus = schemas.StudentRightOfCampus(stu_number=student.stu_number, stu_name=student.stu_name,
                                                       access='')
        for i in range(len(student.campus)):
            if i == len(student.campus) - 1:
                right_of_campus.access += student.campus[i].campus_name
            else:
                right_of_campus.access += student.campus[i].campus_name + ', '
        data.append(right_of_campus)
    return data


def get_all_student_leave_school(db: Session):
    data = []
    for leave_school in db.query(models.ApplyForLeaveSchool).all():
        if leave_school.handle_time is None:
            handle_time = ''
        else:
            handle_time = leave_school.handle_time.strftime('%Y-%m-%d %H:%M:%S')
        leave_school_info = schemas.ApplyForLeaveSchool(pipeline_id=leave_school.pipeline_id, handlers='',
                                                        handle_time=handle_time, suggestion=leave_school.suggestion,
                                                        final_suggestion=leave_school.final_suggestion,
                                                        status=leave_school.status, stu_number=leave_school.stu_number,
                                                        stu_name='', leave_reason=leave_school.leave_reason,
                                                        destination=leave_school.destination,
                                                        departure_date=leave_school.departure_date.strftime(
                                                            '%Y-%m-%d %H:%M:%S'),
                                                        estimated_return_time=leave_school.estimated_return_time.strftime(
                                                            '%Y-%m-%d %H:%M:%S'),
                                                        handle_reason=leave_school.handle_reason)
        leave_school_info.stu_name = \
            db.query(models.Student.stu_name).filter(models.Student.stu_number == leave_school.stu_number).first()[0]
        if leave_school.level == "辅导员":
            leave_school_info.handlers = \
                db.query(models.Counselor.teacher_name).filter(models.Counselor.id == leave_school.handlers_id).first()[
                    0]
        elif leave_school.level == "院系管理员":
            leave_school_info.handlers = db.query(models.DepartmentAdmin.teacher_name).filter(
                models.DepartmentAdmin.id == leave_school.handlers_id).first()[0]
        data.append(leave_school_info)
    return data


def get_all_student_enter_school(db: Session):
    data = []
    for enter_school in db.query(models.ApplyForEnterSchool).all():
        if enter_school.handle_time is None:
            handle_time = ''
        else:
            handle_time = enter_school.handle_time.strftime('%Y-%m-%d %H:%M:%S')
        enter_school_info = schemas.ApplyForEnterSchool(pipeline_id=enter_school.pipeline_id, handlers='',
                                                        handle_time=handle_time, suggestion=enter_school.suggestion,
                                                        final_suggestion=enter_school.final_suggestion,
                                                        status=enter_school.status, stu_number=enter_school.stu_number,
                                                        stu_name='',
                                                        return_school_reason=enter_school.return_school_reason,
                                                        handle_reason=enter_school.handle_reason,
                                                        location_of_seven_days=enter_school.location_of_seven_days,
                                                        estimated_return_school_time=enter_school.estimated_return_school_time.strftime(
                                                            '%Y-%m-%d %H:%M:%S'))
        enter_school_info.stu_name = \
            db.query(models.Student.stu_name).filter(models.Student.stu_number == enter_school.stu_number).first()[0]
        if enter_school.level == "辅导员":
            enter_school_info.handlers = \
                db.query(models.Counselor.teacher_name).filter(models.Counselor.id == enter_school.handlers_id).first()[
                    0]
        elif enter_school.level == "院系管理员":
            enter_school_info.handlers = db.query(models.DepartmentAdmin.teacher_name).filter(
                models.DepartmentAdmin.id == enter_school.handlers_id).first()[0]
        data.append(enter_school_info)
    return data


def get_all_student_leave_school_time(db: Session):
    data = []
    if is_leap_year(datetime.datetime.now().year - 1):
        days = 366
    else:
        days = 365
    year_ago = datetime.datetime.now() - datetime.timedelta(days=days)
    for student in db.query(models.Student).all():
        leave_school_time = schemas.StudentLeaveSchoolTimeOfYear(stu_number=student.stu_number,
                                                                 stu_name=student.stu_name, leave_time='')
        delta = 0
        in_out_infos = db.query(models.InOutCampus).filter(models.InOutCampus.stu_number == student.stu_number). \
            filter(models.InOutCampus.date > year_ago).order_by(models.InOutCampus.date.asc()).all()
        for i in range(len(in_out_infos)):
            if in_out_infos[i].status == '进校':
                if i == 0:
                    delta += in_out_infos[i].date.timestamp() - year_ago.timestamp()
                else:
                    delta += in_out_infos[i].date.timestamp() - in_out_infos[i - 1].date.timestamp()
            else:
                if i == len(in_out_infos) - 1:
                    delta += datetime.datetime.now().timestamp() - in_out_infos[i].date.timestamp()
        leave_school_time.leave_time = str(datetime.timedelta(seconds=int(delta)))
        data.append(leave_school_time)
    return data


# 判断是不是闰年
def is_leap_year(year):
    if (year % 4 == 0 and year % 100 != 0) or year % 400 == 0:
        return True
    else:
        return False


def get_all_student_leave_school_no_pass(days: int, db: Session):
    n_days_ago = datetime.datetime.now() - datetime.timedelta(days=days)
    data = schemas.StudentLeaveSchoolNoPassOfNDays(total=0, list=[])
    for leave_school in db.query(models.ApplyForLeaveSchool).filter(models.ApplyForLeaveSchool.status == '待审核'). \
            filter(models.ApplyForLeaveSchool.submit_time > n_days_ago).all():
        if leave_school.handle_time is None:
            handle_time = ''
        else:
            handle_time = leave_school.handle_time.strftime('%Y-%m-%d %H:%M:%S')
        leave_school_info = schemas.ApplyForLeaveSchool(pipeline_id=leave_school.pipeline_id, handlers='',
                                                        handle_time=handle_time, suggestion=leave_school.suggestion,
                                                        final_suggestion=leave_school.final_suggestion,
                                                        status=leave_school.status, stu_number=leave_school.stu_number,
                                                        stu_name='', leave_reason=leave_school.leave_reason,
                                                        destination=leave_school.destination,
                                                        departure_date=leave_school.departure_date.strftime(
                                                            '%Y-%m-%d %H:%M:%S'),
                                                        estimated_return_time=leave_school.estimated_return_time.strftime(
                                                            '%Y-%m-%d %H:%M:%S'),
                                                        handle_reason=leave_school.handle_reason)

        leave_school_info.stu_name = \
            db.query(models.Student.stu_name).filter(models.Student.stu_number == leave_school.stu_number).first()[0]
        if leave_school.level == "辅导员":
            leave_school_info.handlers = \
                db.query(models.Counselor.teacher_name).filter(models.Counselor.id == leave_school.handlers_id).first()[
                    0]
        elif leave_school.level == "院系管理员":
            leave_school_info.handlers = db.query(models.DepartmentAdmin.teacher_name).filter(
                models.DepartmentAdmin.id == leave_school.handlers_id).first()[0]
        data.list.append(leave_school_info)
        data.total += 1
    return data


def get_all_student_enter_school_no_pass(days: int, db: Session):
    n_days_ago = datetime.datetime.now() - datetime.timedelta(days=days)
    data = schemas.StudentEnterSchoolNoPassOfNDays(total=0, list=[])
    for enter_school in db.query(models.ApplyForEnterSchool).filter(models.ApplyForEnterSchool.status == '待审核'). \
            filter(models.ApplyForEnterSchool.submit_time > n_days_ago).all():
        if enter_school.handle_time is None:
            handle_time = ''
        else:
            handle_time = enter_school.handle_time.strftime('%Y-%m-%d %H:%M:%S')
        enter_school_info = schemas.ApplyForEnterSchool(pipeline_id=enter_school.pipeline_id, handlers='',
                                                        handle_time=handle_time, suggestion=enter_school.suggestion,
                                                        final_suggestion=enter_school.final_suggestion,
                                                        status=enter_school.status, stu_number=enter_school.stu_number,
                                                        stu_name='',
                                                        return_school_reason=enter_school.return_school_reason,
                                                        handle_reason=enter_school.handle_reason,
                                                        location_of_seven_days=enter_school.location_of_seven_days,
                                                        estimated_return_school_time=enter_school.estimated_return_school_time.strftime(
                                                            '%Y-%m-%d %H:%M:%S'))
        enter_school_info.stu_name = \
            db.query(models.Student.stu_name).filter(models.Student.stu_number == enter_school.stu_number).first()[0]
        if enter_school.level == "辅导员":
            enter_school_info.handlers = \
                db.query(models.Counselor.teacher_name).filter(models.Counselor.id == enter_school.handlers_id).first()[
                    0]
        elif enter_school.level == "院系管理员":
            enter_school_info.handlers = db.query(models.DepartmentAdmin.teacher_name).filter(
                models.DepartmentAdmin.id == enter_school.handlers_id).first()[0]
        data.list.append(enter_school_info)
        data.total += 1
    return data


def get_apply_for_enter_count(stu_number: int, db: Session):
    # 计算不同的pipeline_id的数量
    return db.query(distinct(models.ApplyForEnterSchool.pipeline_id)).filter(
        models.ApplyForEnterSchool.stu_number == stu_number).count()


def get_all_student_apply_for_enter_count_in_school(num: int, db: Session):
    data = []
    for student in db.query(models.Student).all():
        student.apply_for_enter_count = get_apply_for_enter_count(student.stu_number, db)
        data.append(schemas.StudentApplyCount(stu_number=student.stu_number, stu_name=student.stu_name,
                                              total=student.apply_for_enter_count))
        data.sort(key=lambda x: x.total, reverse=True)
    if len(data) > num:
        return data[:num]
    else:
        return data


def get_all_student_apply_for_enter_count_in_department(department: str, num: int, db: Session):
    data = []
    for student in db.query(models.Student).filter(models.Student.class_id.in_(db.query(models.Class.id).filter(
            models.Class.department_id == db.query(models.Department.id).filter(
                models.Department.department_name == department).first()[0]))).all():
        student.apply_for_enter_count = get_apply_for_enter_count(student.stu_number, db)
        data.append(schemas.StudentApplyCount(stu_number=student.stu_number, stu_name=student.stu_name,
                                              total=student.apply_for_enter_count))
        data.sort(key=lambda x: x.total, reverse=True)
    if len(data) > num:
        return data[:num]
    else:
        return data


def get_all_student_apply_for_enter_count_in_class(id: int, num: int, db: Session):
    data = []
    for student in db.query(models.Student).filter(models.Student.class_id == id).all():
        student.apply_for_enter_count = get_apply_for_enter_count(student.stu_number, db)
        data.append(schemas.StudentApplyCount(stu_number=student.stu_number, stu_name=student.stu_name,
                                              total=student.apply_for_enter_count))
        data.sort(key=lambda x: x.total, reverse=True)
    if len(data) > num:
        return data[:num]
    else:
        return data


def get_student_average_leave_time(stu_number: int, db: Session):
    delta = 0
    count = 0
    in_out_infos = db.query(models.InOutCampus).filter(models.InOutCampus.stu_number == stu_number) \
        .order_by(models.InOutCampus.date.asc()).all()
    for i in range(len(in_out_infos)):
        if in_out_infos[i].status == '进校':
            if i == 0:
                continue
            else:
                delta += in_out_infos[i].date.timestamp() - in_out_infos[i - 1].date.timestamp()
                count += 1
        else:
            if i == len(in_out_infos) - 1:
                delta += datetime.datetime.now().timestamp() - in_out_infos[i].date.timestamp()
                count += 1
    if count == 0:
        return 0
    return delta / count


def get_all_student_average_leave_time_in_school(num: int, db: Session):
    data = []
    for student in db.query(models.Student).all():
        avg_leave_time = datetime.timedelta(seconds=get_student_average_leave_time(student.stu_number, db))
        data.append(schemas.StudentLeaveSchoolTimeAvg(stu_number=student.stu_number, stu_name=student.stu_name,
                                                      average_leave_time=str(avg_leave_time)))
        data.sort(key=lambda x: x.average_leave_time, reverse=True)
    if len(data) > num:
        return data[:num]
    else:
        return data


def get_all_student_average_leave_time_in_department(department: str, num: int, db: Session):
    data = []
    for student in db.query(models.Student).filter(models.Student.class_id.in_(db.query(models.Class.id).filter(
            models.Class.department_id == db.query(models.Department.id).filter(
                models.Department.department_name == department).first()[0]))).all():
        avg_leave_time = datetime.timedelta(seconds=get_student_average_leave_time(student.stu_number, db))
        data.append(schemas.StudentLeaveSchoolTimeAvg(stu_number=student.stu_number, stu_name=student.stu_name,
                                                      average_leave_time=str(avg_leave_time)))
        data.sort(key=lambda x: x.average_leave_time, reverse=True)
    if len(data) > num:
        return data[:num]
    else:
        return data


def get_all_student_average_leave_time_in_class(id: int, num: int, db: Session):
    data = []
    for student in db.query(models.Student).filter(models.Student.class_id == id).all():
        avg_leave_time = datetime.timedelta(seconds=get_student_average_leave_time(student.stu_number, db))
        data.append(schemas.StudentLeaveSchoolTimeAvg(stu_number=student.stu_number, stu_name=student.stu_name,
                                                      average_leave_time=str(avg_leave_time)))
        data.sort(key=lambda x: x.average_leave_time, reverse=True)
    if len(data) > num:
        return data[:num]
    else:
        return data


# 获取离校学生信息
def get_all_student_leave_school_info(db: Session):
    list = []
    for student in db.query(models.Student).all():
        last_in_out_info = db.query(models.InOutCampus).filter(models.InOutCampus.stu_number == student.stu_number) \
            .order_by(models.InOutCampus.date.desc()).first()
        if last_in_out_info is not None and last_in_out_info.status == '离校':
            list.append(schemas.StudentLeaveSchoolInfo(stu_number=student.stu_number, stu_name=student.stu_name,
                                                       phone_number=student.phone_number, email=student.email,
                                                       address=student.address, family_address=student.family_address,
                                                       id_card_number=student.id_card_number,
                                                       id_card_type=student.id_card_type,
                                                       departure_time=last_in_out_info.date.strftime(
                                                           '%Y-%m-%d %H:%M:%S')))
    return schemas.AllStudentLeaveSchoolInfo(list=list, total=len(list))


# 获取离校超过一天的学生信息
def get_all_student_leave_school_more_than_one_day_info(db: Session):
    list = []
    for student in db.query(models.Student).all():
        last_in_out_info = db.query(models.InOutCampus).filter(models.InOutCampus.stu_number == student.stu_number) \
            .order_by(models.InOutCampus.date.desc()).first()
        if last_in_out_info is not None and last_in_out_info.status == '离校':
            if datetime.datetime.now().timestamp() - last_in_out_info.date.timestamp() > 24 * 60 * 60:
                infos = db.query(models.ApplyForLeaveSchool)\
                    .filter(student.stu_number == models.ApplyForLeaveSchool.stu_number,
                                                            models.ApplyForLeaveSchool.out_date_flag == 0).all()
                applys = set()
                for info in infos:
                    applys.add(info.pipeline_id)
                flag = False
                for apply in applys:
                    if db.query(models.ApplyForLeaveSchool).filter(models.ApplyForLeaveSchool.pipeline_id == apply,
                                                                  models.ApplyForLeaveSchool.status== '已拒绝').first() is  None:
                        flag = True
                        break
                if flag:
                    continue
                list.append(schemas.StudentInfo(stu_number=student.stu_number, stu_name=student.stu_name,
                                                phone_number=student.phone_number, email=student.email,
                                                address=student.address, family_address=student.family_address,
                                                id_card_number=student.id_card_number,
                                                id_card_type=student.id_card_type))
    return schemas.AllStudentInfo(list=list, total=len(list))


# 提交申请但未离校的学生信息
def get_all_student_apply_for_leave_school_but_not_leave_school_info(db: Session):
    list = []
    for student in db.query(models.Student).all():
        last_in_out_info = db.query(models.InOutCampus).filter(models.InOutCampus.stu_number == student.stu_number) \
            .order_by(models.InOutCampus.date.desc()).first()
        if last_in_out_info is not None and last_in_out_info.status == '进校':
            infos = db.query(models.ApplyForLeaveSchool) \
                .filter(student.stu_number == models.ApplyForLeaveSchool.stu_number,
                        models.ApplyForLeaveSchool.out_date_flag == 0).all()
            applys = set()
            for info in infos:
                applys.add(info.pipeline_id)
            for apply in applys:
                if db.query(models.ApplyForLeaveSchool).filter(models.ApplyForLeaveSchool.pipeline_id == apply,
                                                              models.ApplyForLeaveSchool.status == '已拒绝').first() is None:
                    list.append(schemas.StudentInfo(stu_number=student.stu_number, stu_name=student.stu_name,
                                                    phone_number=student.phone_number, email=student.email,
                                                    address=student.address, family_address=student.family_address,
                                                    id_card_number=student.id_card_number,
                                                    id_card_type=student.id_card_type))
                    break

    return schemas.AllStudentInfo(list=list, total=len(list))



# 过去n天的一直在校的学生
def get_all_student_stay_in_school_more_than_n_days_info_in_school_level(days: int,db: Session):
    list = []
    for student in db.query(models.Student).all():
        last_in_out_info = db.query(models.InOutCampus).filter(models.InOutCampus.stu_number == student.stu_number) \
            .order_by(models.InOutCampus.date.desc()).first()
        if last_in_out_info is not None and last_in_out_info.status == '进校':
            if datetime.datetime.now().timestamp() - last_in_out_info.date.timestamp() > days * 24 * 60 * 60:
                list.append(schemas.StudentNumAndName(stu_number=student.stu_number, stu_name=student.stu_name))
    return list


# 过去n天的一直在校的学生(按照学院)
def get_all_student_stay_in_school_more_than_n_days_info_in_department_level(department_name:str,days: int,db: Session):
    list = []
    for student in db.query(models.Student).\
            filter(models.Student.class_id.in_(db.query(models.Class.id).filter(models.Class.department_id.in_(db.query(models.Department.id).filter(models.Department.department_name == department_name))))).all():
        last_in_out_info = db.query(models.InOutCampus).filter(models.InOutCampus.stu_number == student.stu_number) \
            .order_by(models.InOutCampus.date.desc()).first()
        if last_in_out_info is not None and last_in_out_info.status == '进校':
            if datetime.datetime.now().timestamp() - last_in_out_info.date.timestamp() > days * 24 * 60 * 60:
                list.append(schemas.StudentNumAndName(stu_number=student.stu_number, stu_name=student.stu_name))
    return list



# 过去n天的一直在校的学生(按照班级)
def get_all_student_stay_in_school_more_than_n_days_info_in_class_level(id:int,days: int,db: Session):
    list = []
    for student in db.query(models.Student).filter(models.Student.class_id == id).all():
        last_in_out_info = db.query(models.InOutCampus).filter(models.InOutCampus.stu_number == student.stu_number) \
            .order_by(models.InOutCampus.date.desc()).first()
        if last_in_out_info is not None and last_in_out_info.status == '进校':
            if datetime.datetime.now().timestamp() - last_in_out_info.date.timestamp() > days * 24 * 60 * 60:
                list.append(schemas.StudentNumAndName(stu_number=student.stu_number, stu_name=student.stu_name))
    return list


# 连续n天健康日报相同
def get_all_student_health_report_same_for_n_days_info_in_school_level(days: int,db: Session):
    list = []
    for student in db.query(models.Student).all():
        last_health_reports = db.query(models.HealthReport).filter(models.HealthReport.stu_number == student.stu_number) \
            .order_by(models.HealthReport.date.desc()).all()
        if len(last_health_reports) >= days:
            if days <= 1:
                list.append(schemas.StudentInfo(stu_number=student.stu_number, stu_name=student.stu_name,
                                                phone_number=student.phone_number, email=student.email,
                                                address=student.address, family_address=student.family_address,
                                                id_card_number=student.id_card_number,
                                                id_card_type=student.id_card_type))
            else:
                for i in range(len(last_health_reports) - days + 1):
                    flag = True
                    for j in range(i+1,days+i):
                        #计算两个健康日报report_time时间的timestamp差值
                        if int(last_health_reports[i].report_time.timestamp()/60) - int(last_health_reports[i+j].report_time.timestamp()/60) != 24 * 60 * j:
                            flag = False
                            break
                    if flag:
                        list.append(schemas.StudentInfo(stu_number=student.stu_number, stu_name=student.stu_name,
                                                        phone_number=student.phone_number, email=student.email,
                                                        address=student.address, family_address=student.family_address,
                                                        id_card_number=student.id_card_number,
                                                        id_card_type=student.id_card_type))
                        break
    return schemas.AllStudentInfo(list=list, total=len(list))



# 过去days天一个学院学生出入学校最多的校区
def get_most_in_out_campus_in_department(department_name:str,days:int,db: Session):
    list = db.query(models.InOutCampus.campus_id,func.count('*').label('count')).filter(models.InOutCampus.stu_number.in_(db.query(models.Student.stu_number).filter(models.Student.class_id.in_(db.query(models.Class.id).filter(models.Class.department_id.in_(db.query(models.Department.id).filter(models.Department.department_name == department_name)))))),models.InOutCampus.date >= datetime.datetime.now() - datetime.timedelta(days=days)).group_by(models.InOutCampus.campus_id).all()
    # 找到最大的count 对应的campus_id
    max_count = 0
    campus_id = 1
    for i in list:
        if i.count > max_count:
            max_count = i.count
            campus_id = i.campus_id

    return schemas.DepartmentMostStudentInOutCampus(department_name=department_name,campus_name=db.query(models.Campus).filter(models.Campus.id == campus_id).first().campus_name)



# 各个学院学生出入学校最多的校区
def get_most_in_out_campus_in_school(days:int, db: Session):
    list = []
    for department in db.query(models.Department).all():
        list.append(get_most_in_out_campus_in_department(department.department_name,days,db))
    return list


def get_all_student_health_report_of_n_days_of_department(id:int,days: int, db: Session):
    data = []
    n_days_ago = datetime.datetime.now() - datetime.timedelta(days=days)
    for stu_number, stu_name in db.query(models.Student.stu_number, models.Student.stu_name).filter(
            models.Student.class_id.in_(db.query(models.Class.id).filter(models.Class.department_id == id))).all():
        health_report_of_n_days = schemas.StudentHealthReport(stu_number=stu_number, stu_name=stu_name, infoList=[])
        health_report_of_n_days.infoList = db.query(models.HealthReport.date, models.HealthReport.temperature,
                                                    models.HealthReport.location, models.HealthReport.report_time,
                                                    models.HealthReport.other_message) \
            .filter(models.HealthReport.stu_number == stu_number).order_by(models.HealthReport.date.desc()).all()
        health_report_of_n_days.infoList = list(filter(lambda x: x.report_time.timestamp() > n_days_ago.timestamp(),
                                                       health_report_of_n_days.infoList))
        # 将datetime转换为str
        new_info_list = []
        for info in health_report_of_n_days.infoList:
            new_info = schemas.HealthReportInfo(date=info.date.strftime('%Y-%m-%d'), temperature=info.temperature,
                                                location=info.location,
                                                report_time=info.report_time.strftime('%Y-%m-%d %H:%M:%S'),
                                                other_message=info.other_message)
            new_info_list.append(new_info)
        health_report_of_n_days.infoList = new_info_list
        data.append(health_report_of_n_days)
    return data


# 获取院系学生的入校权限
def get_all_student_right_of_campus_of_department(id:int,db: Session):
    data = []
    for student in db.query(models.Student).filter(models.Student.class_id.in_(db.query(models.Class.id).filter(models.Class.department_id == id))).all():
        right_of_campus = schemas.StudentRightOfCampus(stu_number=student.stu_number, stu_name=student.stu_name,
                                                       access='')
        for i in range(len(student.campus)):
            if i == len(student.campus) - 1:
                right_of_campus.access += student.campus[i].campus_name
            else:
                right_of_campus.access += student.campus[i].campus_name + ', '
        data.append(right_of_campus)
    return data


def get_all_student_leave_school_of_department(id:int,db: Session):
    data = []
    for leave_school in db.query(models.ApplyForLeaveSchool).filter(models.ApplyForLeaveSchool.stu_number.in_(db.query(models.Student.stu_number).filter(models.Student.class_id.in_(db.query(models.Class.id).filter(models.Class.department_id == id))))).filter(models.ApplyForLeaveSchool.level == '院系管理员').all():
        if leave_school.handle_time is None:
            handle_time = ''
        else:
            handle_time = leave_school.handle_time.strftime('%Y-%m-%d %H:%M:%S')
        leave_school_info = schemas.ApplyForLeaveSchool(pipeline_id=leave_school.pipeline_id, handlers='',
                                                        handle_time=handle_time, suggestion=leave_school.suggestion,
                                                        final_suggestion=leave_school.final_suggestion,
                                                        status=leave_school.status, stu_number=leave_school.stu_number,
                                                        stu_name='', leave_reason=leave_school.leave_reason,
                                                        destination=leave_school.destination,
                                                        departure_date=leave_school.departure_date.strftime(
                                                            '%Y-%m-%d %H:%M:%S'),
                                                        estimated_return_time=leave_school.estimated_return_time.strftime(
                                                            '%Y-%m-%d %H:%M:%S'),
                                                        handle_reason=leave_school.handle_reason)
        leave_school_info.stu_name = \
            db.query(models.Student.stu_name).filter(models.Student.stu_number == leave_school.stu_number).first()[0]
        if leave_school.level == "辅导员":
            leave_school_info.handlers = \
                db.query(models.Counselor.teacher_name).filter(models.Counselor.id == leave_school.handlers_id).first()[
                    0]
        elif leave_school.level == "院系管理员":
            leave_school_info.handlers = db.query(models.DepartmentAdmin.teacher_name).filter(
                models.DepartmentAdmin.id == leave_school.handlers_id).first()[0]
        data.append(leave_school_info)
    return data

