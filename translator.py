# translator.py

import torch
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from IndicTransToolkit.processor import IndicProcessor

class IndicTranslator:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            print("Loading IndicTrans2 Translator...")
            cls._instance = super().__new__(cls)
            model_name = "./models/indictrans2-en-indic-dist-200M"

            tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
            model = AutoModelForSeq2SeqLM.from_pretrained(
                model_name,
                trust_remote_code=True,
                torch_dtype=torch.bfloat16,
                device_map="auto",
                attn_implementation="eager",
                low_cpu_mem_usage=True,
            )
            model.tie_weights()
            ip = IndicProcessor(inference=True)

            cls._instance.tokenizer = tokenizer
            cls._instance.model = model
            cls._instance.ip = ip
            cls._instance.device = next(model.parameters()).device
        return cls._instance

    def translate(self, text: str, lang: str) -> str:
        if lang == "en" or not text.strip():
            return text

        lang_map = {
            "hi": "hin_Deva", "ta": "tam_Taml", "te": "tel_Telu", "ml": "mal_Mlym",
            "bn": "ben_Beng", "gu": "guj_Gujr", "kn": "kan_Knda", "pa": "pan_Guru",
            "mr": "mar_Deva", "ur": "urd_Arab"
        }
        if lang not in lang_map:
            return text

        tgt_lang = lang_map[lang]
        src_lang = "eng_Latn"

        try:
            batch = self.ip.preprocess_batch([text], src_lang=src_lang, tgt_lang=tgt_lang)
            inputs = self.tokenizer(
                batch, truncation=True, padding="longest",
                return_tensors="pt", return_attention_mask=True
            ).to(self.device)

            with torch.no_grad():
                generated_tokens = self.model.generate(
                    **inputs,
                    use_cache=True,
                    min_length=0,
                    max_length=256,
                    num_beams=5,
                )

            translations = self.tokenizer.batch_decode(
                generated_tokens, skip_special_tokens=True, clean_up_tokenization_spaces=True
            )
            return self.ip.postprocess_batch(translations, lang=tgt_lang)[0]
        except Exception as e:
            print(f"Translation failed for {lang}: {e}")
            return text

translator = IndicTranslator()