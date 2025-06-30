# backend.py (FastAPI version)
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from dotenv import load_dotenv
import random
from gtts import gTTS
from moviepy.editor import VideoFileClip, AudioFileClip
import moviepy.video.fx.crop as crop_vid
import google.generativeai as genai
from constant import gemini_key

app = FastAPI()
load_dotenv()
app.mount("/generated", StaticFiles(directory="generated"), name="generated")
# CORS for local React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class VideoRequest(BaseModel):
    title: str
    useAI: str  # "yes" or "no"
    theme: str = ""
    content: str = ""

@app.post("/generate")
async def generate_video(data: VideoRequest):
    title = data.title
    useAI = data.useAI.lower()
    content = ""

    if useAI == 'yes':
        os.environ["GOOGLE_API_KEY"] = gemini_key
        genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
        model = genai.GenerativeModel('gemini-2.0-flash')

        response = model.generate_content(
            data.theme,
            generation_config=genai.types.GenerationConfig(
                max_output_tokens=1000,
                top_p=0.6,
                top_k=5,
                temperature=0.8
            )
        )

        content = title + response.text

    else:
        content = data.content

    if not os.path.exists('generated'):
        os.mkdir('generated')

    # Generate speech
    speech = gTTS(text=content, lang='en', tld='ca', slow=False)
    speech.save("generated/speech.mp3")

    # Select random video
    # gp = random.choice(["1", "2"])
    gp="1"
    audio_clip = AudioFileClip("generated/speech.mp3")
    video_path = f"gameplay/gameplay_{gp}.mp4"
    video_clip = VideoFileClip(video_path)

    video_duration = video_clip.duration
    required_duration = audio_clip.duration + 1.3

    if required_duration >= video_duration:
        return {"status": "error", "message": "Generated speech is too long for the selected video."}

# Choose a safe random start point
    start_point = random.uniform(0, video_duration - required_duration)

# Re-cut clip safely
    video_clip = video_clip.subclip(start_point, start_point + required_duration)
    final_clip = video_clip.set_audio(audio_clip)    

    if audio_clip.duration + 1.3 > 58:
        return {"status": "error", "message": "Speech too long."}

    video_clip = VideoFileClip(f"gameplay/gameplay_{gp}.mp4").subclip(
        start_point, start_point + audio_clip.duration + 1.3
    )
    final_clip = video_clip.set_audio(audio_clip)

    # Crop to 9:16
    w, h = final_clip.size
    target_ratio = 1080 / 1920
    current_ratio = w / h

    if current_ratio > target_ratio:
        new_width = int(h * target_ratio)
        final_clip = crop_vid.crop(
            final_clip, width=new_width, height=h,
            x_center=w / 2, y_center=h / 2
        )
    else:
        new_height = int(w / target_ratio)
        final_clip = crop_vid.crop(
            final_clip, width=w, height=new_height,
            x_center=w / 2, y_center=h / 2
        )

    out_path = f"generated/{title}.mp4"
    final_clip.write_videofile(
        out_path,
        codec='libx264',
        audio_codec='mp3',
        temp_audiofile='temp-audio.mp3',
        remove_temp=True
    )
    return JSONResponse({
    "status": "success",
    "video_url": f"/generated/{title}.mp4"
    })
