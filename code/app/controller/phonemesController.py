from fastapi import APIRouter
from fastapi import Request, File, UploadFile
from services.phonemes import get_phonemes


router = APIRouter(
    responses={404: {"description": "Not found"}},

)



@router.post('/phonemes')
async def create_phonemes(request: Request, mp3Audio: UploadFile = File(...), textFile: UploadFile = File(...)):
    # execution time is 15.12s
    mp3Audio = await mp3Audio.read()
    textFile = await textFile.read()

    # Do some processing with contents1 and contents2 to generate the text output
    phonemes = get_phonemes(mp3Audio, textFile)

    # Return the phonemes
    return {"phonemes": phonemes}