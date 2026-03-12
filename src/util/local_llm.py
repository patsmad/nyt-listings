from transformers import Qwen2_5_VLForConditionalGeneration, AutoProcessor
from qwen_vl_utils import process_vision_info

# See models in: ~\.cache\huggingface\hub

VCR_CODE_QUERY = ('This is a television listing for a film in The New York Times. '
                  'Identify the vcr code, a 4-8 digit number, at the end of the listing. '
                  'Return ONLY that number.')

class LocalLLMAPI:
    def __init__(self):
        self.model = Qwen2_5_VLForConditionalGeneration.from_pretrained(
            "Qwen/Qwen2.5-VL-7B-Instruct", torch_dtype="auto", device_map="auto"
        )
        self.processor = AutoProcessor.from_pretrained("Qwen/Qwen2.5-VL-7B-Instruct")

    def analyze_image(self, query, image):
        print('Deducing title...')
        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "image", "image": image},
                    {"type": "text", "text": query},
                ],
            }
        ]

        # Preparation for inference
        text = self.processor.apply_chat_template(
            messages, tokenize=False, add_generation_prompt=True
        )
        image_inputs, video_inputs = process_vision_info(messages)
        inputs = self.processor(
            text=[text],
            images=image_inputs,
            videos=video_inputs,
            padding=True,
            return_tensors="pt",
        )
        inputs = inputs.to("cuda")

        # Inference: Generation of the output
        generated_ids = self.model.generate(**inputs, max_new_tokens=128)
        generated_ids_trimmed = [
            out_ids[len(in_ids):] for in_ids, out_ids in zip(inputs.input_ids, generated_ids)
        ]

        output_text = self.processor.batch_decode(
            generated_ids_trimmed, skip_special_tokens=True, clean_up_tokenization_spaces=False
        )
        if len(output_text) > 0:
            return output_text[0]

    def get_vcr_code_for_image(self, image):
        maybe_vcr_code = self.analyze_image(VCR_CODE_QUERY, image)
        if maybe_vcr_code is not None:
            try:
                int(maybe_vcr_code)
                return maybe_vcr_code
            except:
                pass
