import torch
from diffusers.utils import load_video, export_to_video
from diffusers import AutoencoderKLWan, WanVideoToVideoPipeline, UniPCMultistepScheduler
import sys

# Available models: Wan-AI/Wan2.1-T2V-14B-Diffusers, Wan-AI/Wan2.1-T2V-1.3B-Diffusers
model_id = "Wan-AI/Wan2.1-T2V-1.3B-Diffusers"
vae = AutoencoderKLWan.from_pretrained(
    model_id, subfolder="vae", torch_dtype=torch.float32
)
pipe = WanVideoToVideoPipeline.from_pretrained(
    model_id, vae=vae, torch_dtype=torch.bfloat16
)
flow_shift = 3.0  # 5.0 for 720P, 3.0 for 480P
pipe.scheduler = UniPCMultistepScheduler.from_config(
    pipe.scheduler.config, flow_shift=flow_shift
)
# change to pipe.to("cuda") if you have sufficient VRAM
pipe.to("cuda")

prompt = "A promotional video of a cup of coffee with STARBUCKS logo and text on there."
prompt = "A promotional video for STARBUCKS with their logo and text on a cup of coffee which is the head of a women. Next to her, a man is located with a head made of chocolate. They are singing and happy. The video fades into the Starbucks Logo full screen with an advertisement for the products."
negative_prompt = "Bright tones, overexposed, static, blurred details, subtitles, style, works, paintings, images, static, overall gray, worst quality, low quality, JPEG compression residue, ugly, incomplete, extra fingers, poorly drawn hands, poorly drawn faces, deformed, disfigured, misshapen limbs, fused fingers, still picture, messy background, three legs, many people in the background, walking backwards"

video = load_video("media/brainrot_singing_short.mp4")

output = pipe(
    video=video,
    prompt=prompt,
    negative_prompt=negative_prompt,
    height=868,
    width=576,
    guidance_scale=3.0,
    strength=0.7,
    num_inference_steps=20
).frames[0]

export_to_video(output, "output/wan-v2v_portraitmode.mp4", fps=16)