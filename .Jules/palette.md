## 2024-05-24 - Disable interactive settings during global hotkey recording
**Learning:** In desktop apps with global hotkeys (like pynput), users might interact with the UI while holding the hotkey or during the async processing phase. Tkinter doesn't automatically lock the UI.
**Action:** Always explicitly disable configuration controls (radio buttons, checkboxes) when global recording/processing begins, and re-enable them in a `finally` block to prevent mid-flight state mutations and provide clear visual feedback that the app is busy.
