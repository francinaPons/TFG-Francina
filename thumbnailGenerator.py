from moviepy.editor import VideoFileClip
from checktype import checkType


def generate_thumbnail(name):
    path = "media/" + name
    nameWithoutExtension = name.split('.')[0]
    if checkType(name) == 'video':
        path = "media/" + name
        clip = VideoFileClip(path, audio=False)
        # getting only first 3 seconds
        clip = clip.subclip(0, 3)
        thumbnail_output = "thumbnails/" + nameWithoutExtension + ".png"
        clip.save_frame(thumbnail_output, t=clip.duration / 2)
    else:
        nameWithoutExtension = name.split('.')[0]
        thumbnail_output = "thumbnails/" + nameWithoutExtension + ".png"
