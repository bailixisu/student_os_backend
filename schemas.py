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
    id: int
    stu_number: int
    date: str
    temperature: float
    location: str
    report_time: str
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
