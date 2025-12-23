"""
Database models for the video platform
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey
from sqlalchemy.sql import func
from database import Base


class User(Base):
    """User model for authentication"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Video(Base):
    """Video model for storing video metadata"""
    __tablename__ = "videos"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    original_filename = Column(String, nullable=False)
    file_size = Column(Integer)  # in bytes
    duration = Column(Float)  # in seconds
    segments = Column(Integer)  # number of HLS segments
    segment_duration = Column(Integer, default=6)  # segment duration in seconds
    output_size = Column(String)  # human-readable size (e.g., "125M")
    status = Column(String, default="pending")  # pending, converting, completed, error
    progress = Column(Integer, default=0)  # 0-100
    error_message = Column(String, nullable=True)
    playlist_path = Column(String)  # path to .m3u8 file
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
