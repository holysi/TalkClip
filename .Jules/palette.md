## 2024-09-04 - Tkinter Default Contrast and Alignment Issues
**Learning:** Default Tkinter `"gray"` text fails WCAG AA contrast ratio against the standard window background. Also, default `pack()` without `anchor` centers elements, which makes reading options harder (violates F-pattern scannability).
**Action:** When using Tkinter, avoid default `"gray"` and use darker hex values (like `"#555555"`) for hint text. Group related options (like radio buttons/checkboxes) into a `tk.Frame` and `pack(anchor="w")` to left-align them for better scannability.
