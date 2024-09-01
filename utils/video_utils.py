import subprocess
import os

def transcode_video(
    file_uuid: str,
    input_video: str,
    output_dir: str
):
    # Define the resolutions you want to transcode to
    # check video resolution
    command = [
        'ffprobe',
        '-v', 'error',
        '-select_streams', 'v:0',
        '-show_entries', 'stream=width,height',
        '-of', 'csv=s=x:p=0',
        input_video
    ]
    result = subprocess.run(command, stdout=subprocess.PIPE)
    width, height = result.stdout.decode().strip().split('x')
    
    if int(width) < 1280 or int(height) < 720:
        resolutions = {
            "720p": "1280x720",
            "480p": "854x480",
            "360p": "640x360",
        }
    resolutions = {
        "1080p": "1920x1080",
        "720p": "1280x720",
        "480p": "854x480",
        "360p": "640x360",
    }
        
    # Ensure the output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Loop through each resolution and create a transcoded video
    for label, resolution in resolutions.items():
        output_video = os.path.join(output_dir, f"{label}__{file_uuid}.mp4")
        command = [
            'ffmpeg',
            '-i', input_video,             # Input video file
            '-vf', f'scale={resolution}',  # Video filter for scaling
            '-c:a', 'copy',                # Copy the audio without re-encoding
            '-strict', '-2',               # Allow experimental codecs (optional)
            output_video                   # Output video file
        ]
        
        # Run the ffmpeg command
        subprocess.run(command)

    return {
        "message": "Video transcoded successfully",
        "output_dir": output_dir
    }

# if __name__ == "__main__":
#     input_video = 'input.mp4'  # Path to your input video
#     output_dir = 'output_videos'  # Directory to save the transcoded videos
#     transcode_video(input_video, output_dir)
