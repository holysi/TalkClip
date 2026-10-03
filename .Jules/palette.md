## 2025-03-01 - Disable UI controls during async tasks
**Learning:** Users might change settings (like ASR model or refinement toggle) during background processing or recording, leading to inconsistent state or errors.
**Action:** Explicitly disable interactive Tkinter controls (`state=tk.DISABLED`) when starting an async task, and restore them (`state=tk.NORMAL`) in a `finally` block, always ensuring UI updates are thread-safe by using `self.root.after`.
## 2023-10-24 - Left-Aligning Tkinter Radio Buttons
**Learning:** By default, Tkinter `pack()` centers elements, which causes lists of radio buttons to have a jagged, hard-to-read left edge.
**Action:** Always include `anchor="w"` (and optionally `padx` for margins) when packing multiple radio buttons or checkboxes in a vertical stack to ensure a clean, readable left alignment.
## 2024-10-03 - Inline Validation Preview Notification
**Learning:** Showing a static "Copied!" message doesn't provide immediate validation that the correct content was copied, and leaving it on screen creates an inconsistent state.
**Action:** Show a truncated preview inline directly in the notification and automatically clear it after a short delay (e.g. 3s) using a cancelable timeout.
