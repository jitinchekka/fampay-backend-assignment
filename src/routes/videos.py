from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from models import Video
from database import get_db
from datetime import datetime
from typing import Union

router = APIRouter()

class VideoResponse(BaseModel):
    id: int
    video_id: str
    title: str
    description: str
    published_at: datetime
    thumbnails: str

    class Config:
        from_attributes = True

@router.get("/videos", response_model=dict[str, Union[List[VideoResponse], Optional[int]]])
def get_videos(
    db: Session = Depends(get_db),
    cursor: Optional[int] = None,
    page_size: int = 10
):
    query = db.query(Video).order_by(Video.published_at.desc())
    
    if cursor:
        # For timestamp-based pagination
        last_video = db.query(Video).filter(Video.id == cursor).first()
        if last_video:
            query = query.filter(Video.published_at < last_video.published_at)
    
    # Add 1 to page_size to check if there are more results
    videos = query.limit(page_size + 1).all()
    
    has_more = len(videos) > page_size
    if has_more:
        videos = videos[:-1]  # Remove the extra item
    
    next_cursor = videos[-1].id if has_more else None
    
    return {
        "videos": videos,
        "next_cursor": next_cursor
    }