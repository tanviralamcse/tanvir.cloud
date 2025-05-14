import pandas as pd
import time
from tqdm import tqdm
from sentence_transformers import SentenceTransformer
import hdbscan
import numpy as np

# --- CONFIG ---
INPUT_FILE = "/Users/tanviralam/visa2025/video/1bc.csv"           # Your input CSV file
OUTPUT_FILE = "/Users/tanviralam/visa2025/video/clustered_keywords.csv"  # Output file
KEYWORD_COLUMN = "Keyword"            # Column name in the CSV
MODEL_NAME = "all-MiniLM-L6-v2"       # Embedding model
BATCH_SIZE = 512                      # Adjust for memory
# ---------------

# Load data
print("🔄 Loading keywords...")
df = pd.read_csv(INPUT_FILE)
keywords = df[KEYWORD_COLUMN].dropna().tolist()

# Load model
print("⚙️  Loading embedding model...")
model = SentenceTransformer(MODEL_NAME)

# Embed keywords with progress bar and ETA
print(f"🔍 Embedding {len(keywords)} keywords...")
embeddings = []
start_time = time.time()
for i in tqdm(range(0, len(keywords), BATCH_SIZE), desc="Embedding", unit="batch"):
    batch = keywords[i:i + BATCH_SIZE]
    batch_embeddings = model.encode(batch, show_progress_bar=False)
    embeddings.extend(batch_embeddings)
    elapsed = time.time() - start_time
    avg_time_per_keyword = elapsed / (i + BATCH_SIZE)
    remaining = avg_time_per_keyword * (len(keywords) - (i + BATCH_SIZE))
    print(f"⏱️ ETA: {remaining/60:.2f} min remaining")

embeddings = np.array(embeddings)

# Clustering
print("🧠 Clustering with HDBSCAN...")
clusterer = hdbscan.HDBSCAN(min_cluster_size=15, metric='euclidean', prediction_data=True)
cluster_labels = clusterer.fit_predict(embeddings)

# Save results
print("💾 Saving results...")
df = df.loc[:len(cluster_labels)-1]  # In case of length mismatch
df['cluster_id'] = cluster_labels
df.to_csv(OUTPUT_FILE, index=False)

# Summary
num_clusters = len(set(cluster_labels)) - (1 if -1 in cluster_labels else 0)
print(f"\n✅ Done! Saved to '{OUTPUT_FILE}'")
print(f"🔢 Total clusters found: {num_clusters}")
print(f"⚠️ {np.sum(cluster_labels == -1)} keywords were marked as noise (cluster_id = -1)")
