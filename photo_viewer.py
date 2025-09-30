# photo_viewer.py
import ttkbootstrap as ttk
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from main_viewer import MainViewer
from base_viewer import BaseThumbnailViewer
from PIL import Image, ImageTk, ImageDraw, ImageFont
from photo_analyzer import PhotoAnalyzer
from llm_feedback import make_paragraph
import threading


class PhotoViewer(BaseThumbnailViewer, MainViewer):
    """Scrollable grid of photo thumbnails with single-photo preview support."""

    def __init__(self, parent, db, open_single_callback=None, **kwargs):
        kwargs.pop("db", None)
        super().__init__(parent, **kwargs)
        BaseThumbnailViewer.__init__(self, parent, db=db, thumb_size=120, padding=10)

        self.open_single_callback = open_single_callback  # <-- callback to app

        self.thumb_size = 120
        self.padding = 10
        self.columns = 1
        self.labels = []
        self.thumbs = []
        self.single_item_active = False
        self.selected_idx = None
        self.db = db
        self.photo_analyzer = PhotoAnalyzer(db)

        # toolbar for controls (e.g., thumbnail size)
        self.toolbar = ttk.Frame(self.inner_frame)
        self.toolbar.pack(fill="x", side="top")

        ttk.Label(self.toolbar, text="Thumbnails:").pack(side="left", padx=(4, 6))
        self.size_var = tk.StringVar(value="Medium")
        self.size_combo = ttk.Combobox(
            self.toolbar,
            textvariable=self.size_var,
            values=["Small", "Medium", "Large"],
            state="readonly",
            width=8,
        )
        self.size_combo.pack(side="left")
        self.size_combo.bind("<<ComboboxSelected>>", lambda e: self._on_size_change())

        # dedicated container for the grid below toolbar
        self.grid_area = ttk.Frame(self.inner_frame)
        self.grid_area.pack(fill="both", expand=True)

        # --- FLOATING LLM Feedback card: overlay bottom-left of viewer ---
        self.feedback_card = ttk.Labelframe(
            self,  # parent is the viewer itself (not grid_area)
            text="LLM Feedback",
            bootstyle="info",
            padding=10,
        )

        self.feedback_box = ScrolledText(
            self.feedback_card,
            height=6,
            wrap="word",
        )
        self.feedback_box.configure(
            bg="#1e1e1e",
            fg="#ffffff",
            insertbackground="#ffffff",
            relief="flat",
            padx=10,
            pady=10,
        )
        self.feedback_box.grid(row=0, column=0, sticky="nsew", padx=(0, 8), pady=(0, 8))

        self.gen_btn = ttk.Button(
            self.feedback_card,
            text="Generate feedback",
            bootstyle="primary",
            command=self.generate_feedback_for_current,
        )
        self.gen_btn.grid(row=1, column=0, sticky="w", pady=(4, 0))

        self.feedback_card.columnconfigure(0, weight=1)
        self.feedback_card.rowconfigure(0, weight=1)

        # Pin to bottom-left (in front of thumbnails) and keep it there
        # width can be adjusted; height follows content
        self.feedback_card.place(relx=0.0, rely=1.0, x=12, y=-12, anchor="sw", width=360)
        self.feedback_card.lift()

        def _set_feedback(text: str):
            self.feedback_box.configure(state="normal")
            self.feedback_box.delete("1.0", "end")
            self.feedback_box.insert("1.0", text)
            self.feedback_box.configure(state="disabled")
        self._set_feedback = _set_feedback
        # --- end floating card ---

        self.refresh_photos()

    def add_score_overlay(self, image, rank, score):
        try:
            score = float(score)
        except Exception:
            score = 0.0

        draw = ImageDraw.Draw(image)
        font = ImageFont.load_default()

        text_rank = f"#{rank}"
        draw.rectangle([0, 0, 60, 30], fill="black")
        draw.text((5, 5), text_rank, fill="white", font=font)

        text_score = f"{score:.2f}"
        draw.text((5, 15), text_score, fill="white", font=font)

        return image

    def refresh_photos(self, collection_id=None):
        """Load photos as thumbnails."""
        self.current_collection_id = collection_id
        for lbl in self.labels:
            try:
                lbl.destroy()
            except:
                pass
        self.labels = []
        self.thumbs = []

        self.single_item_active = False

        # Make sure grid_area is visible
        if not self.grid_area.winfo_ismapped():
            self.grid_area.pack(fill="both", expand=True)

        self.photos = self.db.get_photos(collection_id)

        # Compute rankings
        ranked = self.photo_analyzer.rank_by_quality([p["id"] for p in self.photos])
        rank_map = {pid: idx + 1 for idx, (pid, _) in enumerate(ranked)}

        ranked_photos = sorted(
            self.photos,
            key=lambda p: rank_map.get(p["id"], float("inf"))
        )

        for photo in ranked_photos:
            photo_id = photo["id"]
            # Start from a uniform, letterboxed PIL thumbnail
            pil_thumb = self.create_uniform_thumbnail_pil(photo["file_path"]) or None
            if pil_thumb is None:
                tk_img = None
            else:
                score = self.db.get_quality_score(photo["id"])
                rank = rank_map.get(photo["id"], "-")
                if score is not None:
                    pil_thumb = self.add_score_overlay(pil_thumb, rank, score)
                tk_img = ImageTk.PhotoImage(pil_thumb)
            if not tk_img:
                continue

            self.thumbs.append(tk_img)

            lbl = ttk.Label(
                self.grid_area,
                image=tk_img,
                cursor="hand2",
                bootstyle="dark",
                relief="flat"
            )
            lbl.image = tk_img
            lbl.photo_id = photo["id"]
            lbl.photo_path = photo["file_path"]

            lbl.bind("<Button-1>", lambda e, pid=photo["id"]: self._on_photo_click(pid))
            lbl.bind(
                "<Double-1>",
                lambda e, path=photo["file_path"], pid=photo["id"]: self._show_single_photo(path, pid)
            )

            self.labels.append(lbl)

        self._reflow_grid()

        if self.labels:
            self._select_idx(0)
            self.select_photo(self.labels[0].photo_id)

    def _on_photo_click(self, photo_id):
        idx = next((i for i, lbl in enumerate(self.labels) if lbl.photo_id == photo_id), None)
        if idx is not None:
            self._select_idx(idx)
        self.select_photo(photo_id)

    def _select_idx(self, idx):
        if self.selected_idx is not None and 0 <= self.selected_idx < len(self.labels):
            self.labels[self.selected_idx].config(relief="flat")
        self.selected_idx = idx
        self.labels[idx].config(relief="solid")

    def _on_resize(self, event=None):
        if self.single_item_active or not self.labels:
            return
        width = self.canvas.winfo_width()
        if width < 50:
            self.after(50, self._on_resize, event)
            return
        self.columns = max(1, width // (self.thumb_size + self.padding))
        self._reflow_grid()

    def _on_size_change(self):
        """Handle toolbar size change and refresh grid."""
        size_map = {"Small": 80, "Medium": 120, "Large": 180}
        new_size = size_map.get(self.size_var.get(), 120)
        if new_size != self.thumb_size:
            self.thumb_size = new_size
            # Rebuild thumbnails at new size
            self.refresh_photos(getattr(self, "current_collection_id", None))
            # Recompute columns with new size
            self.after(0, self._on_resize)

    def _reflow_grid(self):
        if not self.labels or self.single_item_active:
            return
        for lbl in self.labels:
            if lbl.winfo_exists():
                lbl.grid_forget()
        for idx, lbl in enumerate(self.labels):
            if lbl.winfo_exists():
                row, col = divmod(idx, self.columns)
                lbl.grid(row=row, column=col, padx=5, pady=5, sticky="nw")

        # keep feedback floating above
        self.feedback_card.lift()

    def _show_single_photo(self, photo_path, photo_id):
        """Ask the app to switch the center pane to a full SinglePhotoViewer."""
        if callable(self.open_single_callback):
            self.open_single_callback(photo_path, photo_id)

    # --------LLM Helper Methods-------

    def _photo_facts(self):
        """
        Build a minimal, explicit facts object for the LLM.
        Shape:
        {
            "collection_id": <id or None>,
            "count": <int>,
            "photos": [
                {"id": <int>, "exif": {...} or None, "scores": {...} or None}
            ]
        }
        """
        collection_id = getattr(self, "current_collection_id", None)
        photos = self.db.get_photos(collection_id) or []

        facts = {
            "collection_id": collection_id,
            "count": len(photos),
            "photos": [],
        }

        for p in photos:
            pid = p.get("id") if isinstance(p, dict) else getattr(p, "id", None)
            if pid is None:
                continue

            try:
                exif = self.db.get_exif(pid)
            except Exception:
                exif = None

            try:
                if hasattr(self.db, "get_scores") and callable(self.db.get_scores):
                    scores = self.db.get_scores(pid)
                else:
                    scores = {"quality": self.db.get_quality_score(pid)}
            except Exception:
                scores = None

            facts["photos"].append({
                "id": pid,
                "exif": exif,
                "scores": scores,
            })

        return facts

    def generate_feedback_for_current(self):
        """Called by the 'Generate feedback' button."""
        sel = getattr(self, "selected_idx", None)
        if not self.photos:
            self._set_feedback("No photos loaded.")
            return

        collection_id = getattr(self, "current_collection_id", None)
        if collection_id is None:
            self._set_feedback("No collection selected.")
            return

        user_prompt_collection = (
            "Write a short paragraph (3–5 sentences) assessing this photo collection. "
            "Use only the provided facts (EXIF + numeric scores). "
            "If a detail is missing, state 'insufficient data' rather than assuming. "
            "Do not invent camera settings, locations, or subjects."
        )

        def work():
            try:
                col_para = make_paragraph(
                    user_prompt_collection,
                    self._photo_facts()
                )
                out = ["— Collection —", col_para, ""]
                self.after(0, lambda: self._set_feedback("\n".join(out)))
            except Exception as e:
                self.after(0, lambda e=e: self._set_feedback(f"LLM error: {e}"))

        threading.Thread(target=work, daemon=True).start()
