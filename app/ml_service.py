import os
import logging
from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

MODEL_EN_RU = os.getenv("MODEL_NAME_EN_RU", "Helsinki-NLP/opus-mt-en-ru")
MODEL_RU_EN = os.getenv("MODEL_NAME_RU_EN", "Helsinki-NLP/opus-mt-ru-en")

translators = {}

def load_model(model_name: str):
    if model_name not in translators:
        logger.info(f"Loading model {model_name} ...")
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
        translators[model_name] = pipeline("translation", model=model, tokenizer=tokenizer)
    return translators[model_name]

def translate(text: str, direction: str) -> tuple[str, str]:
    if direction == "en-ru":
        model_name = MODEL_EN_RU
    elif direction == "ru-en":
        model_name = MODEL_RU_EN
    else:
        raise ValueError(f"Unsupported direction: {direction}")

    pipe = load_model(model_name)
    result = pipe(text, max_length=512)
    translated = result[0]["translation_text"]
    return translated, model_name