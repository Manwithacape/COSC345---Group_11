# single_photo_viewer.py
import ttkbootstrap as ttk
from PIL import Image, ImageTk
from main_viewer import MainViewer
from tkinter.scrolledtext import ScrolledText  # NEW
from llm_feedback import make_paragraph
from progress_dialog import ProgressDialog
import threading


class SinglePhotoViewer(MainViewer):
    """
    Shows one photo scaled-to-fit and centered directly on the Canvas,
    with an LLM feedback box pinned at the bottom-left.
    """

    def __init__(self, parent, db, photo_path=None, photo_id=None, **kwargs):
        kwargs.pop("photo_path", None)
        super().__init__(parent, **kwargs)

        self.db = db
        self.photo_id = photo_id

        # enter single-photo mode
        self.single_item_active = True

        # hide the grid layer and scrollbar in single view
        try:
            self.canvas.itemconfigure(self.window_id, state="hidden")
        except Exception:
            pass
        try:
            self.scrollbar_y.pack_forget()
        except Exception:
            pass

        self.canvas.configure(highlightthickness=0, bg="#222")

        # image state
        self.photo_path = None
        self._orig_img = None
        self._img_tk = None
        self._img_item = None

        # redraw when the canvas resizes
        self.canvas.bind("<Configure>", self._on_resize)

        # ---------- LLM FEEDBACK BOX (bottom-left overlay) ----------
        self.feedback_card = ttk.Labelframe(
            self,
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

        self.feedback_card.place(
            relx=0.0, rely=1.0, x=12, y=-12, anchor="sw", width=360
        )
        self.feedback_card.lift()
        # ------------------------------------------------------------

        def _set_feedback(text: str):
            self.feedback_box.configure(state="normal")
            self.feedback_box.delete("1.0", "end")
            self.feedback_box.insert("1.0", text)
            self.feedback_box.configure(state="disabled")

        self._set_feedback = _set_feedback

        if photo_path:
            self.load_image(photo_path)

    def load_image(self, photo_path: str):
        """Load the image and render to fit canvas."""
        try:
            self.photo_path = photo_path
            self._orig_img = Image.open(photo_path).convert("RGBA")
            self._render_fit()
        except Exception as e:
            print(f"[SinglePhotoViewer] Failed to load {photo_path}: {e}")

    def _on_resize(self, _event=None):
        if self._orig_img is not None:
            self._render_fit()
        # keep feedback card on top
        try:
            self.feedback_card.lift()
        except Exception:
            pass

    def _render_fit(self):
        """Scale image to fit canvas while preserving aspect ratio and center it."""
        cw = max(1, self.canvas.winfo_width())
        ch = max(1, self.canvas.winfo_height())
        iw, ih = self._orig_img.size

        scale = min(cw / iw, ch / ih)
        new_w = max(1, int(iw * scale))
        new_h = max(1, int(ih * scale))

        img_resized = self._orig_img.resize((new_w, new_h), Image.LANCZOS)
        self._img_tk = ImageTk.PhotoImage(img_resized)

        if self._img_item is not None:
            self.canvas.delete(self._img_item)

        cx, cy = cw // 2, ch // 2
        self._img_item = self.canvas.create_image(
            cx, cy, image=self._img_tk, anchor="center"
        )
        self.canvas.tag_raise(self._img_item)

        # no scrolling in fit view
        self.canvas.config(scrollregion=(0, 0, cw, ch))

    def restore_grid_layer(self):
        """Optional: restore grid mode."""
        self.single_item_active = False
        try:
            self.canvas.itemconfigure(self.window_id, state="normal")
        except Exception:
            pass

    # -----------LLM Helper Methods-----------
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
        pid = self.photo_id
        facts = {
            "collection_id": collection_id,
            "count": 1 if pid is not None else 0,
            "photos": [],
        }

        if pid is not None:
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

            facts["photos"].append(
                {
                    "id": pid,
                    "exif": exif,
                    "scores": scores,
                }
            )

        return facts

    def generate_feedback_for_current(self):
        """Called by the 'Generate feedback' button."""
        if self.photo_id is None and not self.photo_path:
            self._set_feedback("No photo loaded.")
            return

        collection_id = getattr(self, "current_collection_id", None)

        # Note: keep as a single string (no commas) to avoid tuple creation
        user_prompt_photo = (
            "Write a short paragraph (3–5 sentences) assessing the selected photo. "
            "If constructive feedback can be given do so, act as if you are a photography teacher. "
            "Use only the provided facts (EXIF + numeric scores). "
            "Do not mention anything about resolution. "
            "If a detail is missing, state 'insufficient data' rather than assuming. "
            "Do not invent camera settings, locations, or subjects."
        )

        # Show loading dialog and disable the button while generating
        try:
            self.gen_btn.configure(state="disabled")
        except Exception:
            pass
        pd = ProgressDialog(
            self,
            title="Generating feedback",
            message="Asking AI for feedback...",
            indeterminate=True,
        )

        def work():
            try:
                para = make_paragraph(user_prompt_photo, self._photo_facts())
                out = [para, ""]
                def on_ok():
                    try:
                        self._set_feedback("\n".join(out))
                    finally:
                        try:
                            pd.finish(success=True)
                        except Exception:
                            pass
                        try:
                            self.gen_btn.configure(state="normal")
                        except Exception:
                            pass
                self.after(0, on_ok)
            except Exception as e:
                def on_err(e=e):
                    try:
                        self._set_feedback(f"LLM error: {e}")
                    finally:
                        try:
                            pd.finish(success=False, error=str(e))
                        except Exception:
                            pass
                        try:
                            self.gen_btn.configure(state="normal")
                        except Exception:
                            pass
                self.after(0, on_err)

        threading.Thread(target=work, daemon=True).start()
