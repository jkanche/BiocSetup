import shutil
from pathlib import Path
from typing import Optional

from pyscaffold import api
from pyscaffoldext.markdown.extension import Markdown

__author__ = "Jayaram Kancherla"
__copyright__ = "Jayaram Kancherla"
__license__ = "MIT"


def create_repository(
    project_path: str,
    description: Optional[str] = None,
    license: str = "MIT",
) -> None:
    """
    Create a new BiocPy Python package repository.

    Args:
        project_path:
            Path where the new project should be created

        description:
            Optional project description

        license:
            License to use (default: MIT)
    """
    # Create project using pyscaffold with markdown extension
    opts = {
        "project_path": project_path,
        "description": description or "Add a short description here!",
        "license": license,
        "extensions": [Markdown()],
    }
    api.create_project(**opts)

    # Get absolute path to templates directory
    template_dir = Path(__file__).parent / "templates"

    # Add GitHub Actions
    gh_actions_dir = Path(project_path) / ".github" / "workflows"
    gh_actions_dir.mkdir(parents=True, exist_ok=True)

    for workflow in ["pypi-test.yml", "pypi-publish.yml"]:
        src = template_dir / "github_workflows" / workflow
        dst = gh_actions_dir / workflow
        shutil.copy2(src, dst)

    # Add pre-commit config
    precommit_src = template_dir / "precommit" / "pre-commit-config.yaml"
    precommit_dst = Path(project_path) / ".pre-commit-config.yaml"
    shutil.copy2(precommit_src, precommit_dst)

    # Modify sphinx conf.py
    conf_py_path = Path(project_path) / "docs" / "conf.py"
    with open(conf_py_path, "r") as f:
        conf_content = f.read()

    # Add myst-nb extension and configuration
    myst_config = """
# -- Biocsetup configuration -------------------------------------------------

# Enable execution of code chunks in markdown
extensions.append('myst_nb')

# Less verbose api documentation
extensions.append('sphinx_autodoc_typehints')

autodoc_default_options = {
    "special-members": True,
    "undoc-members": True,
    "exclude-members": "__weakref__, __dict__, __str__, __module__",
}

autosummary_generate = True
autosummary_imported_members = True

html_theme = "furo"
"""

    with open(conf_py_path, "w") as f:
        f.write(conf_content + myst_config)

    # Update requirements.txt for docs
    docs_requirements = Path(project_path) / "docs" / "requirements.txt"
    with open(docs_requirements, "a") as f:
        f.write("\nmyst-nb\nfuro\nsphinx-autodoc-typehints\n")

    # Modify README
    readme_path = Path(project_path) / "README.md"
    proj_name = Path(project_path).parts[-1]

    new_readme = f"""
[![PyPI-Server](https://img.shields.io/pypi/v/{proj_name}.svg)](https://pypi.org/project/{proj_name}/)
![Unit tests](https://github.com/BiocPy/{proj_name}/actions/workflows/pypi-test.yml/badge.svg)

# {proj_name}

> {description}

A longer description of your project goes here...

## Install

To get started, install the package from [PyPI](https://pypi.org/project/{proj_name}/)

```bash
pip install {proj_name}
```

<!-- biocsetup-notes -->

## Note

This project has been set up using [BiocSetup](https://github.com/biocpy/biocsetup)
and [PyScaffold](https://pyscaffold.org/).
"""

    with open(readme_path, "w") as f:
        f.write(new_readme)

    # Modify ppyproject.toml to add ruff configuration
    pyprj_path = Path(project_path) / "pyproject.toml"
    with open(pyprj_path, "r") as f:
        pyprj_content = f.read()

    ruff_config = """
[tool.ruff]
line-length = 120
src = ["src"]
exclude = ["tests"]
extend-ignore = ["F821"]

[tool.ruff.pydocstyle]
convention = "google"

[tool.ruff.format]
docstring-code-format = true
docstring-code-line-length = 20

[tool.ruff.per-file-ignores]
"__init__.py" = ["E402", "F401"]
"""

    with open(pyprj_path, "w") as f:
        f.write(pyprj_content + ruff_config)
