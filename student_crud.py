import datetime
import time

from sqlalchemy import func
from sqlalchemy.orm import Session

import models
import schemas
from sqlalchemy.sql import distinct
import counselor_crud
import crud

def get_student_info(id:int, db: Session):
    student = db.query(models.Student).filter(models.Student.stu_number == id).first()
    access =""
    for i in range(len(student.campus)):
        if i == len(student.campus) - 1:
            access += student.campus[i].campus_name
        else:
            access += student.campus[i].campus_name + ', '
    delta = 0
    if is_leap_year(datetime.datetime.now().year - 1):
        days = 366
    else:
        days = 365
    year_ago = datetime.datetime.now() - datetime.timedelta(days=days)
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
    leave_time = str(datetime.timedelta(seconds=int(delta)))
    return schemas.StudentALLInfo(stu_number=student.stu_number, stu_name=student.stu_name,phone_number=student.phone_number,
                                  email=student.email, address=student.address, family_address=student.family_address,
                                  id_card_number=student.id_card_number, id_card_type=student.id_card_type,
                                    access=access, leave_time=leave_time)


def get_student_health_report_of_n_days(id:int, days:int, db: Session):
    student = db.query(models.Student).filter(models.Student.stu_number == id).first()
    stu_number = student.stu_number
    stu_name = student.stu_name
    n_days_ago = datetime.datetime.now() - datetime.timedelta(days=days)
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
    return new_info_list



# 判断是不是闰年
def is_leap_year(year):
    if (year % 4 == 0 and year % 100 != 0) or year % 400 == 0:
        return True
    else:
        return False



# 查看离校申请
def get_leave_campus_apply(id:int, db: Session):
    data = []
    for leave_school in db.query(models.ApplyForLeaveSchool).filter(models.ApplyForLeaveSchool.stu_number == id).all():
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


# 查看进校申请
def get_enter_campus_apply(id:int, db: Session):
    data = []
    for enter_school in db.query(models.ApplyForEnterSchool).filter(models.ApplyForEnterSchool.stu_number == id).all():
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


def get_my_class_statistics_info(id:int, db: Session):
    class_=db.query(models.Class).filter(models.Class.id==db.query(models.Student.class_id).filter(models.Student.stu_number==id).first()[0]).first()
    return schemas.ClassStatisticsInfo(class_id=class_.id,
                                            leaving_num=counselor_crud.get_all_student_leave_school_info_of_class(class_.id,
                                                                                                   db).total,
                                            surpass_num=counselor_crud.get_all_student_leave_school_more_than_one_day_info_of_class(
                                                class_.id, db).total,
                                            not_leave_num=counselor_crud.get_all_student_apply_for_leave_school_but_not_leave_school_info_of_class(
                                                class_.id, db).total)



def get_my_class_enter_and_leave_apply(id:int,days:int,db: Session):
    class_=db.query(models.Class).filter(models.Class.id==db.query(models.Student.class_id).filter(models.Student.stu_number==id).first()[0]).first()
    return schemas.ClassEnterAndLeaveApply(class_id=class_.id,
                                                num1=counselor_crud.get_all_student_enter_school_no_pass_of_class(class_.id,days,db).total,
                                                num2=counselor_crud.get_all_student_leave_school_no_pass_of_class(class_.id,days,db).total)


def get_my_class_same_health_report(id:int,days:int,db: Session):
    class_=db.query(models.Class).filter(models.Class.id==db.query(models.Student.class_id).filter(models.Student.stu_number==id).first()[0]).first()
    return schemas.OtherClassSameTimeReport(class_id=class_.id,
                                                num=counselor_crud.get_all_student_health_report_same_for_n_days_info_of_class(class_.id,days,db).total)


def add_student_health_report(health_report:schemas.StudentHealthReportPost,db: Session):
    #计算health_report的数量
    crud.create_health_report(db,schemas.HealthReport(
        stu_number=health_report.stu_number,
        temperature=health_report.temperature,
        location=health_report.location,
        other_message=health_report.other_message,
        report_time=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        date=datetime.datetime.now().strftime('%Y-%m-%d')
    ))


def add_student_enter_apply(enter_apply:schemas.ApplyForEnterSchoolPost,db: Session):
    #得到当前学生辅导员的id
    counselor=db.query(models.Counselor).filter(models.Counselor.class_id == db.query(models.Student.class_id).filter(models.Student.stu_number==enter_apply.stu_number).first()[0]).first()
    crud.create_in_campus_application(db,schemas.ApplyForEnterSchoolSchema(
        stu_number=enter_apply.stu_number,
        return_school_reason=enter_apply.return_school_reason,
        handle_reason="",
        location_of_seven_days=enter_apply.location_of_seven_days,
        estimated_return_school_time=enter_apply.estimated_return_school_time,
        status="待审核",
        level="辅导员",
        handlers_id=counselor.id,
        submit_time=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        pipeline_id=db.query(models.ApplyForEnterSchool).count()+10,
        suggestion="",
        final_suggestion="",
        out_date_flag=0,
        handlers=counselor.teacher_name
    ))


def add_student_leave_apply(leave_apply:schemas.ApplyForLeaveSchoolPost,db: Session):
    #得到当前学生辅导员的id
    handler=db.query(models.Counselor).filter(models.Counselor.class_id == db.query(models.Student.class_id).filter(models.Student.stu_number==leave_apply.stu_number).first()[0]).first()
    crud.create_out_campus_application(db,schemas.ApplyForLeaveSchoolSchema(
        stu_number=leave_apply.stu_number,
        leave_reason=leave_apply.leave_reason,
        handle_reason="",
        status="待审核",
        level="辅导员",
        handlers_id=handler.id,
        submit_time=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        pipeline_id=db.query(models.ApplyForLeaveSchool).count()+10,
        suggestion="",
        final_suggestion="",
        out_date_flag=0,
        estimated_return_time=leave_apply.estimated_return_time,
        destination=leave_apply.destination,
        departure_date=leave_apply.departure_date,
        handlers=handler.teacher_name
    ))



def modify_student_info(student:schemas.StudentInfo,db: Session):
    #更新学生信息
    db.query(models.Student).filter(models.Student.stu_number==student.stu_number).update({
        models.Student.phone_number:student.phone_number,
        models.Student.email:student.email,
        models.Student.address:student.address,
        models.Student.family_address:student.family_address,
        models.Student.id_card_type:student.id_card_type,
        models.Student.id_card_number:student.id_card_number
    })
    db.commit()
