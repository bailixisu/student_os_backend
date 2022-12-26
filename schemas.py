from pydantic import BaseModel
from typing import Any, Dict, List, Optional, Union
from sqlalchemy import null, DateTime
import uuid


# 学生
class Student(BaseModel):
    stu_number: int
    stu_name: str
    phone_number: str
    email: str
    address: str
    family_address: str
    id_card_number: str
    id_card_type: str
    class_id: int


# 健康日报
class HealthReportInfo(BaseModel):
    temperature: float
    location: str
    report_time: str
    other_message: str
    date: str


# 健康日报表
class HealthReport(BaseModel):
    stu_number: int
    date: str
    temperature: float
    location: str
    report_time: str
    other_message: str


# 学生健康日报信息
class StudentHealthReportPost(BaseModel):
    stu_number: int
    stu_name: str
    date: str
    temperature: float
    location: str
    time: str
    other_message: str


# 学生的健康日报
class StudentHealthReport(BaseModel):
    stu_number: int
    stu_name: str
    infoList: List[HealthReportInfo]


# response 格式
class Response(BaseModel):
    code: int = 200
    message: str = "success"
    data: Any = None


# 院系
class Department(BaseModel):
    id: int
    department_name: str


# 院系管理员
class DepartmentAdmin(BaseModel):
    id: int
    department_id: int
    teacher_name: str


# 班级
class Class(BaseModel):
    id: int
    class_name: str
    department_id: int


# 辅导员
class Counselor(BaseModel):
    id: int
    class_id: int
    teacher_name: str
    department_id: int


# 校区
class Campus(BaseModel):
    id: int
    campus_name: str


# 学生校区连接表
class StudentCampus(BaseModel):
    id: int
    student_id: int
    campus_id: int


# 进出校园
class InOutCampus(BaseModel):
    id: int
    stu_number: int
    status: str
    date: str
    campus_id: int


class StudentRightOfCampus(BaseModel):
    stu_number: int
    stu_name: str
    access: str


# 进校申请
class ApplyForEnterSchool(BaseModel):
    pipeline_id: int
    handlers: str
    handle_time: str
    suggestion: str
    final_suggestion: str
    handle_reason: str
    status: str
    stu_number: int
    stu_name: str
    return_school_reason: str
    location_of_seven_days: str
    estimated_return_school_time: str


class ApplyForEnterSchoolPost(BaseModel):
    stu_number: int
    stu_name: str
    return_school_reason: str
    location_of_seven_days: str
    estimated_return_school_time: str


# 离校申请
class ApplyForLeaveSchool(BaseModel):
    pipeline_id: int
    handlers: str
    handle_time: str
    suggestion: str
    final_suggestion: str
    status: str
    stu_number: int
    stu_name: str
    leave_reason: str
    destination: str
    departure_date: str
    estimated_return_time: str
    handle_reason: str


class AddNewLeaveSchool(BaseModel):
    class_id: int
    pipeline_id: int
    stu_number: int
    leave_reason: str
    destination: str
    departure_date: str
    estimated_return_time: str
    submit_time: str


class AddNewEnterSchool(BaseModel):
    class_id: int
    pipeline_id: int
    stu_number: int
    return_school_reason: str
    location_of_seven_days: str
    estimated_return_school_time: str
    submit_time: str


# 进校申请表的schema
class ApplyForEnterSchoolSchema(BaseModel):
    handlers_id: int
    pipeline_id: int
    handlers: str
    suggestion: str
    final_suggestion: str
    handle_reason: str
    status: str
    stu_number: int
    return_school_reason: str
    location_of_seven_days: str
    estimated_return_school_time: str
    out_date_flag: int
    submit_time: str
    level: str


# 离校申请表的schema
class ApplyForLeaveSchoolSchema(BaseModel):
    handlers_id: int
    level: str
    pipeline_id: int
    handlers: str
    submit_time: str
    suggestion: str
    final_suggestion: str
    status: str
    stu_number: int
    leave_reason: str
    destination: str
    departure_date: str
    estimated_return_time: str
    handle_reason: str
    out_date_flag: int


class ApplyForLeaveSchoolPost(BaseModel):
    stu_number: int
    stu_name: str
    leave_reason: str
    destination: str
    departure_date: str
    estimated_return_time: str


# 学生离校时间
class StudentLeaveSchoolTimeOfYear(BaseModel):
    stu_number: int
    stu_name: str
    leave_time: str


# 学生平均离校时间
class StudentLeaveSchoolTimeAvg(BaseModel):
    stu_number: int
    stu_name: str
    average_leave_time: str

class StudentLeaveSchoolTimeAvgTwo(BaseModel):
    stu_number: int
    stu_name: str
    average_time: str
# 学生未通过的申请
class StudentLeaveSchoolNoPassOfNDays(BaseModel):
    total: int
    list: List[ApplyForLeaveSchool]


# 学生未通过的入校申请
class StudentEnterSchoolNoPassOfNDays(BaseModel):
    total: int
    list: List[ApplyForEnterSchool]


# 学生申请数量
class StudentApplyCount(BaseModel):
    stu_number: int
    stu_name: str
    total: int


# 离校学生信息
class StudentLeaveSchoolInfo(BaseModel):
    stu_number: int
    stu_name: str
    phone_number: str
    email: str
    address: str
    family_address: str
    id_card_number: str
    id_card_type: str
    departure_time: str


class AllStudentLeaveSchoolInfo(BaseModel):
    total: int
    list: List[StudentLeaveSchoolInfo]


class StudentInfo(BaseModel):
    stu_number: int
    stu_name: str
    phone_number: str
    email: str
    address: str
    family_address: str
    id_card_number: str
    id_card_type: str


# 所有学生信息
class AllStudentInfo(BaseModel):
    total: int
    list: List[StudentInfo]


# 学生信息
class StudentNumAndName(BaseModel):
    stu_number: int
    stu_name: str


class AllStudentNumAndName(BaseModel):
    total: int
    list: List[StudentNumAndName]


# 学院学生出入最多的校区
class DepartmentMostStudentInOutCampus(BaseModel):
    department_name: str
    campus_name: str


class AllStudentNumAndNameOfClass(BaseModel):
    class_id: int
    stu: List[StudentNumAndName]


class StudentApplyCountOfClass(BaseModel):
    class_id: int
    stu: List[StudentApplyCount]


# 统计信息
class ClassStatisticsInfo(BaseModel):
    class_id: int
    leaving_num: int
    surpass_num: int
    not_leave_num: int


class ClassEnterAndLeaveApply(BaseModel):
    class_id: int
    num1: int
    num2: int


class OtherClassSameTimeReport(BaseModel):
    class_id: int
    num: int


class StudentALLInfo(BaseModel):
    stu_number: int
    stu_name: str
    phone_number: str
    email: str
    address: str
    family_address: str
    id_card_number: str
    id_card_type: str
    access: str
    leave_time: str


class ApplyPost(BaseModel):
    id: int
    pipeline_id: int
    result: str
    suggestion: str
    reason: str
    type: str
