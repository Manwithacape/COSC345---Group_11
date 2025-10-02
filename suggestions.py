class Suggestions:
    def __init__(self, db, analyzer):
        self.db = db
        self.analyzer = analyzer

    def suggest_for_photo(self, photo_id):
        """
        Suggest 'keep' for best duplicate, 'delete' for others.
        Suggest 'delete' for low-quality photos.
        """
        quality = self.db.get_quality_score(photo_id)
        duplicates = self.db.get_near_duplicates(photo_id)

        # If duplicates found, suggest keep best quality, delete others
        if duplicates:
            group = self.db.get_photos_in_near_duplicate_group(duplicates["id"])
            best = max(group, key=lambda p: self.db.get_quality_score(p["id"]) or 0)
            for p in group:
                self.db.update_photo_suggestion(p["id"], "keep" if p["id"] == best["id"] else "delete")
            return
        
        # Otherwise, use photo quality thresholds
        if quality is not None and quality < 0.3:
            self.db.update_photo_suggestion(photo_id, "delete")
        else:
            self.db.update_photo_suggestion(photo_id, "keep")