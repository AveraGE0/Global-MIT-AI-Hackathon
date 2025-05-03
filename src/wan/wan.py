"""Module to create videos with WAN locally"""
import torch
from diffusers import AutoencoderKLWan, WanPipeline
from diffusers.utils import export_to_video


def generate_video(prompt: str, negative_prompt: str) -> str:
    """Function to generate a video locally, given prompt and negative prompt.

    Args:
        prompt (str): Generation prompt.
        negative_prompt (str): negative prompt.

    Returns:
        str: path to the video generated.
    """
    # Available models: Wan-AI/Wan2.1-T2V-14B-Diffusers, Wan-AI/Wan2.1-T2V-1.3B-Diffusers
    model_id = "Wan-AI/Wan2.1-T2V-14B-Diffusers"
    vae = AutoencoderKLWan.from_pretrained(model_id, subfolder="vae", torch_dtype=torch.float32)
    pipe = WanPipeline.from_pretrained(model_id, vae=vae, torch_dtype=torch.bfloat16)
    pipe.to("cuda")

    # with open("prompts.yaml", "r", encoding="utf-8") as file:
    #     prompts = yaml.safe_load(file)
    # prompt = prompts["brainrot_1"]
    # negative_prompt = prompts["negative_2"]

    output = pipe(
        prompt=prompt,
        negative_prompt=negative_prompt,
        height=832,
        width=480,
        num_frames=81,
        guidance_scale=3.0,
        num_videos_per_prompt=1
    ).frames[0]
    out_path = "data/generated_video.mp4"
    export_to_video(output, "data/generated_video.mp4", fps=16)
    return out_path
