## 2025-03-01 - Disable UI controls during async tasks
**Learning:** Users might change settings (like ASR model or refinement toggle) during background processing or recording, leading to inconsistent state or errors.
**Action:** Explicitly disable interactive Tkinter controls (`state=tk.DISABLED`) when starting an async task, and restore them (`state=tk.NORMAL`) in a `finally` block, always ensuring UI updates are thread-safe by using `self.root.after`.
## 2023-10-24 - Left-Aligning Tkinter Radio Buttons
**Learning:** By default, Tkinter `pack()` centers elements, which causes lists of radio buttons to have a jagged, hard-to-read left edge.
**Action:** Always include `anchor="w"` (and optionally `padx` for margins) when packing multiple radio buttons or checkboxes in a vertical stack to ensure a clean, readable left alignment.

## 2024-05-20 - Inline Clipboard Preview with Auto-Hide
**Learning:** Users benefit from immediate validation of what was copied to the clipboard rather than a generic success message, and auto-hiding the notification reduces UI clutter for repeated actions.
**Action:** For clipboard operations, display a truncated preview of the copied content and automatically reset the notification status after a few seconds using a managed timer.
