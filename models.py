from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class Memo(Base):
    __tablename__ = "memo"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String(100))
    start_time = Column(String(100))
    deadline = Column(String(100))
    complete_time = Column(String(100))
    note = Column(String(100))
    sort = Column(String(100))
    color = Column(Integer)
    status = Column(Integer)
    like = Column(Integer)
    circulate = Column(Integer)

    def __repr__(self):
        return f"Memo(id='{self.id}', content='{self.content}', start_time='{self.start_time}', deadline='{self.deadline}', complete_time='{self.complete_time}', note='{self.note}', sort='{self.sort}', color='{self.color}', status='{self.status}', like='{self.like}', circulate='{self.circulate}')"
    # items = relationship("Item", back_populates="owner")


class SortMemo(Base):
    __tablename__ = "sort_memo"

    sortText = Column(String(100), primary_key=True, index=True)
    sort_icon_color = Column(Integer, index=True)
    sort_background_color = Column(Integer, index=True)

    def __repr__(self):
        return f"SortMemo(sortText='{self.sortText}', sort_icon_color='{self.sort_icon_color}', sort_background_color='{self.sort_background_color}')"

    # owner = relationship("User", back_populates="items")
