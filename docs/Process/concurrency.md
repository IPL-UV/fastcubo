# **Concurrency** ⚙️

- 📖 **Definition**: Concurrency is the management of multiple tasks at the same time. In `fastcubo`, it is used to handle multiple image downloads efficiently.
- 💻 **Example in `fastcubo`**:
  - `ThreadPoolExecutor` is used to manage concurrent downloads in `getPixels` and `computePixels`, allowing multiple images to be downloaded simultaneously, maximizing CPU and network usage.