import moviepy.config as mpy_config
mpy_config.change_settings({
    "IMAGEMAGICK_BINARY": r"C:\Program Files\ImageMagick-7.1.1-Q16-HDRI\magick.exe"
})

from moviepy.editor import TextClip

clip = TextClip("Hello World", fontsize=70, color='white')
clip = clip.set_duration(5)
clip.write_videofile("test_textclip.mp4", fps=24)
