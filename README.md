# ComfyUI Workflows

Beginner workflows. Drag a JSON file onto the canvas.

## MOSS Image

[workflow_moss_image_sft.json](MOSS%20Image/workflow_moss_image_sft.json)

- [moss_image_sft_int8_convrot.safetensors](https://huggingface.co/Comfy-Org/MOSS-Image/blob/main/diffusion_models/moss_image_sft_int8_convrot.safetensors)
- [qwen3.5_9b_w4a8_gptq.safetensors](https://huggingface.co/Comfy-Org/MOSS-Image/blob/main/text_encoders/qwen3.5_9b_w4a8_gptq.safetensors)
- [flux2-vae_small.safetensors](https://huggingface.co/Comfy-Org/MOSS-Image/blob/main/vae/flux2-vae_small.safetensors)

Base with turbo LoRA: [workflow_moss_image_base_turbo.json](MOSS%20Image/workflow_moss_image_base_turbo.json)

- [moss_image_base_int8_convrot.safetensors](https://huggingface.co/Comfy-Org/MOSS-Image/blob/main/diffusion_models/moss_image_base_int8_convrot.safetensors)
- [lora.safetensors](https://huggingface.co/lodestones/MOSS-Image-Base-8-steps-dmd/blob/main/lora.safetensors)
- [qwen3.5_9b_w4a8_gptq.safetensors](https://huggingface.co/Comfy-Org/MOSS-Image/blob/main/text_encoders/qwen3.5_9b_w4a8_gptq.safetensors)
- [flux2-vae_small.safetensors](https://huggingface.co/Comfy-Org/MOSS-Image/blob/main/vae/flux2-vae_small.safetensors)

## Krea 2

[workflow_krea2_raw_turbo.json](Krea%202/workflow_krea2_raw_turbo.json)

- [krea2_raw_int8_convrot.safetensors](https://huggingface.co/Comfy-Org/Krea-2/blob/main/diffusion_models/krea2_raw_int8_convrot.safetensors)
- [krea2_turbo_lora_rank_64_bf16.safetensors](https://huggingface.co/Comfy-Org/Krea-2/blob/main/loras/krea2_turbo_lora_rank_64_bf16.safetensors)
- [qwen3vl_4b_fp8_scaled.safetensors](https://huggingface.co/Comfy-Org/Krea-2/blob/main/text_encoders/qwen3vl_4b_fp8_scaled.safetensors)
- [wan_2.1_vae.safetensors](https://huggingface.co/Comfy-Org/Wan_2.1_ComfyUI_repackaged/blob/main/split_files/vae/wan_2.1_vae.safetensors)

## Qwen 2.1

Text to image: [workflow_qwen21_t2i.json](Qwen%202.1/workflow_qwen21_t2i.json)

- [qwen_image_2.1_int8_convrot.safetensors](https://huggingface.co/Comfy-Org/Qwen-Image-2.1/blob/main/diffusion_models/qwen_image_2.1_int8_convrot.safetensors)
- [qwen3vl_8b_int8_convrot.safetensors](https://huggingface.co/Comfy-Org/Qwen-Image-2.1/blob/main/text_encoders/qwen3vl_8b_int8_convrot.safetensors)
- [qwen_image_2.1_vae_bf16.safetensors](https://huggingface.co/Comfy-Org/Qwen-Image-2.1/blob/main/vae/qwen_image_2.1_vae_bf16.safetensors)

Edit: [workflow_qwen21_edit.json](Qwen%202.1/workflow_qwen21_edit.json)

- Same three files as the text-to-image workflow.

Int8 turbo text to image: [workflow_qwen21_turbo_t2i.json](Qwen%202.1/workflow_qwen21_turbo_t2i.json)

- [qwen_image_2.1_turbo_int8_convrot.safetensors](https://huggingface.co/Comfy-Org/Qwen-Image-2.1/blob/main/diffusion_models/qwen_image_2.1_turbo_int8_convrot.safetensors)
- [qwen3vl_8b_int8_convrot.safetensors](https://huggingface.co/Comfy-Org/Qwen-Image-2.1/blob/main/text_encoders/qwen3vl_8b_int8_convrot.safetensors)
- [qwen_image_2.1_vae_bf16.safetensors](https://huggingface.co/Comfy-Org/Qwen-Image-2.1/blob/main/vae/qwen_image_2.1_vae_bf16.safetensors)

Int8 turbo edit: [workflow_qwen21_turbo_edit.json](Qwen%202.1/workflow_qwen21_turbo_edit.json)

- Same three files as the int8 turbo text-to-image workflow.

Viggle text to image: [workflow_qwen21_viggle_t2i.json](Qwen%202.1/workflow_qwen21_viggle_t2i.json)

- [Qwen-Image-2.1-viggle-turbo-v0.3-6step-int8_convrot.safetensors](https://huggingface.co/Viggle/Qwen-Image-2.1-viggle-turbo/blob/main/Qwen-Image-2.1-viggle-turbo-v0.3-6step-int8_convrot.safetensors)
- [qwen3vl_8b_int8_convrot.safetensors](https://huggingface.co/Comfy-Org/Qwen-Image-2.1/blob/main/text_encoders/qwen3vl_8b_int8_convrot.safetensors)
- [qwen_image_2.1_vae_bf16.safetensors](https://huggingface.co/Comfy-Org/Qwen-Image-2.1/blob/main/vae/qwen_image_2.1_vae_bf16.safetensors)
- [viggle_turbo.py](https://huggingface.co/Viggle/Qwen-Image-2.1-viggle-turbo/blob/main/comfyui/viggle_turbo.py) — copy into `ComfyUI/custom_nodes/` and restart

Viggle edit: [workflow_qwen21_viggle_edit.json](Qwen%202.1/workflow_qwen21_viggle_edit.json)

- Same files as the Viggle text-to-image workflow.

## Image title and tags

[workflow_image_title_tags.json](Image%20Tags/workflow_image_title_tags.json)

- [qwen3vl_4b_bf16.safetensors](https://huggingface.co/Comfy-Org/Qwen3-VL/blob/main/text_encoders/qwen3vl_4b_bf16.safetensors)
- [ComfyUI-Custom-Scripts](https://github.com/pythongosssss/ComfyUI-Custom-Scripts) for the Show Text node

Folder captions: [workflow_image_folder_captions.json](Image%20Tags/workflow_image_folder_captions.json)

Type any folder path. A `.txt` file is written beside each image, using the image name.

- [qwen3vl_4b_bf16.safetensors](https://huggingface.co/Comfy-Org/Qwen3-VL/blob/main/text_encoders/qwen3vl_4b_bf16.safetensors)
- [caption_folder.py](Image%20Tags/caption_folder.py) — copy into `ComfyUI/custom_nodes/` and restart
- [ComfyUI-Custom-Scripts](https://github.com/pythongosssss/ComfyUI-Custom-Scripts) for the Show Text node
