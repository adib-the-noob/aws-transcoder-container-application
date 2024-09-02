import os 
import boto3

from fastapi import APIRouter, BackgroundTasks
from schemas.videoModel import VideoModel
from utils.video_utils import transcode_video
from utils.aws_utils import upload_folder_to_s3

router = APIRouter()

s3_client = boto3.client('s3')

@router.post('/download-s3-file')
def download_s3_file(
    video: VideoModel,
    background_tasks: BackgroundTasks
):
    file_uuid = video.key.split('__')[0]
    raw_dir = f'./media/{file_uuid}/raw/'

    
    os.makedirs(raw_dir, exist_ok=True)
    # os.makedirs(transcoded_dir, exist_ok=True)
    
    s3_client.download_file(video.bucket, video.key, f'./media/{file_uuid}/raw/{video.key}')
    
    background_tasks.add_task(
        transcode_video,
        # file_uuid=file_uuid,
        input_video=f'./media/{file_uuid}/raw/{video.key}',
        output_dir=f'./media/{file_uuid}/transcoded-{file_uuid}/'
    )
    background_tasks.add_task(
        upload_folder_to_s3,
        bucket='adib-hls-output-bucket',
        s3_prefix=f'videos/{file_uuid}/',
        folder_path=f'./media/{file_uuid}/transcoded-{file_uuid}/',
    )
    
    # remove the raw video file and output directory

    
    return {
        "message": "File downloaded successfully, transcoding in progress...",
    }