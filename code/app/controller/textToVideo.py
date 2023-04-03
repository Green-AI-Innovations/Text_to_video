from fastapi import APIRouter
from fastapi.responses import PlainTextResponse
from fastapi import Request
from services.createVideo import create_video_from_text

router = APIRouter(
    responses={404: {"description": "Not found"}},

)



@router.post("/text2video")
async def create_video(request: Request):
    body = await request.body()
    transcript = body.decode("utf-8")
    # process the text and create video
    video= create_video_from_text(transcript)
    print(video)
    return  video