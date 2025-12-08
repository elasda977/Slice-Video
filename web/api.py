#!/usr/bin/env python3
"""
Simple API server for HLS Video Platform management
Handles command execution and returns results
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import subprocess
import os
import urllib.parse

class APIHandler(BaseHTTPRequestHandler):

    def _set_headers(self, status=200, content_type='application/json'):
        self.send_response(status)
        self.send_header('Content-Type', content_type)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_OPTIONS(self):
        self._set_headers()

    def do_GET(self):
        """Handle GET requests for listing videos and status"""
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        if path == '/api/videos':
            self.list_videos()
        elif path == '/api/server-status':
            self.server_status()
        elif path == '/api/disk-usage':
            self.disk_usage()
        elif path.startswith('/api/progress/'):
            video_name = path.split('/')[-1]
            self.get_progress(video_name)
        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({'error': 'Not found'}).encode())

    def do_POST(self):
        """Handle POST requests for commands"""
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)

        try:
            data = json.loads(post_data.decode())
            command = data.get('command')

            if command == 'delete_video':
                self.delete_video(data.get('video'))
            elif command == 'clean_all':
                self.clean_all()
            elif command == 'convert_batch':
                self.convert_batch()
            elif command == 'convert_single':
                self.convert_single(data.get('video'), data.get('segment_duration', 6))
            elif command == 'server_restart':
                self.restart_server()
            else:
                self._set_headers(400)
                self.wfile.write(json.dumps({'error': 'Unknown command'}).encode())
        except Exception as e:
            self._set_headers(500)
            self.wfile.write(json.dumps({'error': str(e)}).encode())

    def list_videos(self):
        """List all converted videos"""
        try:
            output_dir = '/mnt/DATA/Project/video-segment-cutter/output'
            videos = []

            if os.path.exists(output_dir):
                for item in os.listdir(output_dir):
                    item_path = os.path.join(output_dir, item)
                    if os.path.isdir(item_path):
                        playlist = os.path.join(item_path, 'playlist.m3u8')
                        if os.path.exists(playlist):
                            # Count segments
                            segments = len([f for f in os.listdir(item_path) if f.endswith('.ts')])
                            # Get size
                            result = subprocess.run(['du', '-sh', item_path],
                                                  capture_output=True, text=True)
                            size = result.stdout.split()[0] if result.returncode == 0 else 'Unknown'

                            videos.append({
                                'name': item,
                                'segments': segments,
                                'size': size,
                                'path': f'output/{item}/playlist.m3u8'
                            })

            self._set_headers()
            self.wfile.write(json.dumps({'videos': videos}).encode())
        except Exception as e:
            self._set_headers(500)
            self.wfile.write(json.dumps({'error': str(e)}).encode())

    def server_status(self):
        """Check server status"""
        try:
            result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
            server_running = 'python.*8000' in result.stdout

            self._set_headers()
            self.wfile.write(json.dumps({
                'running': server_running,
                'output': result.stdout
            }).encode())
        except Exception as e:
            self._set_headers(500)
            self.wfile.write(json.dumps({'error': str(e)}).encode())

    def disk_usage(self):
        """Get disk usage information"""
        try:
            output_dir = '/mnt/DATA/Project/video-segment-cutter/output'
            result = subprocess.run(['du', '-sh', output_dir],
                                  capture_output=True, text=True)

            self._set_headers()
            self.wfile.write(json.dumps({
                'usage': result.stdout.strip(),
                'output': result.stdout
            }).encode())
        except Exception as e:
            self._set_headers(500)
            self.wfile.write(json.dumps({'error': str(e)}).encode())

    def delete_video(self, video_name):
        """Delete a specific video"""
        try:
            video_path = f'/mnt/DATA/Project/video-segment-cutter/output/{video_name}'

            if not os.path.exists(video_path):
                self._set_headers(404)
                self.wfile.write(json.dumps({'error': 'Video not found'}).encode())
                return

            result = subprocess.run(['rm', '-rf', video_path],
                                  capture_output=True, text=True)

            if result.returncode == 0:
                self._set_headers()
                self.wfile.write(json.dumps({
                    'success': True,
                    'message': f'Deleted {video_name}',
                    'output': f'Successfully deleted {video_path}'
                }).encode())
            else:
                self._set_headers(500)
                self.wfile.write(json.dumps({
                    'error': 'Failed to delete',
                    'output': result.stderr
                }).encode())
        except Exception as e:
            self._set_headers(500)
            self.wfile.write(json.dumps({'error': str(e)}).encode())

    def clean_all(self):
        """Clean all output files"""
        try:
            output_dir = '/mnt/DATA/Project/video-segment-cutter/output'
            # List what will be deleted
            items = [d for d in os.listdir(output_dir)
                    if os.path.isdir(os.path.join(output_dir, d))]

            result = subprocess.run(['rm', '-rf'] +
                                  [os.path.join(output_dir, item) for item in items],
                                  capture_output=True, text=True)

            self._set_headers()
            self.wfile.write(json.dumps({
                'success': True,
                'message': f'Deleted {len(items)} videos',
                'output': f'Cleaned: {", ".join(items)}'
            }).encode())
        except Exception as e:
            self._set_headers(500)
            self.wfile.write(json.dumps({'error': str(e)}).encode())

    def convert_batch(self):
        """Convert all videos in input folder"""
        try:
            input_dir = '/mnt/DATA/Project/video-segment-cutter/input'
            videos = [f for f in os.listdir(input_dir)
                     if f.endswith(('.mp4', '.avi', '.mkv', '.mov'))]

            if not videos:
                self._set_headers()
                self.wfile.write(json.dumps({
                    'success': False,
                    'message': 'No videos found in input folder',
                    'output': 'No videos to convert'
                }).encode())
                return

            output_lines = []
            for video in videos:
                script_path = '/mnt/DATA/Project/video-segment-cutter/scripts/convert-to-hls.sh'
                video_path = os.path.join(input_dir, video)

                result = subprocess.run([script_path, video_path, '6'],
                                      capture_output=True, text=True,
                                      timeout=600)
                output_lines.append(f"Converting {video}...")
                output_lines.append(result.stdout)
                if result.stderr:
                    output_lines.append(result.stderr)

            self._set_headers()
            self.wfile.write(json.dumps({
                'success': True,
                'message': f'Converted {len(videos)} videos',
                'output': '\n'.join(output_lines)
            }).encode())
        except Exception as e:
            self._set_headers(500)
            self.wfile.write(json.dumps({'error': str(e)}).encode())

    def restart_server(self):
        """Restart the web server"""
        try:
            # Kill existing server
            subprocess.run(['pkill', '-f', 'python.*8000'],
                         capture_output=True, text=True)

            # Start new server
            subprocess.Popen(['python', '-m', 'http.server', '8000', '--bind', '0.0.0.0'],
                           cwd='/mnt/DATA/Project/video-segment-cutter/web',
                           stdout=subprocess.DEVNULL,
                           stderr=subprocess.DEVNULL)

            self._set_headers()
            self.wfile.write(json.dumps({
                'success': True,
                'message': 'Server restarted',
                'output': 'Web server has been restarted on port 8000'
            }).encode())
        except Exception as e:
            self._set_headers(500)
            self.wfile.write(json.dumps({'error': str(e)}).encode())

    def get_progress(self, video_name):
        """Get conversion progress for a specific video"""
        try:
            progress_file = f'/mnt/DATA/Project/video-segment-cutter/output/{video_name}/.progress.json'

            if not os.path.exists(progress_file):
                self._set_headers(404)
                self.wfile.write(json.dumps({
                    'status': 'not_found',
                    'message': 'No conversion in progress for this video'
                }).encode())
                return

            # Read progress file
            with open(progress_file, 'r') as f:
                progress_data = json.load(f)

            self._set_headers()
            self.wfile.write(json.dumps(progress_data).encode())
        except json.JSONDecodeError:
            self._set_headers(500)
            self.wfile.write(json.dumps({
                'status': 'error',
                'message': 'Invalid progress file format'
            }).encode())
        except Exception as e:
            self._set_headers(500)
            self.wfile.write(json.dumps({'error': str(e)}).encode())

    def convert_single(self, video_name, segment_duration=6):
        """Convert a single video with progress tracking"""
        try:
            input_dir = '/mnt/DATA/Project/video-segment-cutter/input'
            video_path = os.path.join(input_dir, video_name)

            if not os.path.exists(video_path):
                self._set_headers(404)
                self.wfile.write(json.dumps({
                    'error': 'Video file not found in input directory'
                }).encode())
                return

            script_path = '/mnt/DATA/Project/video-segment-cutter/scripts/convert-to-hls-progress.sh'

            # Start conversion in background
            process = subprocess.Popen(
                [script_path, video_path, str(segment_duration)],
                cwd='/mnt/DATA/Project/video-segment-cutter/scripts',
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )

            # Get video name without extension for tracking
            basename = os.path.splitext(video_name)[0]

            self._set_headers()
            self.wfile.write(json.dumps({
                'success': True,
                'message': f'Conversion started for {video_name}',
                'video_id': basename,
                'pid': process.pid
            }).encode())
        except Exception as e:
            self._set_headers(500)
            self.wfile.write(json.dumps({'error': str(e)}).encode())

    def log_message(self, format, *args):
        """Suppress log messages"""
        pass

def run_api_server(port=8001):
    """Run the API server"""
    server_address = ('', port)
    httpd = HTTPServer(server_address, APIHandler)
    print(f'API Server running on port {port}...')
    httpd.serve_forever()

if __name__ == '__main__':
    run_api_server()
