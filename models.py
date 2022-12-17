from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Table, Date, DateTime, Enum, Float, BigInteger
from sqlalchemy.orm import relationship, backref

from database import Base


# 学生表
class Student(Base):
    __tablename__ = "student"

    stu_number = Column(BigInteger, primary_key=True, index=True)
    stu_name = Column(String(100))
    phone_number = Column(String(100))
    email = Column(String(100))
    address = Column(String(100))
    family_address = Column(String(100))
    id_card_number = Column(String(100))
    id_card_type = Column(Enum('身份证', '护照', '军官证', '港澳通行证', '台胞证', '学生证', '其他'))
    class_id = Column(BigInteger, ForeignKey('class.id'))
    # class_id = Column(BigInteger)

    # 校区
    campus = relationship("Campus", secondary="student_campus", back_populates="student")

    # 班级
    class_ = relationship("Class")


# 校区表
class Campus(Base):
    __tablename__ = "campus"

    id = Column(BigInteger, primary_key=True, index=True)
    campus_name = Column(String(100))

    # 学生
    student = relationship("Student", secondary="student_campus", back_populates="campus")

    def __repr__(self):
        return f'<Campus {self.campus_name}>'


# 学生校区连接表
class StudentCampus(Base):
    __tablename__ = "student_campus"

    id = Column(BigInteger, primary_key=True, index=True)
    student_id = Column(BigInteger, ForeignKey('student.stu_number'))
    campus_id = Column(BigInteger, ForeignKey('campus.id'))


# 进出校园表
class InOutCampus(Base):
    __tablename__ = "in_out_campus"

    id = Column(BigInteger, primary_key=True, index=True)
    stu_number = Column(BigInteger, ForeignKey("student.stu_number"))
    status = Column(Enum('进校', '出校'))
    date = Column(DateTime)
    campus_id = Column(BigInteger, ForeignKey("campus.id"))

    # 学生
    student = relationship("Student")

    # 校区
    campus = relationship("Campus")


# 健康日报表
class HealthReport(Base):
    __tablename__ = "health_report"

    id = Column(String, primary_key=True, index=True)
    stu_number = Column(BigInteger, ForeignKey("student.stu_number"))
    date = Column(Date)
    temperature = Column(Float)
    location = Column(String(100))
    report_time = Column(DateTime)
    other_message = Column(String(100))

    # 学生
    student = relationship("Student")


# 进校申请表
class ApplyForEnterSchool(Base):
    __tablename__ = "apply_for_enter_school"

    id = Column(BigInteger, primary_key=True, index=True)
    stu_number = Column(BigInteger, ForeignKey("student.stu_number"))
    handlers = Column(BigInteger)
    handle_time = Column(DateTime)
    handle_reason = Column(String(100))
    final_suggestion = Column(Enum('同意', '拒绝'))
    status = Column(String(100))
    return_school_reason = Column(String(100))
    estimated_return_school_time = Column(Date)
    location_of_seven_days = Column(String(100))
    level = Column(Enum('辅导员', '院系管理员'))

    # 学生
    student = relationship("Student")

    # 处理人
    # department_admin = relationship("DepartmentAdmin", back_populates="apply_for_enter_school")


# 离校申请表
class ApplyForLeaveSchool(Base):
    __tablename__ = "apply_for_leave_school"

    id = Column(BigInteger, primary_key=True, index=True)
    stu_number = Column(BigInteger, ForeignKey("student.stu_number"))
    handlers = Column(BigInteger)
    handle_time = Column(DateTime)
    handle_reason = Column(String(100))
    final_suggestion = Column(Enum('同意', '拒绝'))
    status = Column(String(100))
    leave_school_reason = Column(String(100))
    estimated_leave_school_time = Column(Date)
    location_of_seven_days = Column(String(100))
    level = Column(Enum('辅导员', '院系管理员'))

    # 学生
    student = relationship("Student")


# 辅导员表
class Counselor(Base):
    __tablename__ = "counselor"

    id = Column(BigInteger, primary_key=True, index=True)
    teacher_name = Column(String(100))
    department_id = Column(BigInteger, ForeignKey("department.id"))
    class_id = Column(BigInteger, ForeignKey("class.id"))

    # 院系
    department = relationship("Department")

    # 班级 一对一
    class_ = relationship("Class", backref=backref("counselor", uselist=False))


# 院系管理员表
class DepartmentAdmin(Base):
    __tablename__ = "department_admin"

    id = Column(BigInteger, primary_key=True, index=True)
    teacher_name = Column(String(100))
    department_id = Column(BigInteger, ForeignKey("department.id"))

    # 院系 一对一
    department = relationship("Department", backref=backref("department_admin", uselist=False))


# 班级表
class Class(Base):
    __tablename__ = "class"

    id = Column(BigInteger, primary_key=True, index=True)
    class_name = Column(String(100))
    department_id = Column(BigInteger, ForeignKey("department.id"))

    # 院系
    department = relationship("Department")


# 院系表
class Department(Base):
    __tablename__ = "department"

    id = Column(BigInteger, primary_key=True, index=True)
    department_name = Column(String(100))


