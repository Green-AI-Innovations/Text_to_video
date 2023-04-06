
from fastapi import APIRouter
from fastapi import Request, File, UploadFile
from services.lazykhRenderFrame import drawer
import json

router = APIRouter(
    responses={404: {"description": "Not found"}},

)


@router.post('/renderFrame')
async def drawer(transcript: UploadFile = File(...), scheduleTable: UploadFile = File(...)):

    transcriptFile = await transcript.read()
    scheduleTableFile = await scheduleTable.read()
    transcriptFile = transcriptFile.decode('utf-8')
    scheduleTableFile = scheduleTableFile.decode('utf-8')


    drawer(transcriptFile, scheduleTableFile)
    return "video rendered"