# Contributing to Our Project

Thank you for your interest in contributing to our project! We welcome
contributions from everyone and value your effort to improve the software.
Below are the guidelines which will help you get started smoothly.

## Code of Conduct

Please read our [Code of Conduct](CODE_OF_CONDUCT.md) to keep our community
approachable and respectable.

## Getting Started

Before you begin, create your github account if you don't have one. You
are strongly encouraged to setup two-factor authentication for your account.

### Setting Up Your Environment

1. **Install miniforge3**
   [Miniforge3](https://github.com/conda-forge/miniforge)
2. **Clone the repository**
   ```bash
   git clone https://github.com/AsgerJon/WorkToy.git
   cd WorkToy
   ```

3. **Create virtual environment**
    ```bash
    mamba env create -f environment.yml
    ```

4. Create a new branch:
   ```bash
   git checkout -b yourBranch
   ```
5. Push your changes:
   ```bash
   git push origin yourBranch
   ```

6. Submit a pull request through the GitHub website. Provide a
   description of the changes and improvements made. You are free to
   write a detailed comment, but frequently a short video can actually
   prove more helpful.s

### Development setup

During development, have a file called main.py in the root directory of the
project. Use this file to run the code you are working on. This will ensure
that the code is always runnable from the root directory of the project.
If you use pycharm, set the project interpreter to the newly created
environment. To run a file in the terminal using the new environment, use:

```bash  
mamba activate worktoy_env
python main.py
```

### Python Code Style

- **Indentation**: Use two spaces for indentation, not tabs.
- **Line Length**: Keep all lines to a maximum of 77 characters.
- **Naming Conventions**:
    - Variables and functions should use `camelCase`.
    - Classes should use `PascalCase`.
- **Type Hinting**: Functions should be type-hinted to clarify the expected
  type of arguments and return types.
- **Docstrings**: Every function and class should include a docstring
  describing what it does. Use triple double quotes (""") for docstrings.
- **Error Handling**: Make use of type guard checks and raise exceptions
  as appropriate.
-

### Commit Messages

- Write clear, concise commit messages in the imperative mood, like "Add
  featureX" or "Fix bugY".
- Begin the commit message with a capital letter.

### Pull Requests

- Make sure your code complies with the coding guidelines.
- Pull requests should be based on the latest version of the main branch.
- Include tests for new features and fixes when applicable.
- Provide a description of what the pull request fixes or enhances.
