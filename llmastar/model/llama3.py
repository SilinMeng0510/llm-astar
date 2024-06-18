import transformers
import torch

class Llama3:
  def __init__(self):
    model_id = "meta-llama/Meta-Llama-3-8B-Instruct"
    self.pipeline = transformers.pipeline(
        "text-generation",
        model=model_id,
        model_kwargs={"torch_dtype": torch.bfloat16},
        device="cuda:3",
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