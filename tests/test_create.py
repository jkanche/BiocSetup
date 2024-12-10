import os
import tempfile
from pathlib import Path

import pytest

from biocsetup.create_repository import create_repository

__author__ = "Jayaram Kancherla"
__copyright__ = "Jayaram Kancherla"
__license__ = "MIT"

@pytest.fixture
def temp_dir():
    """Create a temporary directory for testing."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir

def test_create_repository(temp_dir):
    """Test basic repository creation."""
    project_name = "test_project"
    project_path = os.path.join(temp_dir, project_name)

    create_repository(
        project_path=project_path,
        description="Test project",
    )

    # Check if basic structure is created
    assert os.path.exists(project_path)
    assert os.path.exists(os.path.join(project_path, "src"))
    assert os.path.exists(os.path.join(project_path, "docs"))

    # Check if GitHub Actions are added
    assert os.path.exists(
        os.path.join(project_path, ".github", "workflows", "pypi-test.yml")
    )
    assert os.path.exists(
        os.path.join(project_path, ".github", "workflows", "pypi-publish.yml")
    )

    # Check if pre-commit config is added
    assert os.path.exists(os.path.join(project_path, ".pre-commit-config.yaml"))

    # Check if sphinx conf.py is modified
    conf_py = Path(project_path) / "docs" / "conf.py"
    assert conf_py.exists()

    with open(conf_py, "r") as f:
        content = f.read()
        assert "myst_nb" in content
        assert "furo" in content

    # Check if readme is modified
    readme_py = Path(project_path) / "README.md"
    assert readme_py.exists()
    with open(readme_py, "r") as f:
        content = f.read()
        assert "biocsetup" in content

def test_create_repository_with_description(temp_dir):
    """Test repository creation with custom description."""
    project_path = os.path.join(temp_dir, "test-desc-project")
    description = "Custom project description"

    create_repository(
        project_path=project_path,
        description=description,
    )

    readme_path = Path(project_path) / "README.md"
    with open(readme_path, "r") as f:
        content = f.read()
        assert description in content

def test_create_repository_with_license(temp_dir):
    """Test repository creation with custom license."""
    project_path = os.path.join(temp_dir, "test-license-project")
    license = "BSD"

    create_repository(
        project_path=project_path,
        license=license,
    )

    setup_cfg = Path(project_path) / "setup.cfg"
    with open(setup_cfg, "r") as f:
        content = f.read()
        assert license in content
