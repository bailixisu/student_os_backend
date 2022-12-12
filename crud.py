from sqlalchemy.orm import Session

import models
import schemas


def get_memo(db: Session, memo_id: int):
    return db.query(models.Memo).filter(models.Memo.id == memo_id).first()


def get_memos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Memo).offset(skip).limit(limit).all()


def create_memo(db: Session, memo: schemas.Memo):
    db_memo = models.Memo(**memo.dict())
    db.add(db_memo)
    db.commit()
    db.refresh(db_memo)
    return db_memo


def get_sort_memo(db: Session, sort_memo_id: int):
    return db.query(models.SortMemo).filter(models.SortMemo.id == sort_memo_id).first()


def get_sort_memos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.SortMemo).offset(skip).limit(limit).all()


def create_sort_memo(db: Session, sort_memo: schemas.SortMemo):
    db_sort_memo = models.SortMemo(**sort_memo.dict())
    db.add(db_sort_memo)
    db.commit()
    db.refresh(db_sort_memo)
    return db_sort_memo

