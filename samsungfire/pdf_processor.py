# samsungfire/pdf_processor.py
import json
import os
import re
import pymupdf
import numpy as np
from sentence_transformers import SentenceTransformer


def extract_and_chunk_pdf(pdf_path, chunk_size=600, overlap=100):
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")

    doc = pymupdf.open(pdf_path)
    chunks = []
    chunk_id = 0

    print(f"Processing PDF '{pdf_path}' ({len(doc)} pages)...")

    for page_idx in range(len(doc)):
        page = doc[page_idx]
        raw_text = page.get_text() or ""
        cleaned_text = re.sub(r'\s+', ' ', raw_text).strip()
        if not cleaned_text or len(cleaned_text) < 15:
            continue

        page_num = page_idx + 1

        start = 0
        text_len = len(cleaned_text)
        while start < text_len:
            end = start + chunk_size
            chunk_text = cleaned_text[start:end].strip()
            if len(chunk_text) >= 20:
                chunks.append({
                    "chunk_id": chunk_id,
                    "page": page_num,
                    "text": chunk_text
                })
                chunk_id += 1
            start += (chunk_size - overlap)

    print(f"Total chunks created: {len(chunks)}")
    return chunks


def build_embeddings_and_save(chunks, npy_path, json_path, model_name="jhgan/ko-sbert-sts"):
    print("Saving chunks metadata to JSON...")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(chunks, f, ensure_ascii=False, indent=2)

    print(f"Generating SBERT embeddings with '{model_name}'...")
    model = SentenceTransformer(model_name)
    texts = [c["text"] for c in chunks]
    embeddings = model.encode(texts, show_progress_bar=True, normalize_embeddings=True)

    print(f"Saving embeddings to '{npy_path}' (shape: {embeddings.shape})...")
    np.save(npy_path, embeddings)
    print("Embedding pre-computation complete!")


if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    pdf_file = os.path.join(base_dir, "samsungfire_doc.pdf")
    json_file = os.path.join(base_dir, "chunks.json")
    npy_file = os.path.join(base_dir, "embeddings.npy")

    chunks_data = extract_and_chunk_pdf(pdf_file)
    build_embeddings_and_save(chunks_data, npy_file, json_file)
