import transformers
import torch
from .prompts.llama_prompts import PARSE_LLAMA, LLAMA_PROMPTS

class Llama3:
  def __init__(self, variant="Llama-3.2-3B-Instruct", device=None):
    if device is None:
      device = torch.device("cuda:0")
    self.model_id = f"meta-llama/{variant}"
    # model_id = "meta-llama/Meta-Llama-3-8B-Instruct"
    self.pipeline = transformers.pipeline(
        "text-generation",
        model=self.model_id,
        model_kwargs={"torch_dtype": torch.bfloat16},
        device=device,
    )
    self.terminators = [
        self.pipeline.tokenizer.eos_token_id,
        self.pipeline.tokenizer.convert_tokens_to_ids("<|eot_id|>")
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
      return PARSE_LLAMA.format(**kwargs)
    elif prompt_type in LLAMA_PROMPTS:
      return LLAMA_PROMPTS[prompt_type].format(**kwargs)
    else:
      raise ValueError(f"Unknown prompt type: {prompt_type}")
