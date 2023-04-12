from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fairseq.checkpoint_utils import load_model_ensemble_and_task_from_hf_hub
from fairseq.models.text_to_speech.hub_interface import TTSHubInterface
import IPython.display as ipd

#cors
from fastapi.middleware.cors import CORSMiddleware

# Return voice in correct format
import base64
import io
from starlette.responses import JSONResponse
import torchaudio
from fastapi.responses import StreamingResponse


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class VoiceRequest(BaseModel):
    text: str

class AudioResponse(BaseModel):
    audio_data: str
    sample_rate: int


def generate_audio(request: VoiceRequest):

    models, cfg, task = load_model_ensemble_and_task_from_hf_hub(
        "facebook/fastspeech2-en-ljspeech",
        arg_overrides={"vocoder": "hifigan", "fp16": False}
    )
    model = models[0]
    TTSHubInterface.update_cfg_with_data_cfg(cfg, task.data_cfg)
    generator = task.build_generator([model], cfg)
    # text = "career day was not very fun"
    text = request.text

    sample = TTSHubInterface.get_model_input(task, text)
    wav, rate = TTSHubInterface.get_prediction(task, model, generator, sample)
    return wav, rate


@app.post("/GenerateVoice")
def get_audio(request: VoiceRequest):
    try:
        wav, rate = generate_audio(request)
        audio_buffer = io.BytesIO()

        # Add a singleton dimension to the tensor to make it 2D
        wav_2d = wav.unsqueeze(0)

        # Convert the Tensor to a WAV file and write it to the buffer
        torchaudio.save(audio_buffer, wav_2d, sample_rate=rate, channels_first=True, format='wav', encoding='PCM_S', bits_per_sample=16)
        audio_buffer.seek(0)

        return StreamingResponse(audio_buffer, media_type='audio/wav')

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))