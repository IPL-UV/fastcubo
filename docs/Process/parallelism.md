# **Parallelism** 🖥️

- 📖 **Definition**: Parallelism is the execution of multiple tasks simultaneously, each on its own CPU core.
- 💻 **Example in `fastcubo`**:
  - If the system has multiple CPU cores, `ThreadPoolExecutor` allows several image downloads to run in parallel, reducing total download time.