"""
FastAPI backend for HLS Video Platform
Main application with all API endpoints
"""
import asyncio
import shutil
from pathlib import Path
from datetime import timedelta, datetime
from typing import List, Optional, Dict
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException, status, UploadFile, File, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete

from config import settings
from database import get_db, init_db
from models import User, Video
from schemas import (
    UserCreate, UserLogin, UserResponse, Token,
    VideoCreate, VideoResponse, ConversionRequest,
    ProgressResponse, ServerStatus
)
from auth import (
    get_password_hash, verify_password, create_access_token,
    get_current_active_user, get_optional_user
)
from ffmpeg_converter import FFmpegConverter

# Lifespan context manager for startup/shutdown events
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await init_db()
    print(f"✓ Database initialized")
    print(f"✓ Server starting on {settings.HOST}:{settings.PORT}")
    yield
    # Shutdown (cleanup if needed)
    print("✓ Server shutting down")

# Create FastAPI app
app = FastAPI(
    title="HLS Video Platform API",
    description="Backend API for video conversion and streaming platform",
    version="2.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Store for active conversions with thread safety
active_conversions: Dict[str, "FFmpegConverter"] = {}
conversions_lock = asyncio.Lock()

# WebSocket connections manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        disconnected = []
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception as e:
                print(f"WebSocket broadcast error: {e}")
                disconnected.append(connection)

        # Remove disconnected clients
        for conn in disconnected:
            try:
                self.active_connections.remove(conn)
            except ValueError:
                pass

manager = ConnectionManager()


# ==================== Authentication Endpoints ====================

@app.post("/api/auth/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):
    """Register a new user"""
    # Check if username exists
    result = await db.execute(select(User).where(User.username == user.username))
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Username already registered")

    # Check if email exists
    result = await db.execute(select(User).where(User.email == user.email))
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Email already registered")

    # Create new user
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=get_password_hash(user.password)
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)

    return db_user


@app.post("/api/auth/login", response_model=Token)
async def login(user: UserLogin, db: AsyncSession = Depends(get_db)):
    """Login and get access token"""
    result = await db.execute(select(User).where(User.username == user.username))
    db_user = result.scalar_one_or_none()

    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": db_user.username}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/api/auth/me", response_model=UserResponse)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    """Get current user info"""
    return current_user


# ==================== Video Management Endpoints ====================

@app.get("/api/videos", response_model=List[VideoResponse])
async def list_videos(
    db: AsyncSession = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_user)
):
    """List all videos (or user-specific if authenticated)"""
    if current_user:
        # Authenticated: show only user's videos
        result = await db.execute(
            select(Video)
            .where(Video.user_id == current_user.id)
            .order_by(Video.created_at.desc())
        )
    else:
        # Testing mode: show all videos
        result = await db.execute(select(Video).order_by(Video.created_at.desc()))

    videos = result.scalars().all()
    return videos


@app.get("/api/videos/{video_id}", response_model=VideoResponse)
async def get_video(
    video_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_user)
):
    """Get video by ID (with user ownership check if authenticated)"""
    if current_user:
        # Authenticated: check ownership
        result = await db.execute(
            select(Video)
            .where(Video.id == video_id)
            .where(Video.user_id == current_user.id)
        )
    else:
        # Testing mode: allow any video
        result = await db.execute(select(Video).where(Video.id == video_id))

    video = result.scalar_one_or_none()

    if not video:
        raise HTTPException(status_code=404, detail="Video not found")

    return video


@app.delete("/api/videos/{video_id}")
async def delete_video(
    video_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_user)
):
    """Delete a video (with ownership check if authenticated)"""
    if current_user:
        # Authenticated: check ownership
        result = await db.execute(
            select(Video)
            .where(Video.id == video_id)
            .where(Video.user_id == current_user.id)
        )
    else:
        # Testing mode: allow deleting any video
        result = await db.execute(select(Video).where(Video.id == video_id))

    video = result.scalar_one_or_none()

    if not video:
        raise HTTPException(status_code=404, detail="Video not found")

    # Delete output directory
    output_dir = settings.OUTPUT_DIR / video.name
    if output_dir.exists():
        shutil.rmtree(output_dir)

    # Delete from database
    await db.delete(video)
    await db.commit()

    return {"message": f"Video '{video.name}' deleted successfully"}


@app.post("/api/videos/upload")
async def upload_video(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_user)
):
    """Upload a video file (user-specific if authenticated)"""
    # Validate file type
    allowed_extensions = [".mp4", ".avi", ".mkv", ".mov", ".flv", ".wmv", ".webm"]
    file_ext = Path(file.filename).suffix.lower()

    if file_ext not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type. Allowed: {', '.join(allowed_extensions)}"
        )

    # Check file size (read in chunks to avoid memory issues)
    file_size = 0
    max_size = settings.MAX_UPLOAD_SIZE

    # Save file to input directory with size validation
    file_path = settings.INPUT_DIR / file.filename
    buffer = None

    try:
        buffer = open(file_path, "wb")
        while chunk := await file.read(8192):  # Read 8KB chunks
            file_size += len(chunk)
            if file_size > max_size:
                # Delete partial file
                raise HTTPException(
                    status_code=413,
                    detail=f"File too large. Maximum size: {max_size / (1024**3):.1f}GB"
                )
            buffer.write(chunk)
    except HTTPException:
        # Clean up partial file on size exceeded
        if buffer:
            buffer.close()
        file_path.unlink(missing_ok=True)
        raise
    except Exception as e:
        # Clean up on error
        if buffer:
            buffer.close()
        file_path.unlink(missing_ok=True)
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")
    finally:
        if buffer and not buffer.closed:
            buffer.close()

    return {
        "message": "File uploaded successfully",
        "filename": file.filename,
        "size": file_size,
        "path": str(file_path)
    }


# ==================== Conversion Endpoints ====================

@app.post("/api/convert")
async def convert_video(
    request: ConversionRequest,
    db: AsyncSession = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_user)
):
    """Start video conversion to HLS format (user-specific if authenticated)"""
    # Validate segment_duration
    if request.segment_duration < 1 or request.segment_duration > 30:
        raise HTTPException(
            status_code=400,
            detail="Segment duration must be between 1 and 30 seconds"
        )

    input_file = settings.INPUT_DIR / request.video_name

    if not input_file.exists():
        raise HTTPException(status_code=404, detail="Input video file not found")

    # Check if video already exists in database
    video_basename = input_file.stem
    if current_user:
        # Authenticated: check for user's video
        result = await db.execute(
            select(Video)
            .where(Video.name == video_basename)
            .where(Video.user_id == current_user.id)
        )
    else:
        # Testing mode: check by name only
        result = await db.execute(
            select(Video).where(Video.name == video_basename)
        )

    existing_video = result.scalar_one_or_none()

    if existing_video:
        # Update existing video
        db_video = existing_video
        db_video.status = "pending"
        db_video.progress = 0
        db_video.error_message = None
    else:
        # Create new video record
        db_video = Video(
            name=video_basename,
            original_filename=request.video_name,
            file_size=input_file.stat().st_size,
            segment_duration=request.segment_duration,
            status="pending",
            user_id=current_user.id if current_user else None
        )
        db.add(db_video)

    await db.commit()
    await db.refresh(db_video)

    # Start conversion in background
    output_dir = settings.OUTPUT_DIR / video_basename

    # Create watermark text (user-specific if authenticated, or IP address if not)
    watermark_text = None
    if current_user:
        # Authenticated user: use username and timestamp
        from datetime import datetime
        watermark_text = f"{current_user.username} | {datetime.utcnow().strftime('%Y-%m-%d %H:%M')}"
    else:
        # Testing mode: use a generic watermark with timestamp
        from datetime import datetime
        watermark_text = f"Video Platform | {datetime.utcnow().strftime('%Y-%m-%d %H:%M')}"

    converter = FFmpegConverter(input_file, output_dir, request.segment_duration, watermark_text)

    # Store converter for potential cancellation (thread-safe)
    async with conversions_lock:
        active_conversions[video_basename] = converter

    # Run conversion in background
    asyncio.create_task(run_conversion(converter, db_video.id))

    return {
        "message": f"Conversion started for '{request.video_name}'",
        "video_id": db_video.id,
        "video_name": video_basename
    }


async def run_conversion(converter: FFmpegConverter, video_id: int):
    """Background task to run video conversion"""
    success = await converter.convert()

    # Create new database session for background task
    from database import AsyncSessionLocal
    async with AsyncSessionLocal() as db:
        async with db.begin():
            result = await db.execute(select(Video).where(Video.id == video_id))
            video = result.scalar_one_or_none()

            if video:
                if success:
                    # Read final progress file
                    if converter.progress_file.exists():
                        import json
                        with open(converter.progress_file, "r") as f:
                            progress_data = json.load(f)

                        video.status = "completed"
                        video.progress = 100
                        video.segments = progress_data.get("segments")
                        video.output_size = progress_data.get("output_size")
                        video.duration = progress_data.get("duration")
                        video.playlist_path = f"output/{video.name}/playlist.m3u8"
                else:
                    video.status = "error"
                    video.error_message = "Conversion failed"

                await db.commit()

                # Remove from active conversions (thread-safe)
                if video and video.name in active_conversions:
                    async with conversions_lock:
                        if video.name in active_conversions:
                            del active_conversions[video.name]

                # Broadcast completion via WebSocket
                await manager.broadcast({
                    "type": "conversion_complete",
                    "video_id": video_id,
                    "status": video.status
                })


@app.get("/api/progress/{video_name}", response_model=ProgressResponse)
async def get_progress(video_name: str):
    """Get conversion progress for a video"""
    progress_file = settings.OUTPUT_DIR / video_name / ".progress.json"

    if not progress_file.exists():
        raise HTTPException(
            status_code=404,
            detail="No conversion in progress for this video"
        )

    try:
        import json
        with open(progress_file, "r") as f:
            progress_data = json.load(f)
        return progress_data
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Invalid progress file format")


@app.post("/api/convert/cancel/{video_name}")
async def cancel_conversion(
    video_name: str,
    current_user: Optional[User] = Depends(get_optional_user)
):
    """Cancel an active conversion (with ownership check if authenticated)"""
    async with conversions_lock:
        if video_name not in active_conversions:
            raise HTTPException(status_code=404, detail="No active conversion found")

        converter = active_conversions[video_name]
        await converter.cancel()

        del active_conversions[video_name]

    return {"message": f"Conversion cancelled for '{video_name}'"}


# ==================== Server Status Endpoints ====================

@app.get("/api/status", response_model=ServerStatus)
async def get_server_status(
    db: AsyncSession = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_user)
):
    """Get server status and statistics (user-specific if authenticated)"""
    if current_user:
        # Authenticated: show only user's stats
        result = await db.execute(
            select(Video).where(Video.user_id == current_user.id)
        )
        videos_count = len(result.scalars().all())

        # Calculate disk usage for user's videos only (memory efficient)
        total_size = 0
        user_videos = await db.execute(
            select(Video).where(Video.user_id == current_user.id)
        )
        for video in user_videos.scalars().all():
            video_dir = settings.OUTPUT_DIR / video.name
            if video_dir.exists():
                for f in video_dir.rglob("*"):
                    if f.is_file():
                        total_size += f.stat().st_size
    else:
        # Testing mode: show all stats
        result = await db.execute(select(Video))
        videos_count = len(result.scalars().all())

        # Calculate total disk usage (memory efficient)
        total_size = 0
        if settings.OUTPUT_DIR.exists():
            for f in settings.OUTPUT_DIR.rglob("*"):
                if f.is_file():
                    total_size += f.stat().st_size

    disk_usage = FFmpegConverter._format_size(total_size)

    return {
        "status": "running",
        "videos_count": videos_count,
        "disk_usage": disk_usage,
        "uptime": "N/A"  # Can be implemented with process start time
    }


@app.delete("/api/cleanup")
async def cleanup_all(
    db: AsyncSession = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_user)
):
    """Delete all videos (user-specific if authenticated, all if testing mode)"""
    if current_user:
        # Authenticated: delete only user's videos
        result = await db.execute(
            select(Video).where(Video.user_id == current_user.id)
        )
        user_videos = result.scalars().all()

        # Delete output directories for user's videos
        for video in user_videos:
            output_dir = settings.OUTPUT_DIR / video.name
            if output_dir.exists():
                shutil.rmtree(output_dir)

        # Delete all video records for this user
        await db.execute(delete(Video).where(Video.user_id == current_user.id))
        await db.commit()

        return {"message": "All your videos and output files deleted"}
    else:
        # Testing mode: delete all videos
        for item in settings.OUTPUT_DIR.iterdir():
            if item.is_dir():
                shutil.rmtree(item)

        # Delete all video records
        await db.execute(delete(Video))
        await db.commit()

        return {"message": "All videos and output files deleted"}


# ==================== WebSocket Endpoint ====================

@app.websocket("/ws/progress")
async def websocket_progress(websocket: WebSocket):
    """WebSocket endpoint for real-time progress updates"""
    await manager.connect(websocket)

    try:
        while True:
            # Keep connection alive and listen for client messages
            data = await websocket.receive_text()

            # Client can request specific video progress
            if data.startswith("subscribe:"):
                video_name = data.split(":")[1]
                progress_file = settings.OUTPUT_DIR / video_name / ".progress.json"

                if progress_file.exists():
                    import json
                    with open(progress_file, "r") as f:
                        progress_data = json.load(f)
                    await websocket.send_json(progress_data)

    except WebSocketDisconnect:
        manager.disconnect(websocket)


# ==================== Health Check ====================

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=True
    )
