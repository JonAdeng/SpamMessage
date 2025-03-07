import gdown
import os

# Pastikan folder tujuan ada
os.makedirs("dataset", exist_ok=True)

# Download file pertama
try:
    url = "https://drive.google.com/uc?id=1JH6NXQygYGDA9e_U4HhXYVAuIFZVwAfd"
    output = "dataset/indobert_tokenizer.pkl"
    gdown.download(url, output, quiet=False)
except Exception as e:
    print(f"Error downloading first file: {e}")

# Download file kedua
try:
    url1 = "https://drive.google.com/uc?id=1sVxpucTDccVjYOnoy7h5-e9eSS4x_pIe"
    output1 = "dataset/indobert_finetuned.pkl"
    gdown.download(url1, output1, quiet=False)
except Exception as e:
    print(f"Error downloading second file: {e}")
