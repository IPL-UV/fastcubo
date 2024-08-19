# Contributing

We welcome contributions from the community! Every contribution, no matter how small, is appreciated and credited. Here’s how you can get involved:

## How to contribute

1. **Fork the repository:** Start by forking the [FastCubo](https://github.com/IPL-UV/fastcubo) repository to your GitHub account.
2. **Clone your fork locally:**
    ```bash
    cd <directory_in_which_repo_should_be_created>
    git clone https://github.com/YOUR_GITHUB_USERNAME/fastcubo.git
    cd fastcubo
    ```
3. **Create a branch:** Create a new branch for your feature or bug fix:
    ```bash
    git checkout -b name-of-your-bugfix-or-feature
    ```
4. **Set up the environment:**
   - If you're using `pyenv`, select a Python version:
     ```bash
     pyenv local <x.y.z>
     ```
   - Install dependencies and activate the environment:
     ```bash
     poetry install
     poetry shell
     ```
   - Install pre-commit hooks:
     ```bash
     poetry run pre-commit install
     ```
5. **Make your changes:** Develop your feature or fix, ensuring you write clear, concise commit messages and include any necessary tests.
6. **Check your changes:**
   - Run formatting checks:
     ```bash
     make check
     ```
   - Run unit tests:
     ```bash
     make test
     ```
   - Optionally, run tests across different Python versions using tox:
     ```bash
     tox
     ```
7. **Submit a pull request:** Push your branch to GitHub and submit a pull request to the `develop` branch of the FastCubo repository. Ensure your pull request meets these guidelines:
   - Include tests.
   - Update the documentation if your pull request adds functionality.
   - Provide a detailed description of your changes.

## Types of contributions

- **Report bugs:** 
  - Report bugs by creating an issue on the [FastCubo GitHub repository](https://github.com/IPL-UV/fastcubo/issues). Please include your operating system, setup details, and steps to reproduce the bug.
- **Fix bugs:** Look for issues tagged with "bug" and "help wanted" in the repository to start fixing.
- **Implement features:** Contribute by implementing features tagged with "enhancement" and "help wanted."
- **Write documentation:** Contribute to the documentation in the official docs, docstrings, or through blog posts and articles.
- **Submit feedback:** Propose new features or give feedback by filing an issue on GitHub. 
  - Use the [FastCubo GitHub issues page](https://github.com/IPL-UV/fastcubo/issues) for feedback.

## Acknowledgements

We are grateful to our contributors for their efforts in making FastCubo better:

| [![Bautista Lesly](https://avatars.githubusercontent.com/u/54723897?v=4)](https://github.com/leslybautista) | [![Espinoza Wendy](https://avatars.githubusercontent.com/u/77112851)](https://github.com/Wendy-cuak) | [![Fernando Prudencio](https://avatars.githubusercontent.com/u/49989177)](https://github.com/fernandoprudencio) |
|:---:|:---:|:---:|
| [Bautista Lesly](https://github.com/leslybautista) | [Espinoza Wendy](https://github.com/Wendy-cuak) | [Fernando Prudencio](https://github.com/fernandoprudencio) |
| [![Yali Roy](https://avatars.githubusercontent.com/u/20345946)](https://github.com/ryali93) | [![Aybar Cesar](https://avatars.githubusercontent.com/u/16768318)](https://github.com/csaybar/) | [![Gomez-Chova Luis](https://avatars.githubusercontent.com/u/77457082)](https://github.com/luisgomezchova) |
| [Yali Roy](https://github.com/ryali93) | [Aybar Cesar](https://github.com/csaybar/) | [Gomez-Chova Luis](https://github.com/luisgomezchova) |
| [![David Montero](https://avatars.githubusercontent.com/u/49817852?v=4)](https://github.com/davemlz) | [![Julio Contreras](https://avatars.githubusercontent.com/u/126512018?v=4)](https://github.com/JulioContrerasH) | [![Jeanett Valladares](https://avatars.githubusercontent.com/u/86890658?v=4)](https://github.com/jeanevh) |
| [David Montero](https://github.com/davemlz) | [Julio Contreras](https://github.com/JulioContrerasH) | [Jeanett Valladares](https://github.com/jeanevh) ||

Thank you to all our contributors! Your hard work and dedication make FastCubo possible.
