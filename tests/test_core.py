import importlib
import sys

import pytest


def test_missing_cpp_extension_error_message(monkeypatch):
    """Ensure that a missing _arnio_cpp extension raises an ImportError with a helpful message."""
    try:
        import arnio  # noqa: F401
    except ImportError as e:
        # If arnio is already failing to import due to missing extension (like in local tests)
        error_msg = str(e)
    else:
        # If it is installed, we force it to fail
        monkeypatch.setitem(sys.modules, "arnio._arnio_cpp", None)
        monkeypatch.delitem(sys.modules, "arnio._core", raising=False)
        with pytest.raises(ImportError) as exc_info:
            importlib.import_module("arnio._core")
        error_msg = str(exc_info.value)

    assert "arnio C++ extension (_arnio_cpp) not found" in error_msg
    assert "pip install -e ." in error_msg
    assert "Desktop development with C++" in error_msg
    assert "gcc or clang" in error_msg


# ---------------------------------------------------------------------------
# Regression tests for issue #1892:
# __version__ must reflect the source checkout, not a stale installed dist.
# ---------------------------------------------------------------------------


def test_version_is_string():
    """arnio.__version__ must always be a non-empty string."""
    import arnio

    assert isinstance(arnio.__version__, str)
    assert len(arnio.__version__) > 0


def test_version_not_unknown_on_installed_package():
    """In a normal test environment (package installed) version must not be 'unknown'."""
    import arnio

    assert (
        arnio.__version__ != "unknown"
    ), "__version__ fell through to 'unknown' even though arnio is installed"


def test_version_reads_pyproject_in_source_checkout(tmp_path):
    """When pyproject.toml sits next to the package dir, its version is used."""
    import importlib.util
    import pathlib

    # Copy the version-resolution block from the real __init__.py into a tmp package.
    real_init = pathlib.Path(__file__).parent.parent / "arnio" / "__init__.py"
    src = real_init.read_text(encoding="utf-8")
    version_block = src[: src.index("from .")]

    pkg_dir = tmp_path / "arnio"
    pkg_dir.mkdir()
    (pkg_dir / "__init__.py").write_text(version_block, encoding="utf-8")

    # Place a pyproject.toml with a sentinel version next to the package dir.
    (tmp_path / "pyproject.toml").write_text(
        '[project]\nname = "arnio"\nversion = "9.9.9"\n', encoding="utf-8"
    )

    spec = importlib.util.spec_from_file_location(
        "arnio_checkout", pkg_dir / "__init__.py"
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    assert (
        mod.__version__ == "9.9.9"
    ), f"Expected '9.9.9' from pyproject.toml, got {mod.__version__!r}"


def test_version_fallback_unknown_when_no_pyproject_and_no_metadata(
    tmp_path, monkeypatch
):
    """When neither pyproject.toml nor metadata is available, fall back to 'unknown'."""
    import importlib.metadata
    import importlib.util
    import pathlib

    real_init = pathlib.Path(__file__).parent.parent / "arnio" / "__init__.py"
    src = real_init.read_text(encoding="utf-8")
    version_block = src[: src.index("from .")]

    pkg_dir = tmp_path / "arnio"
    pkg_dir.mkdir()
    (pkg_dir / "__init__.py").write_text(version_block, encoding="utf-8")
    # No pyproject.toml — simulates an install without source tree.

    monkeypatch.setattr(
        importlib.metadata,
        "version",
        lambda name: (_ for _ in ()).throw(
            importlib.metadata.PackageNotFoundError(name)
        ),
    )

    spec = importlib.util.spec_from_file_location(
        "arnio_isolated", pkg_dir / "__init__.py"
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    assert mod.__version__ == "unknown", f"Expected 'unknown', got {mod.__version__!r}"
