"""
arnio — Fast CSV processing and data cleaning companion for pandas.

import arnio as ar
"""


def _resolve_version() -> str:
    """Resolve __version__ robustly for both installed and source-checkout imports.

    Strategy
    --------
    1. Try importlib.metadata first (fast path for installed distributions).
    2. If pyproject.toml exists next to the package directory, we are likely
       in a source checkout — read the version from pyproject.toml directly
       instead of trusting metadata that may belong to a different install.
    3. Fall back to importlib.metadata when no pyproject.toml is present
       (normal installed-package import).
    4. Final fallback: "unknown".
    """
    import pathlib
    import re

    _here = pathlib.Path(__file__).resolve().parent
    _pyproject = _here.parent / "pyproject.toml"

    # If pyproject.toml exists we are in a source checkout.
    # Read the version directly so we never report a stale installed version.
    if _pyproject.exists():
        try:
            _text = _pyproject.read_text(encoding="utf-8")
            _match = re.search(r'^\s*version\s*=\s*"([^"]+)"', _text, re.MULTILINE)
            if _match:
                return _match.group(1)
        except Exception:
            pass

    # Normal installed-package import: trust importlib.metadata.
    try:
        from importlib.metadata import version

        return version("arnio")
    except Exception:
        pass

    return "unknown"


__version__ = _resolve_version()
del _resolve_version

from .cleaning import (
    cast_types,
    clean,
    clean_column_names,
    clip_numeric,
    coalesce_columns,
    combine_columns,
    drop_columns,
    drop_columns_matching,
    drop_constant_columns,
    drop_duplicates,
    drop_empty_columns,
    drop_nulls,
    fill_nulls,
    filter_rows,
    keep_rows_with_nulls,
    normalize_case,
    normalize_unicode,
    normalize_whitespace,
    parse_bool_strings,
    rename_columns,
    replace_values,
    round_numeric_columns,
    safe_divide_columns,
    select_columns,
    slugify_column_names,
    standardize_missing_tokens,
    strip_whitespace,
    trim_column_names,
    validate_columns_exist,
    winsorize_outliers,
)
from .convert import from_dict, from_pandas, to_arrow, to_pandas
from .exceptions import (
    ArnioError,
    CsvReadError,
    JsonlReadError,
    PipelineStepError,
    SchemaValidationError,
    TypeCastError,
    UnknownStepError,
)
from .frame import ArFrame, ColumnSummary
from .integrations import ArnioPandasAccessor, register_duckdb
from .io import (
    read_csv,
    read_csv_chunked,
    read_jsonl,
    scan_csv,
    sniff_delimiter,
    write_csv,
    write_parquet,
)
from .pipeline import (
    PipelineContext,
    get_builtin_step_signatures,
    list_steps,
    pipeline,
    register_step,
    reset_steps,
    unregister_step,
)
from .quality import (
    CleanExplanation,
    CleaningSuggestion,
    CleanStepRecord,
    ColumnProfile,
    DataQualityReport,
    ProfileComparison,
    QualityGateIssue,
    QualityGateResult,
    auto_clean,
    check_quality_gates,
    compare_profiles,
    profile,
    suggest_cleaning,
)
from .schema import (
    URL,
    Bool,
    CountryCode,
    CurrencyCode,
    Custom,
    Date,
    DateTime,
    Email,
    Field,
    Float64,
    Int64,
    LanguageCode,
    PhoneNumber,
    Regex,
    Schema,
    SchemaDiff,
    SchemaDiffEntry,
    String,
    TimeZone,
    ValidationIssue,
    ValidationResult,
    diff_schema,
    register_validator,
    validate,
)
from .schema_export import schema_to_dict, schema_to_yaml

from_records = ArFrame.from_records

__all__ = [
    # Core class
    "ArFrame",
    "ColumnSummary",
    # I/O
    "read_csv",
    "read_csv_chunked",
    "read_jsonl",
    "write_csv",
    "write_parquet",
    "scan_csv",
    "sniff_delimiter",
    # Cleaning
    "drop_nulls",
    "drop_columns",
    "select_columns",
    "keep_rows_with_nulls",
    "fill_nulls",
    "validate_columns_exist",
    "filter_rows",
    "replace_values",
    "normalize_whitespace",
    "drop_duplicates",
    "drop_constant_columns",
    "drop_empty_columns",
    "clean_column_names",
    "clip_numeric",
    "winsorize_outliers",
    "coalesce_columns",
    "combine_columns",
    "drop_columns_matching",
    "strip_whitespace",
    "parse_bool_strings",
    "normalize_case",
    "rename_columns",
    "round_numeric_columns",
    "cast_types",
    "clean",
    "safe_divide_columns",
    "slugify_column_names",
    "trim_column_names",
    "standardize_missing_tokens",
    "CleaningSuggestion",
    # Conversion
    "to_pandas",
    "to_arrow",
    "from_pandas",
    "from_records",
    "from_dict",
    # Integrations
    "ArnioPandasAccessor",
    "register_duckdb",
    # Pipeline
    "pipeline",
    "register_step",
    "unregister_step",
    "get_builtin_step_signatures",
    "list_steps",
    "PipelineContext",
    "reset_steps",
    # Data quality
    "profile",
    "compare_profiles",
    "check_quality_gates",
    "suggest_cleaning",
    "auto_clean",
    "ColumnProfile",
    "DataQualityReport",
    "CleanStepRecord",
    "CleanExplanation",
    "ProfileComparison",
    "QualityGateIssue",
    "QualityGateResult",
    # Schema validation
    "Schema",
    "SchemaDiff",
    "SchemaDiffEntry",
    "Field",
    "ValidationIssue",
    "ValidationResult",
    "validate",
    "diff_schema",
    "Int64",
    "Float64",
    "String",
    "CountryCode",
    "CurrencyCode",
    "LanguageCode",
    "TimeZone",
    "Bool",
    "Email",
    "URL",
    "PhoneNumber",
    "DateTime",
    # Exceptions
    "UnknownStepError",
    "ArnioError",
    "CsvReadError",
    "JsonlReadError",
    "TypeCastError",
    "PipelineStepError",
    "SchemaValidationError",
    "normalize_unicode",
    "Regex",
    "Custom",
    "register_validator",
    "Date",
    "schema_to_dict",
    "schema_to_yaml",
]
