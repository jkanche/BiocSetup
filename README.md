[![PyPI-Server](https://img.shields.io/pypi/v/biocsetup.svg)](https://pypi.org/project/biocsetup/)
![Unit tests](https://github.com/BiocPy/BiocSetup/actions/workflows/pypi-test.yml/badge.svg)
[![Project generated with PyScaffold](https://img.shields.io/badge/-PyScaffold-005CA0?logo=pyscaffold)](https://pyscaffold.org/)

# BiocSetup

BiocSetup helps scaffold new Python packages in [BiocPy](https://github.com/biocpy) with consistent configuration for package management.

It automates the setup process by using PyScaffold with additional configurations specific to BiocPy projects, including documentation setup, GitHub Actions for testing and publishing, and code quality tools.

For more details, see our [developer guide](https://github.com/BiocPy/developer_guide).

## Installation

```bash
pip install biocsetup
```

## Usage

### Command Line Interface

Create a new package using the command line:

```bash
biocsetup my-new-package --description "Description of my package" --license MIT
```

Options:
- `--description`, `-d`: Project description
- `--license`, `-l`: License to use (default: MIT)

### Python API

You can also create packages programmatically:

```python
from biocsetup import create_repository

create_repository(
    project_path="my-new-package",
    description="Description of my package",
    license="MIT"
)
```

<!-- pyscaffold-notes -->

## Note

This project has been set up using PyScaffold 4.6. For details and usage
information on PyScaffold see https://pyscaffold.org/.
