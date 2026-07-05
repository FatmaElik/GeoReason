"""
Step 2 — Run the VLM over all samples and all conditions.

Inference only, no training. Designed for a free Colab GPU with the
2B model; if you have more memory, change MODEL_ID to a larger
Qwen3-VL variant — the rest of the code stays the same.

Results are appended to results.csv after EVERY sample, so a Colab
disconnect never loses finished work; re-running skips completed rows.

Usage:
    python run_experiment.py --data pilot_data
"""

import argparse
import os

import pandas as pd
import torch
from PIL import Image
from transformers import AutoProcessor, Qwen3VLForConditionalGeneration

from prompts import CONDITIONS, build_prompt, normalize_answer

MODEL_ID = "Qwen/Qwen3-VL-2B-Instruct"  # upgrade to 4B/8B if GPU allows
MAX_NEW_TOKENS = 32


def load_model():
    processor = AutoProcessor.from_pretrained(MODEL_ID)
    model = Qwen3VLForConditionalGeneration.from_pretrained(
        MODEL_ID,
        dtype=torch.float16,
        device_map="auto",
    )
    return processor, model


def ask_vlm(processor, model, image: Image.Image, prompt: str) -> str:
    messages = [
        {
            "role": "user",
            "content": [
                {"type": "image", "image": image},
                {"type": "text", "text": prompt},
            ],
        }
    ]
    inputs = processor.apply_chat_template(
        messages,
        add_generation_prompt=True,
        tokenize=True,
        return_dict=True,
        return_tensors="pt",
    ).to(model.device)

    with torch.no_grad():
        output_ids = model.generate(
            **inputs,
            max_new_tokens=MAX_NEW_TOKENS,
            do_sample=False,  # deterministic: same input -> same answer
        )

    generated = output_ids[:, inputs["input_ids"].shape[1]:]
    return processor.batch_decode(generated, skip_special_tokens=True)[0]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", default="pilot_data")
    args = parser.parse_args()

    samples = pd.read_csv(
        os.path.join(args.data, "samples.csv"), dtype={"sample_id": str}
    )

    results_path = os.path.join(args.data, "results.csv")

    # Resume support: skip (sample, condition) pairs already done
    done = set()
    if os.path.exists(results_path):
        old = pd.read_csv(results_path, dtype={"sample_id": str})
        done = set(zip(old["sample_id"], old["condition"]))
        print(f"Resuming: {len(done)} rows already finished.")

    processor, model = load_model()
    print("Model ready:", MODEL_ID)

    results = []
    total = len(samples) * len(CONDITIONS)
    step = 0

    for _, row in samples.iterrows():
        image = Image.open(
            os.path.join(args.data, row["prompt_image"])
        ).convert("RGB")
        true_class = int(row["true_class"])

        for condition in CONDITIONS:
            step += 1
            if (row["sample_id"], condition) in done:
                continue

            prompt = build_prompt(condition, true_class)
            raw = ask_vlm(processor, model, image, prompt)
            answer = normalize_answer(raw)

            results.append({
                "sample_id": row["sample_id"],
                "condition": condition,
                "true_class": true_class,
                "raw_answer": raw,
                "answer": answer,
            })

            # append-save after every call (Colab-safe)
            pd.DataFrame(results).to_csv(
                results_path,
                mode="a" if os.path.exists(results_path) else "w",
                header=not os.path.exists(results_path),
                index=False,
            )
            results = []

            print(f"[{step}/{total}] {row['sample_id']} {condition} -> {answer}")

    print("Done. Results at:", results_path)


if __name__ == "__main__":
    main()
