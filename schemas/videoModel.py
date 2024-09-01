from pydantic import BaseModel

    # download file from and save it to a directory named "/{uuid}/raw/"
    # start transcoding using ffmpeg
    # multiscale - if 1080p then -> 720p, 480p, 360p - condition will run after checking resolution
    # save it to a "{uuid}/hls/{1080p} | {720p} | {480p} | {360p}/" 
    # run job for uploading every quality
    # made an api service for background progress checking..
     
class VideoModel(BaseModel):
    bucket: str
    key: str
    
    class Config:
        schema_extra = {
            "example": {
                "bucket": "adib-source-bucket",
                "key": "adib-blue.png"
            }
        }
