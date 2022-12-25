import datetime
import time

from sqlalchemy import func
from sqlalchemy.orm import Session

import models
import schemas
from sqlalchemy.sql import distinct
import crud

def get_all_student_health_report_of_n_days_of_class(id: int, days: int, db: Session):
    data = []
    n_days_ago = datetime.datetime.now() - datetime.timedelta(days=days)
    for stu_number, stu_name in db.query(models.Student.stu_number, models.Student.stu_name).filter(
            models.Student.class_id == id).all():
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
def get_all_student_right_of_campus_of_class(id: int, db: Session):
    data = []
    for student in db.query(models.Student).filter(models.Student.class_id == id).all():
        right_of_campus = schemas.StudentRightOfCampus(stu_number=student.stu_number, stu_name=student.stu_name,
                                                       access='')
        for i in range(len(student.campus)):
            if i == len(student.campus) - 1:
                right_of_campus.access += student.campus[i].campus_name
            else:
                right_of_campus.access += student.campus[i].campus_name + ', '
        data.append(right_of_campus)
    return data


def get_all_student_leave_school_of_class(id: int, db: Session):
    data = []
    for leave_school in db.query(models.ApplyForLeaveSchool).filter(models.ApplyForLeaveSchool.stu_number.in_(
            db.query(models.Student.stu_number).filter(models.Student.class_id == id))).filter(
            models.ApplyForLeaveSchool.level == "辅导员").all():
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


def get_all_student_enter_school_of_class(id: int, db: Session):
    data = []
    for enter_school in db.query(models.ApplyForEnterSchool).filter(models.ApplyForEnterSchool.stu_number.in_(
            db.query(models.Student.stu_number).filter(models.Student.class_id == id))).filter(
            models.ApplyForEnterSchool.level == "辅导员").all():
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


def get_all_student_leave_school_time_of_class(id: int, db: Session):
    data = []
    if is_leap_year(datetime.datetime.now().year - 1):
        days = 366
    else:
        days = 365
    year_ago = datetime.datetime.now() - datetime.timedelta(days=days)
    for student in db.query(models.Student).filter(models.Student.class_id == id).all():
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


def get_all_student_leave_school_no_pass_of_class(id: int, days: int, db: Session):
    n_days_ago = datetime.datetime.now() - datetime.timedelta(days=days)
    data = schemas.StudentLeaveSchoolNoPassOfNDays(total=0, list=[])
    for leave_school in db.query(models.ApplyForLeaveSchool).filter(models.ApplyForLeaveSchool.status == '待审核'). \
            filter(models.ApplyForLeaveSchool.submit_time > n_days_ago).filter(
        models.ApplyForLeaveSchool.stu_number.in_(
            db.query(models.Student.stu_number).filter(models.Student.class_id == id))).filter(
            models.ApplyForLeaveSchool.level == "辅导员").all():
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


def get_all_student_enter_school_no_pass_of_class(id: int, days: int, db: Session):
    n_days_ago = datetime.datetime.now() - datetime.timedelta(days=days)
    data = schemas.StudentEnterSchoolNoPassOfNDays(total=0, list=[])
    for enter_school in db.query(models.ApplyForEnterSchool).filter(models.ApplyForEnterSchool.status == '待审核'). \
            filter(models.ApplyForEnterSchool.submit_time > n_days_ago).filter(
        models.ApplyForEnterSchool.stu_number.in_(
            db.query(models.Student.stu_number).filter(models.Student.class_id == id))).filter(
            models.ApplyForEnterSchool.level == "辅导员").all():
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


def get_all_student_apply_for_enter_count_of_class(id: int, num: int, db: Session):
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


def get_all_student_average_leave_time_of_class(id: int, num: int, db: Session):
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
def get_all_student_leave_school_info_of_class(id: int, db: Session):
    list = []
    for student in db.query(models.Student).filter(models.Student.class_id == id).all():
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
def get_all_student_leave_school_more_than_one_day_info_of_class(id: int, db: Session):
    list = []
    for student in db.query(models.Student).filter(models.Student.class_id == id).all():
        last_in_out_info = db.query(models.InOutCampus).filter(models.InOutCampus.stu_number == student.stu_number) \
            .order_by(models.InOutCampus.date.desc()).first()
        if last_in_out_info is not None and last_in_out_info.status == '离校':
            if datetime.datetime.now().timestamp() - last_in_out_info.date.timestamp() > 24 * 60 * 60:
                infos = db.query(models.ApplyForLeaveSchool) \
                    .filter(student.stu_number == models.ApplyForLeaveSchool.stu_number,
                            models.ApplyForLeaveSchool.out_date_flag == 0).all()
                applys = set()
                for info in infos:
                    applys.add(info.pipeline_id)
                flag = False
                for apply in applys:
                    if db.query(models.ApplyForLeaveSchool).filter(models.ApplyForLeaveSchool.pipeline_id == apply,
                                                                   models.ApplyForLeaveSchool.status == '已拒绝').first() is None:
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
def get_all_student_apply_for_leave_school_but_not_leave_school_info_of_class(id: int, db: Session):
    list = []
    for student in db.query(models.Student).filter(models.Student.class_id == id).all():
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


# 过去n天的一直在校的学生(按照班级)
def get_all_student_stay_in_school_more_than_n_days_info_in_class_level(id: int, days: int, db: Session):
    list = []
    for student in db.query(models.Student).filter(models.Student.class_id == id).all():
        last_in_out_info = db.query(models.InOutCampus).filter(models.InOutCampus.stu_number == student.stu_number) \
            .order_by(models.InOutCampus.date.desc()).first()
        if last_in_out_info is not None and last_in_out_info.status == '进校':
            if datetime.datetime.now().timestamp() - last_in_out_info.date.timestamp() > days * 24 * 60 * 60:
                list.append(schemas.StudentNumAndName(stu_number=student.stu_number, stu_name=student.stu_name))
    return list


# 连续n天健康日报相同
def get_all_student_health_report_same_for_n_days_info_of_class(id: int, days: int, db: Session):
    list = []
    for student in db.query(models.Student).filter(models.Student.class_id == id).all():
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
                    for j in range(i + 1, days + i):
                        # 计算两个健康日报report_time时间的timestamp差值
                        if int(last_health_reports[i].report_time.timestamp() / 60) - int(
                                last_health_reports[i + j].report_time.timestamp() / 60) != 24 * 60 * j:
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
def get_most_in_out_campus_in_department(department_name: str, days: int, db: Session):
    list = db.query(models.InOutCampus.campus_id, func.count('*').label('count')).filter(
        models.InOutCampus.stu_number.in_(db.query(models.Student.stu_number).filter(models.Student.class_id.in_(
            db.query(models.Class.id).filter(models.Class.department_id.in_(
                db.query(models.Department.id).filter(models.Department.department_name == department_name)))))),
        models.InOutCampus.date >= datetime.datetime.now() - datetime.timedelta(days=days)).group_by(
        models.InOutCampus.campus_id).all()
    # 找到最大的count 对应的campus_id
    max_count = 0
    campus_id = 1
    for i in list:
        if i.count > max_count:
            max_count = i.count
            campus_id = i.campus_id

    return schemas.DepartmentMostStudentInOutCampus(department_name=department_name,
                                                    campus_name=db.query(models.Campus).filter(
                                                        models.Campus.id == campus_id).first().campus_name)


# 各个学院学生出入学校最多的校区
def get_most_in_out_campus_in_school(days: int, db: Session):
    list = []
    for department in db.query(models.Department).all():
        list.append(get_most_in_out_campus_in_department(department.department_name, days, db))
    return list


def get_other_class_statistics_info(id: int, db: Session):
    list = []
    for class_ in db.query(models.Class).filter(db.query(models.Class).filter(
            models.Class.id == id).first().department_id == models.Class.department_id).all():
        if class_.id != id:
            list.append(schemas.ClassStatisticsInfo(class_id=class_.id,
                                                    leaving_num=get_all_student_leave_school_info_of_class(class_.id,
                                                                                                           db).total,
                                                    surpass_num=get_all_student_leave_school_more_than_one_day_info_of_class(
                                                        class_.id, db).total,
                                                    not_leave_num=get_all_student_apply_for_leave_school_but_not_leave_school_info_of_class(
                                                        class_.id, db).total))
    return list


def get_other_class_enter_and_leave_apply(id: int, days: int, db: Session):
    list = []
    for class_ in db.query(models.Class).filter(db.query(models.Class).filter(
            models.Class.id == id).first().department_id == models.Class.department_id).all():
        if class_.id != id:
            list.append(schemas.ClassEnterAndLeaveApply(class_id=class_.id,
                                                        num1=get_all_student_enter_school_no_pass_of_class(class_.id,
                                                                                                           days,
                                                                                                           db).total,
                                                        num2=get_all_student_leave_school_no_pass_of_class(class_.id,
                                                                                                           days,
                                                                                                           db).total))
    return list


def get_other_class_same_health_report(id: int, days: int, db: Session):
    list = []
    for class_ in db.query(models.Class).filter(db.query(models.Class).filter(
            models.Class.id == id).first().department_id == models.Class.department_id).all():
        if class_.id != id:
            list.append(schemas.OtherClassSameTimeReport(class_id=class_.id,
                                                         num=get_all_student_health_report_same_for_n_days_info_of_class(
                                                             class_.id, days, db).total))
    return list


def handle_class_apply(apply: schemas.ApplyPost, db: Session):
    if apply.result == "同意":
        status = "已同意"
        final_result = "同意"
    else:
        status = "已拒绝"
        final_result = "不同意"
    if apply.type == '入校':
        db.query(models.ApplyForEnterSchool).filter(models.ApplyForEnterSchool.pipeline_id == apply.pipeline_id,
                                                    models.ApplyForEnterSchool.level == "辅导员").update({
            models.ApplyForEnterSchool.status: status,
            models.ApplyForEnterSchool.final_suggestion: final_result,
            models.ApplyForEnterSchool.handle_reason: apply.reason,
            models.ApplyForEnterSchool.handle_time: datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            models.ApplyForEnterSchool.suggestion: apply.suggestion
        })
        db.commit()
        if apply.result == "同意":
            enter_apply = db.query(models.ApplyForEnterSchool).filter(
                models.ApplyForEnterSchool.pipeline_id == apply.pipeline_id,
                models.ApplyForEnterSchool.level == "辅导员").first()

            add_student_enter_apply(schemas.AddNewEnterSchool(
                class_id=enter_apply.handlers_id,
                pipeline_id=enter_apply.pipeline_id,
                stu_number=enter_apply.stu_number,
                return_school_reason=enter_apply.return_school_reason,
                location_of_seven_days=enter_apply.location_of_seven_days,
                estimated_return_school_time=enter_apply.estimated_return_school_time.strftime("%Y-%m-%d %H:%M:%S"),
                submit_time=enter_apply.submit_time.strftime("%Y-%m-%d %H:%M:%S"),
            ), db)
    else:
        db.query(models.ApplyForLeaveSchool).filter(models.ApplyForLeaveSchool.pipeline_id == apply.pipeline_id,
                                                    models.ApplyForLeaveSchool.level == "辅导员").update({
            models.ApplyForLeaveSchool.status: status,
            models.ApplyForLeaveSchool.final_suggestion: final_result,
            models.ApplyForLeaveSchool.handle_reason: apply.reason,
            models.ApplyForLeaveSchool.handle_time: datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            models.ApplyForLeaveSchool.suggestion: apply.suggestion
        })
        db.commit()
        if apply.result == "同意":
            leave_apply = db.query(models.ApplyForLeaveSchool).filter(
                models.ApplyForLeaveSchool.pipeline_id == apply.pipeline_id,
                models.ApplyForLeaveSchool.level == "辅导员").first()
            add_student_leave_apply(schemas.AddNewLeaveSchool(
                class_id=leave_apply.handlers_id,
                pipeline_id=leave_apply.pipeline_id,
                stu_number=leave_apply.stu_number,
                leave_reason=leave_apply.leave_reason,
                departure_date=leave_apply.departure_date.strftime("%Y-%m-%d %H:%M:%S"),
                estimated_return_time=leave_apply.estimated_return_time.strftime("%Y-%m-%d %H:%M:%S"),
                submit_time=leave_apply.submit_time.strftime("%Y-%m-%d %H:%M:%S"),
                destination=leave_apply.destination
            ), db)





def add_student_leave_apply(leave_apply:schemas.AddNewLeaveSchool,db: Session):
    #得到当前院系管理员
    handler=db.query(models.DepartmentAdmin).filter(models.DepartmentAdmin.department_id== db.query(models.Counselor).filter(models.Counselor.id==leave_apply.class_id).first().department_id).first()
    crud.create_out_campus_application(db,schemas.ApplyForLeaveSchoolSchema(
        stu_number=leave_apply.stu_number,
        leave_reason=leave_apply.leave_reason,
        handle_reason="",
        status="待审核",
        level="院系管理员",
        handlers_id=handler.id,
        submit_time=leave_apply.submit_time,
        pipeline_id=db.query(models.ApplyForLeaveSchool).count()+10,
        suggestion="",
        final_suggestion="",
        out_date_flag=0,
        estimated_return_time=leave_apply.estimated_return_time,
        destination=leave_apply.destination,
        departure_date=leave_apply.departure_date,
        handlers=handler.teacher_name
    ))


def add_student_enter_apply(enter_apply:schemas.AddNewEnterSchool,db: Session):
    #得到当前学生辅导员的id
    handler=db.query(models.DepartmentAdmin).filter(models.DepartmentAdmin.department_id== db.query(models.Counselor).filter(models.Counselor.id==enter_apply.class_id).first().department_id).first()
    crud.create_in_campus_application(db,schemas.ApplyForEnterSchoolSchema(
        stu_number=enter_apply.stu_number,
        return_school_reason=enter_apply.return_school_reason,
        handle_reason="",
        location_of_seven_days=enter_apply.location_of_seven_days,
        estimated_return_school_time=enter_apply.estimated_return_school_time,
        status="待审核",
        level="院系管理员",
        handlers_id=handler.id,
        submit_time=enter_apply.submit_time,
        pipeline_id=db.query(models.ApplyForEnterSchool).count()+10,
        suggestion="",
        final_suggestion="",
        out_date_flag=0,
        handlers=handler.teacher_name
    ))
