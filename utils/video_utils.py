import os
import subprocess


def transcode_video(
    input_video: str,
    output_dir: str
):
    
    resolutions = {
            "1080p": {"resolution": "1920x1080", "bitrate": 5000000},  # 5 Mbps
            "720p": {"resolution": "1280x720", "bitrate": 2800000},    # 2.8 Mbps
            "480p": {"resolution": "854x480", "bitrate": 1400000},     # 1.4 Mbps
            "360p": {"resolution": "640x360", "bitrate": 800000},      # 800 Kbps
        }

    # Ensure output directories exist
    os.makedirs(output_dir, exist_ok=True)
    
    master_playlist_path = os.path.join(output_dir, "master.m3u8")
    
    hls_commands = []
    for label, settings in resolutions.items():
        resolution = settings["resolution"]
        bitrate = settings["bitrate"]
        
        resolution_output_dir = os.path.join(output_dir, label)
        os.makedirs(resolution_output_dir, exist_ok=True)
        
        # Define HLS segment files
        hls_command = [
            'ffmpeg',
            '-i', input_video,            # Input video file
            '-vf', f'scale={resolution}', # Scale video
            '-c:a', 'aac',                # Audio codec
            '-b:a', '128k',               # Audio bitrate
            '-c:v', 'h264',               # Video codec
            '-b:v', f'{bitrate}',         # Video bitrate based on resolution (no 'k' suffix)
            '-f', 'hls',                  # Output format
            '-hls_time', '10',            # Segment duration
            '-hls_list_size', '0',        # Unlimited playlist length
            '-hls_segment_filename', f'{resolution_output_dir}/%03d.ts', # Segment file naming
            f'{resolution_output_dir}/playlist.m3u8' # Output playlist file
        ]
        
        hls_commands.append(hls_command)
    
    # Run all transcoding commands
    for cmd in hls_commands:
        subprocess.run(cmd, check=True)

    # Generate master playlist file
    with open(master_playlist_path, 'w') as master_file:
        master_file.write("#EXTM3U\n")  # Master playlist header
        for label, settings in resolutions.items():
            resolution = settings["resolution"]
            bitrate = settings["bitrate"]
            playlist_path = os.path.join(output_dir, label, 'playlist.m3u8')
            master_file.write(f"#EXT-X-STREAM-INF:BANDWIDTH={bitrate},RESOLUTION={resolution}\n")
            master_file.write(f"{label}/playlist.m3u8\n")

