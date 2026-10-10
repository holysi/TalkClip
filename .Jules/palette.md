## 2025-03-01 - Disable UI controls during async tasks
**Learning:** Users might change settings (like ASR model or refinement toggle) during background processing or recording, leading to inconsistent state or errors.
**Action:** Explicitly disable interactive Tkinter controls (`state=tk.DISABLED`) when starting an async task, and restore them (`state=tk.NORMAL`) in a `finally` block, always ensuring UI updates are thread-safe by using `self.root.after`.
## 2023-10-24 - Left-Aligning Tkinter Radio Buttons
**Learning:** By default, Tkinter `pack()` centers elements, which causes lists of radio buttons to have a jagged, hard-to-read left edge.
**Action:** Always include `anchor="w"` (and optionally `padx` for margins) when packing multiple radio buttons or checkboxes in a vertical stack to ensure a clean, readable left alignment.
## 2025-03-01 - Inline Clipboard Previews
**Learning:** Generic "Copied!" messages force users to blindly trust the clipboard content, which causes anxiety, especially for generated/transcribed text.
**Action:** Always provide a truncated inline preview of the copied content in the success notification and automatically reset the UI to its default state after a few seconds to provide immediate validation and clean up the interface.
