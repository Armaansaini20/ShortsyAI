from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
import moviepy.config as mpy_config

# ✅ Set ImageMagick path if needed (adjust path to your ImageMagick install)
mpy_config.change_settings({
    "IMAGEMAGICK_BINARY": r"C:\Program Files\ImageMagick-7.1.1-Q16-HDRI\magick.exe"
})

# ✅ Load video
video = VideoFileClip("gameplay/gameplay_1.mp4").subclip(0, 5)  # 5 sec test

# ✅ Define test subtitles (timestamped)
subtitles = [
    {"word": "Hello", "start": 0.5, "end": 1.5},
    {"word": "Subtitle", "start": 2.0, "end": 3.0},
    {"word": "Test", "start": 3.5, "end": 4.5},
]

# ✅ Create subtitle clips
subtitle_clips = []
for s in subtitles:
    txt = TextClip(
        txt=s["word"],
        fontsize=70,
        font="DejaVu-Sans",  # or Arial if installed
        color="red",
        stroke_color="white",
        stroke_width=3,
        method="caption"
    ).set_start(s["start"]).set_end(s["end"]).set_position(("center", "top"))
    
    subtitle_clips.append(txt)

# ✅ Combine video + subtitles
final = CompositeVideoClip([video] + subtitle_clips)

# ✅ Export
final.write_videofile("test_output_with_top_subtitles.mp4", fps=30)
