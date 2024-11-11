from sqlalchemy import Integer, String, DateTime, Float, PrimaryKeyConstraint
from datetime import datetime
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

class Base(DeclarativeBase):
    pass

class RecommendationSimilarBoard(Base):
    
    __tablename__ = 'recommendation_similar_board'

    query_item : Mapped[int] = mapped_column(Integer, primary_key=True)
    recommendation_item : Mapped[int] = mapped_column(Integer, primary_key=True)
    score : Mapped[float] = mapped_column(Float)
    rank : Mapped[int] = mapped_column(Integer)
    recommendation_theme : Mapped[str] = mapped_column(String)
    model_version : Mapped[str] = mapped_column(String)
    created_at : Mapped[datetime] = mapped_column(DateTime)
    modified_at : Mapped[datetime] = mapped_column(DateTime)

    __table_args__ = {
        PrimaryKeyConstraint('query_item', 'recommendation_item')
        }