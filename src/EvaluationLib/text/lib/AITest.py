from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline, logging
import os
import re

logging.set_verbosity_error()

base_dir = os.path.dirname(__file__)
model_dir = os.path.abspath(os.path.join(base_dir, "..", "models"))
tokenizer = AutoTokenizer.from_pretrained(model_dir)
model = AutoModelForTokenClassification.from_pretrained(model_dir)
ner_pipeline_obj = pipeline(
    "ner",
    model=model,
    tokenizer=tokenizer,
    aggregation_strategy="simple"
)
def normalize(text: str) -> str:
    text = re.sub(r"[^\w\s/]", "", text)
    text = text.lower()
    return text

def NERTest(text: str):
    text= normalize(text)
    results = ner_pipeline_obj(text)
    target_tags = ["VELOCITY", "LOCATION", "OBSTACLE", "FLOOD", "POLICE", "JAM"]
    output = {}

    for tag in target_tags:
        tag_results = []
        for r in results:
            entity = r["entity_group"].upper()
            if entity.startswith("B-") or entity.startswith("I-"):
                entity = entity.split("-")[-1]
            if entity == tag:
                tag_results.append(r)

        if tag_results:
            best = max(tag_results, key=lambda x: x["score"])
            conf = float(best["score"])
            output[tag] = {
                "detected": True,
                "text": best["word"],
                "score": round(conf, 2)
            }
        else:
            output[tag] = {
                "detected": False,
                "text": None,
                "score": 0.0
            }

    return output

    
if __name__ == "__main__":
    import sys
    import io

    # Set stdout to use UTF-8 encoding
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    print(NERTest(''))