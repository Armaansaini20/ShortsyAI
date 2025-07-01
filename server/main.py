# main.py
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from gtts import gTTS
from moviepy.editor import VideoFileClip, AudioFileClip
import moviepy.video.fx.crop as crop_vid
import google.generativeai as genai
from dotenv import load_dotenv
import os
import random
from constant import gemini_key

load_dotenv()

app = FastAPI()

# Allow frontend access
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

@app.post("/generate")
async def generate_video(data: VideoRequest):
    title = data.title
    useAI = data.useAI.lower()

    # Create output directory
    if not os.path.exists("generated"):
        os.makedirs("generated")

    # Get content from Gemini or user
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

    # Convert text to speech
    tts = gTTS(text=content, lang='en', tld='ca', slow=False)
    speech_path = "generated/speech.mp3"
    tts.save(speech_path)

    audio_clip = AudioFileClip(speech_path)
    required_duration = audio_clip.duration + 1.3
    max_video_duration = 115  # gameplay_1.mp4 is 1.55 minutes

    if required_duration >= max_video_duration:
        return {"status": "error", "message": "Speech too long for fixed video."}

    # Load video and cut to match audio
    video_path = "gameplay/gameplay_1.mp4"
    try:
        video_clip = VideoFileClip(video_path)
    except Exception as e:
        return {"status": "error", "message": f"Error loading video: {str(e)}"}

    start_point = random.uniform(0, max_video_duration - required_duration)
    print(f"Cutting from {start_point} to {start_point + required_duration:.2f}")

    video_clip = video_clip.subclip(start_point, start_point + required_duration)
    final_clip = video_clip.set_audio(audio_clip)

    # Crop to 9:16 ratio
    w, h = final_clip.size
    target_ratio = 1080 / 1920
    current_ratio = w / h

    if current_ratio > target_ratio:
        new_width = int(h * target_ratio)
        final_clip = crop_vid.crop(final_clip, width=new_width, height=h, x_center=w / 2, y_center=h / 2)
    else:
        new_height = int(w / target_ratio)
        final_clip = crop_vid.crop(final_clip, width=w, height=new_height, x_center=w / 2, y_center=h / 2)

    # Export video
    out_path = f"generated/{title}.mp4"
    print(f"Exporting to {out_path}...")
    try:
        final_clip.write_videofile(
            out_path,
            codec="libx264",
            audio_codec="aac",  # Recommended with libx264
            temp_audiofile="temp-audio.m4a",
            remove_temp=True
        )
    except Exception as e:
        return {"status": "error", "message": f"Video export failed: {str(e)}"}

    return JSONResponse({
        "status": "success",
        "video_url": f"/generated/{title}.mp4"
    })
