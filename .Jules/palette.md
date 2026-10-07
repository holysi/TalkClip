## 2025-03-01 - Disable UI controls during async tasks
**Learning:** Users might change settings (like ASR model or refinement toggle) during background processing or recording, leading to inconsistent state or errors.
**Action:** Explicitly disable interactive Tkinter controls (`state=tk.DISABLED`) when starting an async task, and restore them (`state=tk.NORMAL`) in a `finally` block, always ensuring UI updates are thread-safe by using `self.root.after`.
## 2023-10-24 - Left-Aligning Tkinter Radio Buttons
**Learning:** By default, Tkinter `pack()` centers elements, which causes lists of radio buttons to have a jagged, hard-to-read left edge.
**Action:** Always include `anchor="w"` (and optionally `padx` for margins) when packing multiple radio buttons or checkboxes in a vertical stack to ensure a clean, readable left alignment.

## 2026-10-07 - Clipboard Feedback Truncation
**Learning:** Users need immediate validation of what was copied to the clipboard, but full text can break UI layouts or overwhelm the user. Truncated previews provide validation without clutter, and auto-hiding returns the UI to a clean state.
**Action:** Implement truncated inline previews (e.g., first 15 chars + '...') that auto-hide after a few seconds instead of static 'Copied!' messages for clipboard operations.
