from fastapi import APIRouter, Depends, Query
from elasticsearch import Elasticsearch
from sqlalchemy.orm import Session
from database import get_db
from typing import List, Optional
from models import Video

router = APIRouter()


@router.get("/search")
def search(
        db: Session = Depends(get_db),
        query: str = Query(..., description="Search query"),
        cursor: Optional[int] = Query(None, description="Cursor for pagination"),
        page_size: int = 10):
    
    query = db.query(Video).filter(
        (Video.title.ilike(f'%{query}%')) |
        (Video.description.ilike(f'%{query}%'))
    ).order_by(Video.published_at.desc())

    if cursor:
        query = query.filter(Video.id < cursor)

    videos = query.limit(page_size).all()

    next_cursor = None
    if len(videos) == page_size:
        next_cursor = videos[-1].id

    return {"videos": videos, "next_cursor": next_cursor}

# es = Elasticsearch()
# @router.get("/elastic_search")
# def elastic_search(db: Session = Depends(get_db), query: str = None, cursor: int = None, page_size: int = 10):
#     videos = db.execute(
#         f"SELECT * FROM videos WHERE title LIKE '%{
#             query}%' OR description LIKE '%{query}%'"
#     ).fetchall()

#     next_cursor = None
#     if len(videos) == page_size:
#         next_cursor = videos[-1].id

#     return {"videos": videos, "next_cursor": next_cursor}
