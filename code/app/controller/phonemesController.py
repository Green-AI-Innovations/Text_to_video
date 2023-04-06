from fastapi import APIRouter
from fastapi import Request
from services.phonemes import get_phonemes


router = APIRouter(
    responses={404: {"description": "Not found"}},

)



@router.post('/phonemes')
def create_phonemes(request: Request):
    mp3Audio = request.files['mp3Audio']
    textFile = request.files['textFile']

    # Do some processing with mp3Audio and textFile to generate the text output
    phonemes=get_phonemes(mp3Audio,textFile)

    # Return the phonemes
    return phonemes