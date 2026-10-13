import json
import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"

sys.path.insert(0, str(SRC_DIR))

from xsd_schema_converter.SchemaConverter import (
    convert_xsd_string_to_openapi,
    map_xsd_type_to_json,
)


def test_supported_primitive_type_mappings():
    assert map_xsd_type_to_json("xs:string") == ("string", None)
    assert map_xsd_type_to_json("xs:int") == ("integer", "int32")
    assert map_xsd_type_to_json("xs:long") == ("integer", "int64")
    assert map_xsd_type_to_json("xs:boolean") == ("boolean", None)
    assert map_xsd_type_to_json("xs:decimal") == ("number", "float")


def test_example_conversion_matches_expected_schema():
    xsd_path = PROJECT_ROOT / "examples" / "basic.xsd"
    expected_path = PROJECT_ROOT / "examples" / "expected_schema.json"

    xsd_content = xsd_path.read_text(encoding="utf-8")
    expected = json.loads(
        expected_path.read_text(encoding="utf-8")
    )

    actual = convert_xsd_string_to_openapi(xsd_content)

    assert actual == expected


def test_optional_age_is_not_required():
    xsd_path = PROJECT_ROOT / "examples" / "basic.xsd"
    xsd_content = xsd_path.read_text(encoding="utf-8")

    result = convert_xsd_string_to_openapi(xsd_content)
    person_schema = result["components"]["schemas"]["PersonType"]

    assert "Age" in person_schema["properties"]
    assert "Age" not in person_schema.get("required", [])