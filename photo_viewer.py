# photo_viewer.py
import ttkbootstrap as ttk
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from tkinter import messagebox
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

        self.open_single_callback = open_single_callback

        self.thumb_size = 120
        self.padding = 10
        self.columns = 1
        self.labels = []
        self.thumbs = []
        self.single_item_active = False
        self.selected_idx = None
        self.db = db
        self.photo_analyzer = PhotoAnalyzer(db)

        # NEW: remember last number of columns so we can clear them on change
        self._last_cols = 0

        # context menu state
        self._ctx_menu = None
        self._ctx_photo_id = None
        self.current_collection_id = None

        # toolbar
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

        # grid area
        self.grid_area = ttk.Frame(self.inner_frame)
        self.grid_area.pack(fill="both", expand=True)
        self.grid_area.bind("<Configure>", lambda e: self._reflow_grid())
        self.canvas.bind("<Configure>", lambda e: self._reflow_grid())

        # Floating LLM feedback card
        self.feedback_card = ttk.Labelframe(
            self, text="LLM Feedback", bootstyle="info", padding=10
        )
        self.feedback_box = ScrolledText(self.feedback_card, height=6, wrap="word")
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
        self.feedback_card.place(
            relx=0.0, rely=1.0, x=12, y=-12, anchor="sw", width=360
        )
        self.feedback_card.lift()

        def _set_feedback(text: str):
            self.feedback_box.configure(state="normal")
            self.feedback_box.delete("1.0", "end")
            self.feedback_box.insert("1.0", text)
            self.feedback_box.configure(state="disabled")

        self._set_feedback = _set_feedback

    # ---------------- thumbnails ----------------

    def add_score_overlay(self, image, rank, score):
        try:
            score = float(score)
        except Exception:
            score = 0.0
        draw = ImageDraw.Draw(image)
        font = ImageFont.load_default()
        draw.rectangle([0, 0, 60, 30], fill="black")
        draw.text((5, 5), f"#{rank}", fill="white", font=font)
        draw.text((5, 15), f"{score:.2f}", fill="white", font=font)
        return image

    def refresh_photos(self, collection_id=None):
        self.current_collection_id = collection_id
        for w in self.labels:
            try:
                w.destroy()
            except Exception:
                pass
        self.labels = []
        self.thumbs = []
        self.single_item_active = False

        if not self.grid_area.winfo_ismapped():
            self.grid_area.pack(fill="both", expand=True)

        photos_raw = self.db.get_photos(collection_id)
        self.photos = [
            p for p in photos_raw if (p.get("suggestion") or "").lower() != "deleted"
        ]

        ranked = self.photo_analyzer.rank_by_quality([p["id"] for p in self.photos])
        rank_map = {pid: idx + 1 for idx, (pid, _) in enumerate(ranked)}
        ranked_photos = sorted(
            self.photos, key=lambda p: rank_map.get(p["id"], float("inf"))
        )

        for photo in ranked_photos:
            photo_id = photo["id"]
            pil_thumb = self.create_uniform_thumbnail_pil(photo["file_path"]) or None
            if not pil_thumb:
                continue
            score = self.db.get_quality_score(photo_id)
            rank = rank_map.get(photo_id, "-")
            if score is not None:
                pil_thumb = self.add_score_overlay(pil_thumb, rank, score)
            tk_img = ImageTk.PhotoImage(pil_thumb)
            self.thumbs.append(tk_img)

            frame = ttk.Frame(self.grid_area, padding=0)
            frame.photo_id = photo_id

            lbl = ttk.Label(frame, image=tk_img, cursor="hand2", relief="flat")
            lbl.image = tk_img
            lbl.photo_id = photo_id
            lbl.photo_path = photo["file_path"]
            lbl.pack()

            show_suggestions = getattr(
                self.master.sidebar_buttons, "suggestions_visible", False
            )
            if show_suggestions:
                suggestion = self.db.get_photo_suggestion(photo_id) or "undecided"
                if suggestion == "keep":
                    frame.config(bootstyle="success")
                elif suggestion == "delete":
                    frame.config(bootstyle="danger")
                else:
                    frame.config(bootstyle="secondary")
            else:
                frame.config(bootstyle="secondary")

            lbl.bind("<Button-1>", lambda e, pid=photo_id: self._on_photo_click(pid))
            lbl.bind(
                "<Double-1>",
                lambda e, path=photo[
                    "file_path"
                ], pid=photo_id: self._show_single_photo(path, pid),
            )

            self._bind_thumb_context(lbl, photo_id=photo_id)
            self.labels.append(frame)

        self._reflow_grid()

        if self.labels:
            self._select_idx(0)
            first_pid = getattr(self.labels[0], "photo_id", None)
            if first_pid is not None:
                self.select_photo(first_pid)

    def _on_photo_click(self, photo_id):
        idx = next(
            (
                i
                for i, fr in enumerate(self.labels)
                if getattr(fr, "photo_id", None) == photo_id
            ),
            None,
        )
        if idx is not None:
            self._select_idx(idx)
        self.select_photo(photo_id)

    def _select_idx(self, idx):
        if self.selected_idx is not None and 0 <= self.selected_idx < len(self.labels):
            self.labels[self.selected_idx].config(relief="flat")
        self.selected_idx = idx
        self.labels[idx].config(relief="solid")

    # SIZE CHANGE: rebuild and reflow (important for avoiding stale columns)
    def _on_size_change(self):
        size_map = {"Small": 80, "Medium": 120, "Large": 180}
        new_size = size_map.get(self.size_var.get(), 120)
        if new_size != self.thumb_size:
            self.thumb_size = new_size
            self.refresh_photos(getattr(self, "current_collection_id", None))
            # force a layout pass after the rebuild
            self.after_idle(self._reflow_grid)

    # REFLOW: compute columns fresh, clear previous columnconfigure,
    # and grid items left-to-right, wrapping as needed.
    def _reflow_grid(self):
        if not self.labels or self.single_item_active:
            return

        # sync sizes to get an accurate width
        self.update_idletasks()
        self.grid_area.update_idletasks()
        self.canvas.update_idletasks()

        container_w = max(self.grid_area.winfo_width(), self.canvas.winfo_width())
        if container_w <= 1:
            self.after(50, self._reflow_grid)
            return

        gp = self.padding
        cell_w = self.thumb_size + gp * 2 + 10  # 10px slack for borders/shadows

        # compute how many columns fit; then clamp to avoid edge overshoot
        cols = max(1, container_w // cell_w)
        while cols > 1 and (cols * cell_w + gp) > container_w:
            cols -= 1

        # CLEAR previous column configs so old widths don't linger
        if self._last_cols:
            for c in range(self._last_cols):
                try:
                    self.grid_area.columnconfigure(c, weight=0, minsize=0)
                except Exception:
                    pass

        # remove any old placements
        for fr in self.labels:
            if fr.winfo_exists():
                fr.grid_forget()

        # place items row-by-row
        for i, fr in enumerate(self.labels):
            if fr.winfo_exists():
                r, c = divmod(i, cols)
                fr.grid(row=r, column=c, padx=gp, pady=gp, sticky="n")

        # set current columns; do NOT stretch (weight=0) to prevent overshoot
        for c in range(cols):
            self.grid_area.columnconfigure(
                c, weight=0, minsize=self.thumb_size + gp * 2
            )

        self._last_cols = cols  # remember for next clear
        self.feedback_card.lift()

    # ---------------- single-photo ----------------

    def _show_single_photo(self, photo_path, photo_id):
        if callable(self.open_single_callback):
            self.open_single_callback(photo_path, photo_id)

    # ---------------- context menu ----------------

    def _ensure_context_menu(self):
        if self._ctx_menu is None:
            self._ctx_menu = tk.Menu(self, tearoff=False)
            self._ctx_menu.add_command(
                label="Delete from collection", command=self._ctx_delete_selected
            )

    def _bind_thumb_context(self, widget, photo_id: int):
        self._ensure_context_menu()
        widget._photo_id = photo_id
        widget.bind("<Button-3>", self._on_thumb_context)
        widget.bind("<Control-Button-1>", self._on_thumb_context)

    def _on_thumb_context(self, event):
        self._ensure_context_menu()
        self._ctx_photo_id = getattr(event.widget, "_photo_id", None)
        if not self._ctx_photo_id:
            return
        try:
            self._ctx_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self._ctx_menu.grab_release()

    def _ctx_delete_selected(self):
        pid = self._ctx_photo_id
        if not pid:
            return
        if not messagebox.askyesno(
            "Delete photo",
            "Remove this photo from the collection? This also removes its scores/EXIF/etc.",
        ):
            return
        try:
            self.db.delete_photo(pid)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete photo: {e}")
            return
        self.refresh_photos(getattr(self, "current_collection_id", None))

    # ---------------- LLM helpers ----------------

    def _photo_facts(self):
        collection_id = getattr(self, "current_collection_id", None)
        photos = self.db.get_photos(collection_id) or []
        facts = {"collection_id": collection_id, "count": len(photos), "photos": []}
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
            facts["photos"].append({"id": pid, "exif": exif, "scores": scores})
        return facts

    def generate_feedback_for_current(self):
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
                col_para = make_paragraph(user_prompt_collection, self._photo_facts())
                self.after(
                    0, lambda: self._set_feedback("— Collection —\n" + col_para + "\n")
                )
            except Exception as e:
                self.after(0, lambda e=e: self._set_feedback(f"LLM error: {e}"))

        threading.Thread(target=work, daemon=True).start()
