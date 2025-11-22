# model.py

from transformers import pipeline, AutoTokenizer
import torch

class AstroLLM:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            print("Loading Phi-3 Mini...")
            cls._instance = super().__new__(cls)
            model_id = "microsoft/Phi-3-mini-4k-instruct"
            tokenizer = AutoTokenizer.from_pretrained(model_id, trust_remote_code=True)

            pipe = pipeline(
                "text-generation",
                model=model_id,
                tokenizer=tokenizer,
                torch_dtype=torch.bfloat16,
                device_map="auto",
                trust_remote_code=True,
                max_new_tokens=120,
                do_sample=True,
                temperature=0.75,
                top_p=0.9,
                return_full_text=False,        
                eos_token_id=tokenizer.eos_token_id,
                pad_token_id=tokenizer.eos_token_id,
            )

            cls._instance.pipe = pipe
            cls._instance.tokenizer = tokenizer

        return cls._instance

    def generate_insight(self, prompt: str) -> str:
        try:
            messages = [{"role": "user", "content": prompt}]
            formatted = self.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
            
            outputs = self.pipe(formatted, max_new_tokens=120, do_sample=True, temperature=0.75)
            text = outputs[0]["generated_text"].strip()

            if "assistant" in text:
                text = text.split("assistant")[-1]
            if "<|end|>" in text:
                text = text.split("<|end|>")[0]

            return text.strip() or "The stars shine brightly upon you today. Great energy flows your way."
        
        except Exception as e:
            print(f"LLM Error: {e}")
            return "The universe is aligning beautiful things for you today. Trust the journey."

llm = AstroLLM()