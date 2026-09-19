## 2024-05-18 - Disable Controls During Processing
**Learning:** Disabling interactive UI controls in desktop apps during async processing prevents mid-task configuration changes and race conditions.
**Action:** Implement a method to toggle UI control states (e.g., DISABLED/NORMAL) around asynchronous tasks like recording and model inference.
