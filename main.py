from __future__ import annotations

import argparse

from pipeline.dialogue_writer import write_dialogue
from pipeline.image_generator import generate_background
from pipeline.scene_analyzer import analyze_scene
from pipeline.tts_generator import generate_audio
from pipeline.video_assembler import assemble_video


def run_pipeline(scene_text: str) -> str:
    print("Step 1: Analyzing scene...")
    scene_data = analyze_scene(scene_text)

    print("Step 2: Writing dialogue...")
    dialogue = write_dialogue(scene_data)

    print("Step 3: Generating background image...")
    bg_image_path = generate_background(scene_data["setting"])

    print("Step 4: Generating character audio...")
    audio_files = generate_audio(dialogue, scene_data["characters"])

    print("Step 5: Assembling video...")
    video_path = assemble_video(bg_image_path, audio_files, dialogue)

    print(f"✅ Done! Video saved to: {video_path}")
    return video_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate a short scene-to-video MP4 from text.")
    parser.add_argument("scene_text", type=str, help="A short scene description.")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    run_pipeline(args.scene_text)
