## 2024-05-18 - Prevent Configuration Changes During Processing
**Learning:** Interactive Tkinter components (like radio buttons or checkboxes) must be disabled during asynchronous background processes (e.g., audio recording and API processing) to prevent the user from altering the configuration mid-task and causing unpredictable application states.
**Action:** Use `state=tk.DISABLED` when a task begins, and ensure `state=tk.NORMAL` is called in a `finally` block when the task completes (delegating to the main thread with `self.root.after()` if necessary).
