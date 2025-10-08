import torch
import clip
from PIL import Image
import numpy as np
from tqdm import tqdm

from db import Database


class PhotoAnalyzer:
    """
    PhotoAnalyzr handles higher level photo analysis:
    - Extracts deep embeddings using CLIP
    - Embeddings can be used for:
        - clustering/grouping photos
        - search by similarity
        - training data for high-level ML models
        - duplicate detection
    - Stores embeddings in DB
    - Provides clustering and ranking tools
    NOTE: Quality scoring is handled by PhotoScorer and importer
    """

    def __init__(self, db: Database = None, device: str = None):
        self.db = db
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")

        # Load CLIP model
        self.model, self.process = clip.load("ViT-B/32", device=self.device)

    # --------------------- Embeddings -------------------------
    def extract_embedding(self, file_path):
        """Extracts a semantic embedding vector using CLIP."""
        img = Image.open(file_path).convert("RGB")
        img_preprocessed = self.process(img).unsqueeze(0).to(self.device)

        with torch.no_grad():
            features = self.model.encode_image(img_preprocessed)
            features /= features.norm(dim=-1, keepdim=True)  # nomarlize

        return features.cpu().numpy().flatten()

    def analyze_photo(self, photo_id, file_path):
        """
        Analyze a single photo:
        - Extract CLIP embedding and store in DB
        (Scores already handled at import time)
        """
        if self.db is None:
            raise ValueError("Database instance not provided.")

        embedding = self.extract_embedding(file_path)
        self.db.add_embedding(photo_id, embedding.tolist())

        return {"embedding": embedding}

    # --------------- Analyze Collection of Photos -----------------
    def analyze_collection(self, photo_list):
        """
        Analyze a list of photos
        Stores results in DB
        returns dict: photo_id -> embedding
        """

        results = {}
        for photo in tqdm(photo_list, desc="Analyzing photos"):
            photo_id, path = photo["id"], photo["file_path"]
            try:
                results[photo_id] = self.analyze_photo(photo_id, path)
            except Exception as e:
                print(f"Failed to analyze {path}: {e}")

        return results

    # --------------- Cluster Photos -----------------
    def cluster_embeddings(self, photo_ids, eps=0.3, min_samples=2):
        """
        Cluster photos based on their CLIP embeddings using DBSCAN.
        Returns dict: cluster_id -> list of photo_ids
        """

        from sklearn.cluster import DBSCAN

        embeddings = []
        id_map = []
        for pid in photo_ids:
            emb = self.db.get_embedding(pid)
            if emb is not None:
                embeddings.append(emb)
                id_map.append(pid)

        if not embeddings:
            return {}

        embeddings_np = np.array(embeddings)
        clustering = DBSCAN(eps=eps, min_samples=min_samples, metric="cosine").fit(
            embeddings_np
        )
        labels = clustering.labels_

        clusters = {}
        for pid, label in zip(id_map, labels):
            if label == -1:
                continue  # ignore noise
            clusters.setdefault(label, []).append(pid)

        return clusters

    # --------------- Rank Photos by Quality -----------------
    def rank_by_quality(self, photo_ids):
        """
        Rank photos by a composite quality score derived from low-level metrics.
        Returns list of (photo_id, score) sorted by score descending.
        """

        scores = []
        for pid in photo_ids:
            q = self.db.get_quality_score(pid)
            if q is not None:
                scores.append((pid, q))

        scores.sort(key=lambda x: x[1], reverse=True)
        return scores
