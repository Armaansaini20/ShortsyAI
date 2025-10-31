from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from moviepy.editor import VideoFileClip, AudioFileClip
import moviepy.video.fx.crop as crop_vid
import google.generativeai as genai
from dotenv import load_dotenv
import os
import random
from constant import gemini_key, eleven_key
from elevenlabs.client import ElevenLabs

load_dotenv()

app = FastAPI()

# CORS middleware for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve generated videos
app.mount("/generated", StaticFiles(directory="generated"), name="generated")

class VideoRequest(BaseModel):
    title: str
    useAI: str  # "yes" or "no"
    theme: str = ""
    content: str = ""

# 🔊 ElevenLabs speech generation
def generate_elevenlabs_speech(text: str, output_path: str):
    client = ElevenLabs(api_key=eleven_key)

    audio_generator = client.text_to_speech.convert(
        text=text,
        voice_id="JBFqnCBsd6RMkjVDRZzb",
        model_id="eleven_multilingual_v2",
        output_format="mp3_44100_128",
    )

    with open(output_path, "wb") as f:
        for chunk in audio_generator:
            f.write(chunk)


@app.post("/generate")
async def generate_video(data: VideoRequest):
    title = data.title.strip().replace(" ", "_")  # filename safe
    useAI = data.useAI.lower()

    # Step 1: Content generation
    if useAI == 'yes':
        os.environ["GOOGLE_API_KEY"] = gemini_key
        genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
        model = genai.GenerativeModel("gemini-2.0-flash")
        response = model.generate_content(
            data.theme,
            generation_config=genai.types.GenerationConfig(
                max_output_tokens=1000,
                top_p=0.6,
                top_k=5,
                temperature=0.8,
            )
        )
        content = title + response.text
    else:
        content = data.content

    # Step 2: Speech generation
    os.makedirs("generated", exist_ok=True)
    speech_path = f"generated/speech.mp3"

    try:
        generate_elevenlabs_speech(content, speech_path)
    except Exception as e:
        return JSONResponse({"status": "error", "message": f"TTS failed: {str(e)}"})

    # Step 3: Video preparation
    try:
        audio_clip = AudioFileClip(speech_path)
        video_clip = VideoFileClip("gameplay/gameplay_1.mp4")
    except Exception as e:
        return JSONResponse({"status": "error", "message": f"File error: {str(e)}"})

    required_duration = audio_clip.duration + 1.3
    max_video_duration = 115  # 1.55 minutes

    if required_duration >= max_video_duration:
        return JSONResponse({"status": "error", "message": "Speech too long for available video"})

    start = random.uniform(0, max_video_duration - required_duration)
    video_clip = video_clip.subclip(start, start + required_duration).set_audio(audio_clip)

    # Step 4: Crop to 9:16
    w, h = video_clip.size
    target_ratio = 1080 / 1920
    current_ratio = w / h

    if current_ratio > target_ratio:
        new_width = int(h * target_ratio)
        video_clip = crop_vid.crop(video_clip, width=new_width, height=h, x_center=w / 2, y_center=h / 2)
    else:
        new_height = int(w / target_ratio)
        video_clip = crop_vid.crop(video_clip, width=w, height=new_height, x_center=w / 2, y_center=h / 2)

    # Step 5: Export
    out_path = f"generated/{title}.mp4"
    try:
        video_clip.write_videofile(
            out_path,
            codec="libx264",
            audio_codec="aac",
            temp_audiofile="temp-audio.m4a",
            remove_temp=True,
            threads=4,
            fps=30
        )
    except Exception as e:
        return JSONResponse({"status": "error", "message": f"Video export failed: {str(e)}"})

    return JSONResponse({
        "status": "success",
        "video_url": f"/generated/{title}.mp4"
    })
