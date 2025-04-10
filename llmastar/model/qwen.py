import transformers
import torch
from .prompts.qwen_prompts import PARSE_QWEN, QWEN_PROMPTS

class Qwen:
    def __init__(self, variant="Qwen2.5-7B-Instruct", device=None):
        if device is None:
            device = torch.device("cuda:0")
        
        self.model_id = f"Qwen/{variant}"
        
        self.pipeline = transformers.pipeline(
            "text-generation",
            model=self.model_id,
            model_kwargs={"torch_dtype": torch.bfloat16},
            device=device,
        )
        self.terminators = [
            self.pipeline.tokenizer.eos_token_id,
            self.pipeline.tokenizer.convert_tokens_to_ids("<|im_end|>")
        ]
    
    def ask(self, prompt):
        outputs = self.pipeline(
            prompt,
            max_new_tokens=8000,
            eos_token_id=self.terminators,
            do_sample=False,
            temperature=None,
            top_p=None,
            pad_token_id=self.pipeline.tokenizer.eos_token_id
        )
        return outputs[0]["generated_text"][len(prompt):]
        
    def get_prompt(self, prompt_type, **kwargs):
        """Get a prompt template and format it with the provided parameters."""
        if prompt_type == "parse":
            return PARSE_QWEN.format(**kwargs)
        elif prompt_type in QWEN_PROMPTS:
            return QWEN_PROMPTS[prompt_type].format(**kwargs)
        else:
            raise ValueError(f"Unknown prompt type: {prompt_type}")
