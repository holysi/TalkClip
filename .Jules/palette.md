## 2024-05-18 - Disable interactive elements during async tasks in Tkinter UIs
**Learning:** Background asynchronous tasks (like recording and processing) in Tkinter UIs can result in inconsistent state changes if users interact with UI elements during the process.
**Action:** Always disable interactive Tkinter controls (like radio buttons or checkboxes) during asynchronous tasks and re-enable them in a `finally` block to prevent mid-task configuration changes. Ensure these UI modifications from background threads are safely delegated to the main thread using `self.root.after(0, ...)`.
