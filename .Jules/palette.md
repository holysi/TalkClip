## 2024-09-16 - Prevent UI interaction during async audio processing
**Learning:** Interactive Tkinter controls (like radio buttons or checkboxes) must be disabled (`state=tk.DISABLED`) during asynchronous tasks such as recording or background processing, and re-enabled (`state=tk.NORMAL`) in a `finally` block to prevent mid-task configuration changes.
**Action:** Add disable/enable methods and hook them up to the recording start and completion.
