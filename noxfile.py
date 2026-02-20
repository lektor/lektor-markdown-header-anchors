# /// script
# dependencies = ["nox"]
# ///
from collections.abc import Iterable

import nox

nox.options.default_venv_backend = "uv|venv"


pyproject = nox.project.load_toml("pyproject.toml")
dependencies = pyproject.get("project", {}).get("dependencies", [])
dev_dependencies = pyproject.get("dependency-groups", {}).get("dev", [])


@nox.session(
    python=["3.10", "3.11", "3.12", "3.13", "3.14"],
    requires=["cover_clean"],
)
@nox.parametrize("pins", [
    nox.param(("lektor==3.3.*",), id="lektor33"),
    nox.param(("lektor==3.4.*,>=3.4.0b1", "mistune==2.*"), id="lektor34-mistune2"),
    nox.param(("lektor==3.4.*,>=3.4.0b1", "mistune==0.*"), id="lektor34-mistune0"),
])
def pytest(s: nox.Session, pins: Iterable[str]) -> None:
    """Run pytest tests."""
    s.install(".", "coverage", "pytest", *dependencies, *dev_dependencies, *pins)
    s.run("coverage", "run", "--append", "-m", "pytest", "tests", "-ra")
    s.notify("cover_report")


@nox.session
def cover_clean(s: nox.Session) -> None:
    """Erase any existing coverage data."""
    s.install("coverage")
    s.run("coverage", "erase")


@nox.session
def cover_report(s: nox.Session) -> None:
    """Report cumulative code coverage status."""
    s.install("coverage")
    s.run("coverage", "html")
    s.run("coverage", "report", "--show-missing")


if __name__ == "__main__":
    nox.main()
