## 2026-09-09 - Disable UI Controls During Async Tasks
**Learning:** Disabling interactive UI controls (like radio buttons and checkboxes) during asynchronous tasks (such as recording or processing) prevents users from making mid-task configuration changes that could cause errors or unexpected behavior.
**Action:** Always ensure that interactive UI elements are disabled using `state=tk.DISABLED` when an async task starts and safely re-enabled using `state=tk.NORMAL` in a `finally` block when the task completes.
