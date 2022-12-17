from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

import crud
import models
import schemas
from database import SessionLocal, engine
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
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
def root(db: Session = Depends(get_db)):
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
    data = crud.get_all_student_right_of_campus(db)
    return schemas.Response(data=data)
    # try:
    #
    # except Exception as e:
    #     return schemas.Response(message=str(e), code=500)

