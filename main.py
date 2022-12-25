from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

import crud
import models
import schemas
import admin_crud
import counselor_crud
import student_crud
from database import SessionLocal, engine
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root(department_name:str,db: Session = Depends(get_db)):
    # crud.get_most_in_out_campus_in_department(department_name,db)
    # crud.create_in_out_campus(db=db, in_out_campus=schemas.InOutCampus(
    #     id = 10,
    #     stu_number=20301234568,
    #     status="进校",
    #     date="2020-12-12 15:12:12",
    #     campus_id=1
    # ))
    # crud.create_in_out_campus(db=db, in_out_campus=schemas.InOutCampus(
    #     id = 11,stu_number=20301234568,status="离校",date="2020-12-12 16:12:12",campus_id=1
    # ))
    # crud.create_in_out_campus(db=db, in_out_campus=schemas.InOutCampus(
    #     id = 12,stu_number=20301234568,status="进校",date="2020-12-12 17:12:12",campus_id=1
    # ))
    # crud.create_in_out_campus(db=db, in_out_campus=schemas.InOutCampus(
    #     id = 13,stu_number=20301234568,status="离校",date="2020-12-12 18:12:12",campus_id=1
    # ))
    # crud.create_in_out_campus(db=db, in_out_campus=schemas.InOutCampus(
    #     id = 14,stu_number=20301234569,status="进校",date="2020-12-13 09:12:12",campus_id=1
    # ))
    # crud.create_in_out_campus(db=db, in_out_campus=schemas.InOutCampus(
    #     id = 15,stu_number=20301234569,status="离校",date="2020-12-13 10:12:12",campus_id=1
    # ))
    # crud.create_in_out_campus(db=db, in_out_campus=schemas.InOutCampus(
    #     id = 16,stu_number=20301234569,status="进校",date="2020-12-13 11:12:12",campus_id=1
    # ))
    # crud.create_in_out_campus(db=db, in_out_campus=schemas.InOutCampus(
    #     id = 17,stu_number=20301234569,status="离校",date="2020-12-13 12:12:12",campus_id=1
    # ))
    # crud.create_in_out_campus(db=db, in_out_campus=schemas.InOutCampus(
    #     id = 18,stu_number=20301234570,status="进校",date="2020-12-14 13:12:12",campus_id=1
    # ))
    # crud.create_in_out_campus(db=db, in_out_campus=schemas.InOutCampus(
    #     id = 19,stu_number=20301234570,status="离校",date="2020-12-14 14:12:12",campus_id=1
    # ))
    # crud.create_in_out_campus(db=db, in_out_campus=schemas.InOutCampus(
    #     id = 20,stu_number=20301234571,status="进校",date="2020-12-14 15:12:12",campus_id=1
    # ))
    # crud.create_in_out_campus(db=db, in_out_campus=schemas.InOutCampus(
    #     id = 21,stu_number=20301234572,status="进校",date="2020-12-14 16:12:12",campus_id=3
    # ))

    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.get("/root/info", response_model=schemas.Response)
def get_root_info(days: int, db: Session = Depends(get_db)):
    try:
        data = crud.get_all_student_health_report_of_n_days(days, db)
        return schemas.Response(data=data)
    except Exception as e:
        return schemas.Response(error=str(e), code=500)


@app.get("/root/access", response_model=schemas.Response)
def get_root_access(db: Session = Depends(get_db)):
    try:
        data = crud.get_all_student_right_of_campus(db)
        return schemas.Response(data=data)
    except Exception as e:
        return schemas.Response(message=str(e), code=500)


@app.get("/root/leave", response_model=schemas.Response)
def get_root_leave(db: Session = Depends(get_db)):
    try:
        data = crud.get_all_student_leave_school(db)
        return schemas.Response(data=data)
    except Exception as e:
        return schemas.Response(message=str(e), code=500)


@app.get("/root/enter", response_model=schemas.Response)
def get_root_enter(db: Session = Depends(get_db)):
    try:
        data = crud.get_all_student_enter_school(db)
        return schemas.Response(data=data)
    except Exception as e:
        return schemas.Response(message=str(e), code=500)


@app.get("/root/leave/time", response_model=schemas.Response)
def get_root_leave_time(db: Session = Depends(get_db)):
    try:
        data = crud.get_all_student_leave_school_time(db)
        return schemas.Response(data=data)
    except Exception as e:
        return schemas.Response(message=str(e), code=500)


@app.get("/root/leave/noPass", response_model=schemas.Response)
def get_root_leave_noPass(days: int, db: Session = Depends(get_db)):
    try:
        data = crud.get_all_student_leave_school_no_pass(days,db)
        return schemas.Response(data=data)
    except Exception as e:
        return schemas.Response(message=str(e), code=500)


@app.get("/root/enter/noPass", response_model=schemas.Response)
def get_root_enter_noPass(days: int, db: Session = Depends(get_db)):
    try:
        data = crud.get_all_student_enter_school_no_pass(days, db)
        return schemas.Response(data=data)
    except Exception as e:
        return schemas.Response(message=str(e), code=500)


@app.get("/root/enter/most/school", response_model=schemas.Response)
def get_root_enter_most_school(num: int, db: Session = Depends(get_db)):
    try:
        data = crud.get_all_student_apply_for_enter_count_in_school(num, db)
        return schemas.Response(data=data)
    except Exception as e:
        return schemas.Response(message=str(e), code=500)


@app.get("/root/enter/most/department", response_model=schemas.Response)
def get_root_enter_most_department(department_name:str,num: int, db: Session = Depends(get_db)):
    try:
        data = crud.get_all_student_apply_for_enter_count_in_department(department_name, num, db)
        return schemas.Response(data=data)
    except Exception as e:
        return schemas.Response(message="查询信息有误", code=400)



@app.get("/root/enter/most/class", response_model=schemas.Response)
def get_root_enter_most_class(id:int,num: int, db: Session = Depends(get_db)):
    try:
        data = crud.get_all_student_apply_for_enter_count_in_class(id, num, db)
        return schemas.Response(data=data)
    except Exception as e:
        return schemas.Response(message="查询信息有误", code=400)


@app.get("/root/leave/most/school", response_model=schemas.Response)
def get_root_leave_most_school(num: int, db: Session = Depends(get_db)):
    try:
        data = crud.get_all_student_average_leave_time_in_school(num, db)
        return schemas.Response(data=data)
    except Exception as e:
        return schemas.Response(message=str(e), code=500)


@app.get("/root/leave/most/department", response_model=schemas.Response)
def get_root_leave_most_department(department_name:str,num: int, db: Session = Depends(get_db)):
    try:
        data = crud.get_all_student_average_leave_time_in_department(department_name, num, db)
        return schemas.Response(data=data)
    except Exception as e:
        return schemas.Response(message="查询信息有误", code=400)


@app.get("/root/leave/most/class", response_model=schemas.Response)
def get_root_leave_most_class(id:int,num: int, db: Session = Depends(get_db)):
    try:
        data = crud.get_all_student_average_leave_time_in_class(id, num, db)
        return schemas.Response(data=data)
    except Exception as e:
        return schemas.Response(message="查询信息有误", code=400)


@app.get("/root/leaving", response_model=schemas.Response)
def get_root_leaving(db: Session = Depends(get_db)):
    try:
        data = crud.get_all_student_leave_school_info(db)
        return schemas.Response(data=data)
    except Exception as e:
        return schemas.Response(message=str(e), code=500)


@app.get("/root/leave/noApply", response_model=schemas.Response)
def get_root_leave_noApply(db: Session = Depends(get_db)):

    try:
        data = crud.get_all_student_leave_school_more_than_one_day_info(db)
        return schemas.Response(data=data)
    except Exception as e:
        return schemas.Response(message=str(e), code=500)


@app.get("/root/apply/noLeave", response_model=schemas.Response)
def get_root_apply_noLeave(db: Session = Depends(get_db)):
        try:
            data = crud.get_all_student_apply_for_leave_school_but_not_leave_school_info(db)
            return schemas.Response(data=data)
        except Exception as e:
            return schemas.Response(message=str(e), code=500)


@app.get("/root/stay/school", response_model=schemas.Response)
def get_root_stay_school(days:int, db: Session = Depends(get_db)):
    try:
        data = crud.get_all_student_stay_in_school_more_than_n_days_info_in_school_level(days,db)
        return schemas.Response(data=data)
    except Exception as e:
        return schemas.Response(message=str(e), code=500)


@app.get("/root/stay/department", response_model=schemas.Response)
def get_root_stay_department(department_name:str,days:int,db: Session = Depends(get_db)):
    try:
        data = crud.get_all_student_stay_in_school_more_than_n_days_info_in_department_level(department_name,days, db)
        return schemas.Response(data=data)
    except Exception as e:
        return schemas.Response(message="查询信息有误", code=400)


@app.get("/root/stay/class", response_model=schemas.Response)
def get_root_stay_class(id:int,num:int,db: Session = Depends(get_db)):
    try:
        data = crud.get_all_student_stay_in_school_more_than_n_days_info_in_class_level(id,num, db)
        return schemas.Response(data=data)
    except Exception as e:
        return schemas.Response(message="查询信息有误", code=400)


@app.get("/root/same", response_model=schemas.Response)
def get_root_same(days:int,db: Session = Depends(get_db)):
    try:
        data = crud.get_all_student_health_report_same_for_n_days_info_in_school_level(days,db)
        return schemas.Response(data=data)
    except Exception as e:
        return schemas.Response(message=str(e), code=500)


@app.get("/root/record/most", response_model=schemas.Response)
def get_root_record_most(days:int,db: Session = Depends(get_db)):
    try:
        data = crud.get_most_in_out_campus_in_school(days,db)
        return schemas.Response(data=data)
    except Exception as e:
        return schemas.Response(message=str(e), code=500)


# 院系管理员
@app.get("/department/info", response_model=schemas.Response)
def get_department_info(id:int,days:int,db: Session = Depends(get_db)):
    try:
        data = crud.get_all_student_health_report_of_n_days_of_department(id,days,db)
        return schemas.Response(data=data)
    except Exception as e:
        return schemas.Response(message=str(e), code=500)


@app.get("/department/access", response_model=schemas.Response)
def get_department_access(id:int,db: Session = Depends(get_db)):
    try:
        data = crud.get_all_student_right_of_campus_of_department(id,db)
        return schemas.Response(data=data)
    except Exception as e:
        return schemas.Response(message=str(e), code=500)


@app.get("/department/leave", response_model=schemas.Response)
def get_department_leave(id:int,db: Session = Depends(get_db)):
    try:
        data = crud.get_all_student_leave_school_of_department(id,db)
        return schemas.Response(data=data)
    except Exception as e:
        return schemas.Response(message=str(e), code=500)


@app.get("/department/enter", response_model=schemas.Response)
def get_department_enter(id:int,db: Session = Depends(get_db)):
    try:
        data = admin_crud.get_all_student_enter_school_of_department(id,db)
        return schemas.Response(data=data)
    except Exception as e:
        return schemas.Response(message=str(e), code=500)


@app.get("/department/leave/time", response_model=schemas.Response)
def get_department_leave_time(id:int,db: Session = Depends(get_db)):
    try:
        data = admin_crud.get_all_student_leave_school_time_of_department(id,db)
        return schemas.Response(data=data)
    except Exception as e:
        return schemas.Response(message=str(e), code=500)


@app.get("/department/leave/noPass", response_model=schemas.Response)
def get_department_leave_noPass(id:int,days:int,db: Session = Depends(get_db)):
    try:
        data = admin_crud.get_all_student_leave_school_no_pass_of_department(id,days,db)
        return schemas.Response(data=data)
    except Exception as e:
        return schemas.Response(message=str(e), code=500)


@app.get("/department/enter/noPass", response_model=schemas.Response)
def get_department_enter_noPass(id:int,days:int,db: Session = Depends(get_db)):
    try:
        data = admin_crud.get_all_student_enter_school_no_pass_of_department(id,days,db)
        return schemas.Response(data=data)
    except Exception as e:
        return schemas.Response(message=str(e), code=500)


@app.get("/department/enter/most", response_model=schemas.Response)
def get_department_enter_most(id:int,num:int,db: Session = Depends(get_db)):
    try:
        data = admin_crud.get_all_student_apply_for_enter_count_in_department(id,num,db)
        return schemas.Response(data=data)
    except Exception as e:
        return schemas.Response(message=str(e), code=500)


@app.get("/department/enter/most/class", response_model=schemas.Response)
def get_department_enter_most_class(id:int,num:int,db: Session = Depends(get_db)):
    try:
        data = admin_crud.get_all_student_apply_for_enter_count_in_class(id,num,db)
        return schemas.Response(data=data)
    except Exception as e:
        return schemas.Response(message=str(e), code=500)


@app.get("/department/leave/most", response_model=schemas.Response)
def get_department_leave_most(id:int,num:int,db: Session = Depends(get_db)):
    try:
        data = admin_crud.get_all_student_average_leave_time_in_department(id,num,db)
        return schemas.Response(data=data)
    except Exception as e:
        return schemas.Response(message=str(e), code=500)


@app.get("/department/leave/most/class", response_model=schemas.Response)
def get_department_leave_most_class(id:int,num:int,db: Session = Depends(get_db)):
    try:
        data = admin_crud.get_all_student_average_leave_time_in_class(id,num,db)
        return schemas.Response(data=data)
    except Exception as e:
        return schemas.Response(message=str(e), code=500)


@app.get("/department/leaving", response_model=schemas.Response)
def get_department_leaving(id:int,db: Session = Depends(get_db)):
    try:
        data = admin_crud.get_all_student_leave_school_info_of_department(id,db)
        return schemas.Response(data=data)
    except Exception as e:
        return schemas.Response(message=str(e), code=500)


@app.get("/department/leave/noApply", response_model=schemas.Response)
def get_department_leave_noApply(id:int,db: Session = Depends(get_db)):
    try:
        data = admin_crud.get_all_student_leave_school_more_than_one_day_info(id,db)
        return schemas.Response(data=data)
    except Exception as e:
        return schemas.Response(message=str(e), code=500)


@app.get("/department/apply/noLeave", response_model=schemas.Response)
def get_department_apply_noLeave(id:int,db: Session = Depends(get_db)):
    try:
        data = admin_crud.get_all_student_apply_for_leave_school_but_not_leave_school_info(id,db)
        return schemas.Response(data=data)
    except Exception as e:
        return schemas.Response(message=str(e), code=500)


@app.get("/department/stay", response_model=schemas.Response)
def get_department_stay(id:int,days:int,db: Session = Depends(get_db)):
    try:
        data = admin_crud.get_all_student_stay_in_school_more_than_n_days_info_in_department_level(id,days,db)
        return schemas.Response(data=data)
    except Exception as e:
        return schemas.Response(message=str(e), code=500)


@app.get("/department/stay/class", response_model=schemas.Response)
def get_department_stay_class(id:int,days:int,db: Session = Depends(get_db)):
    try:
        data = admin_crud.get_all_student_stay_in_school_more_than_n_days_info_in_class_level(id,days,db)
        return schemas.Response(data=data)
    except Exception as e:
        return schemas.Response(message=str(e), code=500)



@app.get("/department/same", response_model=schemas.Response)
def get_department_same(id:int,days:int,db: Session = Depends(get_db)):
    try:
        data = admin_crud.get_all_student_health_report_same_for_n_days_info_in_department_level(id,days,db)
        return schemas.Response(data=data)
    except Exception as e:
        return schemas.Response(message=str(e), code=500)


@app.get("/department/record/most", response_model=schemas.Response)
def get_department_record_most(id:int,days:int,db: Session = Depends(get_db)):
    try:
        data = admin_crud.get_most_in_out_campus_in_department(id,days,db)
        return schemas.Response(data=data)
    except Exception as e:
        return schemas.Response(message=str(e), code=500)


@app.get("/class/info", response_model=schemas.Response)
def get_class_info(id:int,days:int,db: Session = Depends(get_db)):
    try:
        data = counselor_crud.get_all_student_health_report_of_n_days_of_class(id,days,db)
        return schemas.Response(data=data)
    except Exception as e:
        return schemas.Response(message=str(e), code=500)


@app.get("/class/access", response_model=schemas.Response)
def get_class_access(id:int,db: Session = Depends(get_db)):
    try:
        data = counselor_crud.get_all_student_right_of_campus_of_class(id,db)
        return schemas.Response(data=data)
    except Exception as e:
        return schemas.Response(message=str(e), code=500)


@app.get("/class/leave", response_model=schemas.Response)
def get_class_leave(id:int,db: Session = Depends(get_db)):
    try:
        data = counselor_crud.get_all_student_leave_school_of_class(id,db)
        return schemas.Response(data=data)
    except Exception as e:
        return schemas.Response(message=str(e), code=500)


@app.get("/class/enter", response_model=schemas.Response)
def get_class_enter(id:int,db: Session = Depends(get_db)):
    try:
        data = counselor_crud.get_all_student_enter_school_of_class(id,db)
        return schemas.Response(data=data)
    except Exception as e:
        return schemas.Response(message=str(e), code=500)


@app.get("/class/leave/time", response_model=schemas.Response)
def get_class_leave_time(id:int,db: Session = Depends(get_db)):
    try:
        data = counselor_crud.get_all_student_leave_school_time_of_class(id,db)
        return schemas.Response(data=data)
    except Exception as e:
        return schemas.Response(message=str(e), code=500)


@app.get("/class/leave/noPass", response_model=schemas.Response)
def get_class_leave_noPass(id:int,days:int,db: Session = Depends(get_db)):
    try:
        data = counselor_crud.get_all_student_leave_school_no_pass_of_class(id,days,db)
        return schemas.Response(data=data)
    except Exception as e:
        return schemas.Response(message=str(e), code=500)


@app.get("/class/enter/noPass", response_model=schemas.Response)
def get_class_enter_noPass(id:int,days:int,db: Session = Depends(get_db)):
    try:
        data = counselor_crud.get_all_student_enter_school_no_pass_of_class(id,days,db)
        return schemas.Response(data=data)
    except Exception as e:
        return schemas.Response(message=str(e), code=500)


@app.get("/class/enter/most", response_model=schemas.Response)
def get_class_enter_most(id:int,num:int,db: Session = Depends(get_db)):
    try:
        data = counselor_crud.get_all_student_apply_for_enter_count_of_class(id,num,db)
        return schemas.Response(data=data)
    except Exception as e:
        return schemas.Response(message=str(e), code=500)


@app.get("/class/leave/most", response_model=schemas.Response)
def get_class_leave_most(id:int,num:int,db: Session = Depends(get_db)):
    try:
        data = counselor_crud.get_all_student_average_leave_time_of_class(id,num,db)
        return schemas.Response(data=data)
    except Exception as e:
        return schemas.Response(message=str(e), code=500)



@app.get("/class/leaving", response_model=schemas.Response)
def get_class_leaving(id:int,db: Session = Depends(get_db)):
    try:
        data = counselor_crud.get_all_student_leave_school_info_of_class(id,db)
        return schemas.Response(data=data)
    except Exception as e:
        return schemas.Response(message=str(e), code=500)


@app.get("/class/leave/noApply", response_model=schemas.Response)
def get_class_leave_noApply(id:int,db: Session = Depends(get_db)):
    try:
        data = counselor_crud.get_all_student_leave_school_more_than_one_day_info_of_class(id,db)
        return schemas.Response(data=data)
    except Exception as e:
        return schemas.Response(message=str(e), code=500)


@app.get("/class/apply/noLeave", response_model=schemas.Response)
def get_class_apply_noLeave(id:int,db: Session = Depends(get_db)):
    try:
        data = counselor_crud.get_all_student_apply_for_leave_school_but_not_leave_school_info_of_class(id,db)
        return schemas.Response(data=data)
    except Exception as e:
        return schemas.Response(message=str(e), code=500)


@app.get("/class/stay", response_model=schemas.Response)
def get_class_stay(id:int,days:int,db: Session = Depends(get_db)):
    try:
        data = counselor_crud.get_all_student_stay_in_school_more_than_n_days_info_in_class_level(id,days,db)
        return schemas.Response(data=data)
    except Exception as e:
        return schemas.Response(message=str(e), code=500)


@app.get("/class/same", response_model=schemas.Response)
def get_class_same(id:int,days:int,db: Session = Depends(get_db)):
    try:
        data = counselor_crud.get_all_student_health_report_same_for_n_days_info_of_class(id,days,db)
        return schemas.Response(data=data)
    except Exception as e:
        return schemas.Response(message=str(e), code=500)

@app.get("/class/other", response_model=schemas.Response)
def get_class_other(id:int,db: Session = Depends(get_db)):
    try:
        data = counselor_crud.get_other_class_statistics_info(id,db)
        return schemas.Response(data=data)
    except Exception as e:
        return schemas.Response(message=str(e), code=500)


@app.get("/class/other/noPass", response_model=schemas.Response)
def get_class_other_noPass(id:int,days:int,db: Session = Depends(get_db)):
    try:
        data = counselor_crud.get_other_class_enter_and_leave_apply(id,days,db)
        return schemas.Response(data=data)
    except Exception as e:
        return schemas.Response(message=str(e), code=500)


@app.get("/class/other/same", response_model=schemas.Response)
def get_class_other_same(id:int,days:int,db: Session = Depends(get_db)):
    try:
        data = counselor_crud.get_other_class_same_health_report(id,days,db)
        return schemas.Response(data=data)
    except Exception as e:
        return schemas.Response(message=str(e), code=500)


@app.get("/stu/info", response_model=schemas.Response)
def get_stu_info(id:int,db: Session = Depends(get_db)):
    try:
        data = student_crud.get_student_info(id,db)
        return schemas.Response(data=data)
    except Exception as e:
        return schemas.Response(message=str(e), code=500)


@app.get("/stu/health", response_model=schemas.Response)
def get_stu_health(id:int,days:int,db: Session = Depends(get_db)):
    try:
        data = student_crud.get_student_health_report_of_n_days(id,days,db)
        return schemas.Response(data=data)
    except Exception as e:
        return schemas.Response(message=str(e), code=500)



@app.get("/stu/leave", response_model=schemas.Response)
def get_stu_leave(id:int,db: Session = Depends(get_db)):
    try:
        data = student_crud.get_leave_campus_apply(id,db)
        return schemas.Response(data=data)
    except Exception as e:
        return schemas.Response(message=str(e), code=500)


@app.get("/stu/enter", response_model=schemas.Response)
def get_stu_enter(id:int,db: Session = Depends(get_db)):
    try:
        data = student_crud.get_enter_campus_apply(id,db)
        return schemas.Response(data=data)
    except Exception as e:
        return schemas.Response(message=str(e), code=500)


@app.get("/stu/other", response_model=schemas.Response)
def get_stu_other(id:int,db: Session = Depends(get_db)):
    try:
        data = student_crud.get_my_class_statistics_info(id,db)
        return schemas.Response(data=data)
    except Exception as e:
        return schemas.Response(message=str(e), code=500)


@app.get("/stu/class/noPass", response_model=schemas.Response)
def get_stu_class_noPass(id:int,days:int,db: Session = Depends(get_db)):
    try:
        data = student_crud.get_my_class_enter_and_leave_apply(id,days,db)
        return schemas.Response(data=data)
    except Exception as e:
        return schemas.Response(message=str(e), code=500)


@app.get("/stu/class/same", response_model=schemas.Response)
def get_stu_class_same(id:int,days:int,db: Session = Depends(get_db)):
    try:
        data = student_crud.get_my_class_same_health_report(id,days,db)
        return schemas.Response(data=data)
    except Exception as e:
        return schemas.Response(message=str(e), code=500)


@app.post("/stu/health/add", response_model=schemas.Response)
def add_stu_health(health:schemas.StudentHealthReportPost,db: Session = Depends(get_db)):
    try:
        student_crud.add_student_health_report(health,db)
        return schemas.Response()
    except Exception as e:
        return schemas.Response(message=str(e), code=500)


@app.post("/stu/enter/add", response_model=schemas.Response)
def add_stu_enter(enter:schemas.ApplyForEnterSchoolPost,db: Session = Depends(get_db)):
    try:
        student_crud.add_student_enter_apply(enter,db)
        return schemas.Response()
    except Exception as e:
        return schemas.Response(message=str(e), code=500)


@app.post("/stu/leave/add", response_model=schemas.Response)
def add_stu_leave(leave:schemas.ApplyForLeaveSchoolPost,db: Session = Depends(get_db)):
    try:
        student_crud.add_student_leave_apply(leave, db)
        return schemas.Response()
    except Exception as e:
        return schemas.Response(message=str(e), code=500)


@app.post("/stu/info/modify", response_model=schemas.Response)
def modify_stu_info(info:schemas.StudentInfo,db: Session = Depends(get_db)):
    try:
        student_crud.modify_student_info(info,db)
        return schemas.Response()
    except Exception as e:
        return schemas.Response(message=str(e), code=500)


@app.post("/class/handle", response_model=schemas.Response)
def handle_class_apply(apply:schemas.ApplyPost,db: Session = Depends(get_db)):
    try:
        counselor_crud.handle_class_apply(apply, db)
        return schemas.Response()
    except Exception as e:
        return schemas.Response(message=str(e), code=500)


@app.post("/department/handle", response_model=schemas.Response)
def handle_department_apply(apply:schemas.ApplyPost,db: Session = Depends(get_db)):
    try:
        admin_crud.handle_admin_apply(apply,db)
        return schemas.Response()
    except Exception as e:
        return schemas.Response(message=str(e), code=500)

