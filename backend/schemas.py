"""
Pydantic schemas for request/response validation
"""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


# User schemas (not used with auth disabled, but kept for compatibility)
class UserCreate(BaseModel):
    username: str
    email: str
    password: str


class UserLogin(BaseModel):
    username: str
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


# Video schemas
class VideoCreate(BaseModel):
    name: str
    original_filename: str
    segment_duration: int = 6


class VideoResponse(BaseModel):
    id: int
    name: str
    original_filename: str
    file_size: Optional[int]
    duration: Optional[float]
    segments: Optional[int]
    segment_duration: int
    output_size: Optional[str]
    status: str
    progress: int
    error_message: Optional[str]
    playlist_path: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True


class ConversionRequest(BaseModel):
    video_name: str
    segment_duration: int = 6


class ProgressResponse(BaseModel):
    status: str
    progress: int
    message: Optional[str] = None
    duration: Optional[int] = None
    current_time: Optional[int] = None
    time_string: Optional[str] = None
    frame: Optional[str] = None
    speed: Optional[str] = None
    eta: Optional[str] = None
    segments: Optional[int] = None
    output_size: Optional[str] = None
    error: Optional[str] = None
    timestamp: Optional[str] = None


class ServerStatus(BaseModel):
    status: str
    videos_count: int
    disk_usage: str
    uptime: str
