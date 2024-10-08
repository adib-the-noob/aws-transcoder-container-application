import os 
import boto3

from fastapi import APIRouter, BackgroundTasks
from schemas.videoModel import VideoModel
from utils.video_utils import transcode_video
from utils.aws_utils import upload_folder_to_s3

from dotenv import load_dotenv
load_dotenv()

AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')

router = APIRouter()

s3_client = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)

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
     
     
    return {
        "message": "File downloaded successfully, transcoding in progress...",
    }