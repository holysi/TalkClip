## 2024-05-20 - Prevent Mid-Task UI Configuration Changes
**Learning:** Interactive Tkinter UI controls (like radio buttons or checkboxes) must be disabled during asynchronous tasks (such as recording or background processing) to prevent users from changing state while an operation is in progress.
**Action:** Always disable (`state=tk.DISABLED`) UI controls at the start of an async operation and re-enable them (`state=tk.NORMAL`) inside a `finally` block to guarantee they are restored even on error.
