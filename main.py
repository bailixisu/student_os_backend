from fastapi import FastAPI, Depends

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


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/db")
def get_db_test(db: SessionLocal = Depends(get_db)):
    return crud.create_sort_memo(db, schemas.SortMemo(sortText="test", sort_icon_color=1, sort_background_color=1))


@app.put("/memo")
def put_memo(memo: schemas.Memo, db: SessionLocal = Depends(get_db)):
    return crud.create_memo(db, memo)


@app.get("/memo")
def get_memo(db: SessionLocal = Depends(get_db)):
    return crud.get_memos(db)


@app.get("/sort_memo")
def get_sort_memo(db: SessionLocal = Depends(get_db)):
    return crud.get_sort_memos(db)