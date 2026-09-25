## 2025-03-01 - Disable UI controls during async tasks
**Learning:** Users might change settings (like ASR model or refinement toggle) during background processing or recording, leading to inconsistent state or errors.
**Action:** Explicitly disable interactive Tkinter controls (`state=tk.DISABLED`) when starting an async task, and restore them (`state=tk.NORMAL`) in a `finally` block, always ensuring UI updates are thread-safe by using `self.root.after`.
## 2025-03-01 - Add logical grouping and alignment for model selection
**Learning:** Using a LabelFrame in Tkinter to group related radio buttons clarifies visual hierarchy, helping users immediately identify the section's purpose without adding clunky inline labels.
**Action:** When offering multiple related toggle options (like models or formats), wrap them in a `ttk.LabelFrame` with a concise title, and left-align the options for easier scanning.
