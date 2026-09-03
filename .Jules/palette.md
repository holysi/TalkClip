## 2024-05-24 - Grouping related options with LabelFrame
**Learning:** In desktop UI (Tkinter), floating radio buttons without a visual or semantic group boundary increase cognitive load, much like form inputs without `<fieldset>` in HTML.
**Action:** Always wrap related options (like model selection) in a `ttk.LabelFrame` and align them (`anchor="w"`) for better scannability and structural clarity.
