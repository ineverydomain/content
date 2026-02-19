from __future__ import annotations

import os
from pathlib import Path
from typing import Dict, List

from moviepy.editor import AudioFileClip, CompositeVideoClip, ImageClip, TextClip, concatenate_audioclips

from .common import OUTPUT_DIR


def assemble_video(background_image: str, audio_files: List[str], dialogue: List[Dict[str, str]]) -> str:
    if len(audio_files) != len(dialogue):
        raise ValueError("audio_files and dialogue lengths must match.")

    width = int(os.getenv("VIDEO_WIDTH", "1280"))
    height = int(os.getenv("VIDEO_HEIGHT", "720"))
    fps = int(os.getenv("VIDEO_FPS", "24"))

    audio_clips: List[AudioFileClip] = []
    subtitle_clips: List[TextClip] = []
    current_t = 0.0

    for idx, audio_path in enumerate(audio_files):
        clip = AudioFileClip(audio_path)
        audio_clips.append(clip)

        line = dialogue[idx]
        subtitle_text = f"{line['character']}: {line['line']}"
        subtitle = (
            TextClip(
                subtitle_text,
                fontsize=38,
                color="white",
                font="DejaVu-Sans",
                method="caption",
                size=(width - 80, None),
                stroke_color="black",
                stroke_width=2,
            )
            .set_start(current_t)
            .set_duration(clip.duration)
            .set_position(("center", height - 140))
        )
        subtitle_clips.append(subtitle)
        current_t += clip.duration + 0.3

    if not audio_clips:
        raise ValueError("No audio clips provided.")

    # Add silence between lines by inserting brief silent clips using volume-scaled base clips.
    spaced_audio: List[AudioFileClip] = []
    for i, clip in enumerate(audio_clips):
        spaced_audio.append(clip)
        if i < len(audio_clips) - 1:
            spaced_audio.append(clip.subclip(0, min(0.3, clip.duration)).volumex(0))

    final_audio = concatenate_audioclips(spaced_audio)

    background = ImageClip(background_image).set_duration(final_audio.duration).resize((width, height))
    final_video = CompositeVideoClip([background, *subtitle_clips]).set_audio(final_audio)

    output_path = Path(OUTPUT_DIR) / "final_video.mp4"
    final_video.write_videofile(str(output_path), codec="libx264", audio_codec="aac", fps=fps)

    for clip in audio_clips:
        clip.close()
    final_audio.close()
    final_video.close()

    return str(output_path)
