import torch
import numpy as np
from diffusers import AutoencoderKLWan, WanImageToVideoPipeline
from diffusers.utils import export_to_video, load_image
from transformers import CLIPVisionModel

# Available models: Wan-AI/Wan2.1-I2V-14B-480P-Diffusers, Wan-AI/Wan2.1-I2V-14B-720P-Diffusers
model_id = "Wan-AI/Wan2.1-I2V-14B-720P-Diffusers"
image_encoder = CLIPVisionModel.from_pretrained(
    model_id, subfolder="image_encoder", torch_dtype=torch.float32
)
vae = AutoencoderKLWan.from_pretrained(model_id, subfolder="vae", torch_dtype=torch.float32)
pipe = WanImageToVideoPipeline.from_pretrained(
    model_id, vae=vae, image_encoder=image_encoder, torch_dtype=torch.bfloat16
)

# replace this with pipe.to("cuda") if you have sufficient VRAM
pipe.to("cuda")
# pipe.enable_model_cpu_offload()

# image = load_image("https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/diffusers/astronaut.jpg")

image_file_name = "girl-fire.png"
image_name = image_file_name.split(".")[0]
img_path = f"media/{image_file_name}"

image = load_image(
    img_path
)

max_area = 480 * 832
aspect_ratio = image.height / image.width
mod_value = pipe.vae_scale_factor_spatial * pipe.transformer.config.patch_size[1]
height = round(np.sqrt(max_area * aspect_ratio)) // mod_value * mod_value
width = round(np.sqrt(max_area / aspect_ratio)) // mod_value * mod_value
image = image.resize((width, height))


prompt = "A high-fashion Dolce & Gabbana commercial infused with the chaotic energy of the ‘Italian brain rot’ trend — sun-soaked Amalfi coast streets bursting with over-saturated colors, muscular men in gold chains dramatically eating spaghetti, grandmas shouting in Italian from balconies, Vespas doing wheelies through fountains. Cut to a surreal indoor fashion runway lined with marble statues of Roman emperors dabbing, models in exaggerated leopard-print suits and oversized sunglasses striking absurd poses. A giant floating mozzarella ball glows like the sun in the background. Operatic music mixed with Eurobeat blasts while text flashes in gaudy fonts: ‘MAMMA MIA, IT’S FASHION’. Final shot: a dramatic zoom on a model kissing a tomato while whispering, ‘Dolce far niente, baby.’ "
negative_prompt = "worst quality, inconsistent motion, blurry, jittery, distorted"

num_frames = 81

output = pipe(
    image=image,
    prompt=prompt,
    negative_prompt=negative_prompt,
    height=height,
    width=width,
    num_frames=num_frames,
    guidance_scale=5.0,
).frames[0]
export_to_video(output, "wan-i2v_201.mp4", fps=16)