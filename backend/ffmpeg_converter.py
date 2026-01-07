"""
FFmpeg video conversion module
Converts videos to HLS format with progress tracking
"""
import asyncio
import subprocess
import json
import re
from pathlib import Path
from typing import Optional, Dict, Any
from datetime import datetime


class FFmpegConverter:
    """Handle video conversion to HLS format using FFmpeg"""

    def __init__(self, input_file: Path, output_dir: Path, segment_duration: int = 6, watermark_text: Optional[str] = None):
        self.input_file = input_file
        self.output_dir = output_dir
        self.segment_duration = segment_duration
        self.watermark_text = watermark_text
        self.progress_file = output_dir / ".progress.json"
        self.log_file = output_dir / ".conversion.log"
        self.duration: Optional[float] = None
        self.process: Optional[asyncio.subprocess.Process] = None

    async def get_video_duration(self) -> float:
        """Get video duration using ffprobe"""
        cmd = [
            "ffprobe",
            "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            str(self.input_file)
        ]

        try:
            proc = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, _ = await proc.communicate()
            duration = float(stdout.decode().strip())
            return duration
        except (ValueError, subprocess.CalledProcessError):
            return 0.0

    async def update_progress(self, status: str, progress: int = 0, **kwargs):
        """Update progress JSON file"""
        progress_data = {
            "status": status,
            "progress": progress,
            "timestamp": datetime.utcnow().isoformat(),
            **kwargs
        }

        self.output_dir.mkdir(parents=True, exist_ok=True)
        with open(self.progress_file, "w") as f:
            json.dump(progress_data, f, indent=2)

    async def parse_ffmpeg_progress(self, line: str) -> Optional[Dict[str, Any]]:
        """Parse FFmpeg progress output"""
        if not self.duration or self.duration == 0:
            return None

        # Extract time (format: time=00:01:23.45)
        time_match = re.search(r"time=(\d{2}):(\d{2}):(\d{2})\.(\d{2})", line)
        if not time_match:
            return None

        hours, minutes, seconds, _ = map(int, time_match.groups())
        current_time = hours * 3600 + minutes * 60 + seconds

        # Calculate progress percentage
        progress = min(int((current_time / self.duration) * 100), 100)

        # Extract speed (format: speed=1.23x)
        speed = "0x"
        speed_match = re.search(r"speed=([0-9.]+)x", line)
        if speed_match:
            speed = f"{speed_match.group(1)}x"

        # Extract frame number
        frame = "0"
        frame_match = re.search(r"frame=\s*(\d+)", line)
        if frame_match:
            frame = frame_match.group(1)

        # Calculate ETA
        eta = "calculating..."
        if speed_match:
            speed_val = float(speed_match.group(1))
            if speed_val > 0:
                remaining = self.duration - current_time
                eta_seconds = int(remaining / speed_val)

                eta_hours = eta_seconds // 3600
                eta_minutes = (eta_seconds % 3600) // 60
                eta_secs = eta_seconds % 60

                if eta_hours > 0:
                    eta = f"{eta_hours}h {eta_minutes}m"
                elif eta_minutes > 0:
                    eta = f"{eta_minutes}m {eta_secs}s"
                else:
                    eta = f"{eta_secs}s"

        # Format time string
        current_hours = current_time // 3600
        current_minutes = (current_time % 3600) // 60
        current_secs = current_time % 60

        duration_hours = int(self.duration) // 3600
        duration_minutes = (int(self.duration) % 3600) // 60
        duration_secs = int(self.duration) % 60

        time_str = f"{current_hours:02d}:{current_minutes:02d}:{current_secs:02d} / {duration_hours:02d}:{duration_minutes:02d}:{duration_secs:02d}"

        return {
            "progress": progress,
            "current_time": current_time,
            "time_string": time_str,
            "frame": frame,
            "speed": speed,
            "eta": eta
        }

    async def convert(self) -> bool:
        """Convert video to HLS format with progress tracking"""
        try:
            # Get video duration
            await self.update_progress("initializing", 0, message="Analyzing video...")
            self.duration = await self.get_video_duration()

            if self.duration == 0:
                await self.update_progress("error", 0, message="Could not determine video duration")
                return False

            # Create output directory
            self.output_dir.mkdir(parents=True, exist_ok=True)

            # Build FFmpeg command with optional watermark
            cmd = ["ffmpeg", "-i", str(self.input_file)]

            # Add watermark filter if watermark text is provided
            if self.watermark_text:
                # Escape special characters in watermark text for FFmpeg
                # Replace colons with \: and escape single quotes
                escaped_text = self.watermark_text.replace(":", r"\:").replace("'", r"'\\\''")

                # Create watermark with semi-transparent text overlay
                # Position: bottom-right corner with 10px padding
                # Font size: 24, color: white with 50% opacity
                watermark_filter = (
                    f"drawtext=text='{escaped_text}':"
                    f"fontsize=24:"
                    f"fontcolor=white@0.5:"
                    f"x=w-tw-10:"
                    f"y=h-th-10:"
                    f"box=1:"
                    f"boxcolor=black@0.3:"
                    f"boxborderw=5"
                )
                cmd.extend(["-vf", watermark_filter])
                cmd.extend(["-c:v", "libx264"])
            else:
                cmd.extend(["-c:v", "libx264"])

            cmd.extend([
                "-c:a", "aac",
                "-start_number", "0",
                "-hls_time", str(self.segment_duration),
                "-hls_list_size", "0",
                "-hls_segment_filename", str(self.output_dir / "segment_%03d.ts"),
                "-f", "hls",
                "-progress", "pipe:1",
                str(self.output_dir / "playlist.m3u8")
            ])

            await self.update_progress("converting", 1, message="Starting encoding...", duration=int(self.duration))

            # Start FFmpeg process with proper file handle management
            log_file_handle = None
            try:
                log_file_handle = open(self.log_file, "w")
                self.process = await asyncio.create_subprocess_exec(
                    *cmd,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=log_file_handle
                )

                # Read progress output
                while True:
                    line = await self.process.stdout.readline()
                    if not line:
                        break

                    line_str = line.decode().strip()
                    progress_data = await self.parse_ffmpeg_progress(line_str)

                    if progress_data:
                        await self.update_progress(
                            "converting",
                            message="Encoding in progress...",
                            duration=int(self.duration),
                            **progress_data
                        )

                # Wait for process to complete
                await self.process.wait()
            finally:
                # Ensure log file is closed
                if log_file_handle is not None:
                    log_file_handle.close()

            # Check if conversion was successful
            if self.process.returncode == 0:
                # Count segments
                segments = len(list(self.output_dir.glob("segment_*.ts")))

                # Get output size
                total_size = sum(f.stat().st_size for f in self.output_dir.rglob("*") if f.is_file())
                output_size = self._format_size(total_size)

                await self.update_progress(
                    "completed",
                    100,
                    message="Conversion completed successfully!",
                    duration=int(self.duration),
                    segments=segments,
                    output_size=output_size
                )
                return True
            else:
                # Read error from log file
                error_msg = "Conversion failed"
                if self.log_file.exists():
                    with open(self.log_file, "r") as f:
                        lines = f.readlines()
                        error_msg = " ".join(lines[-5:]).strip()

                await self.update_progress(
                    "error",
                    0,
                    message="Conversion failed. Check log file for details.",
                    error=error_msg
                )
                return False

        except Exception as e:
            await self.update_progress(
                "error",
                0,
                message=f"Conversion error: {str(e)}",
                error=str(e)
            )
            return False

    @staticmethod
    def _format_size(size_bytes: int) -> str:
        """Format bytes to human-readable size"""
        for unit in ["B", "K", "M", "G", "T"]:
            if size_bytes < 1024.0:
                return f"{size_bytes:.1f}{unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.1f}P"

    async def cancel(self):
        """Cancel the conversion process"""
        if self.process:
            self.process.terminate()
            await self.process.wait()
            await self.update_progress("cancelled", 0, message="Conversion cancelled")
