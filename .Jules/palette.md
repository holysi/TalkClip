## 2025-03-01 - Disable UI controls during async tasks
**Learning:** Users might change settings (like ASR model or refinement toggle) during background processing or recording, leading to inconsistent state or errors.
**Action:** Explicitly disable interactive Tkinter controls (`state=tk.DISABLED`) when starting an async task, and restore them (`state=tk.NORMAL`) in a `finally` block, always ensuring UI updates are thread-safe by using `self.root.after`.
## 2023-10-24 - Left-Aligning Tkinter Radio Buttons
**Learning:** By default, Tkinter `pack()` centers elements, which causes lists of radio buttons to have a jagged, hard-to-read left edge.
**Action:** Always include `anchor="w"` (and optionally `padx` for margins) when packing multiple radio buttons or checkboxes in a vertical stack to ensure a clean, readable left alignment.
## 2024-05-08 - Inline Clipboard Preview
**Learning:** Generic "Copied!" messages force users to paste the content elsewhere to verify what was actually transcribed, creating friction in voice-to-text workflows.
**Action:** Implemented a truncated inline preview (e.g., "已複製: [preview]...") that automatically resets to the ready state, providing immediate visual validation and maintaining a clean UI for the next interaction.
