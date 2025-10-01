import pytest
from jsonschema import validate, ValidationError
from helpers import load_local_schema

# Load the schema
schema = load_local_schema("tests/tools_validation_schema.json")

# 1. A tool that should pass validation
valid_tool = {
  "type": "SoftwareApplication",
  "name": "Black",
  "description": "Deterministic Python code formatter that enforces consistent coding style across software projects, improving code readability, maintainability, and collaboration in research teams.",
  "url": "https://github.com/psf/black",
  "applicationCategory": "CodeQuality",
  "hasQualityDimension": [
    "Maintainability"
  ],
  "ring": "Adopt",
  "segment": "Software engineering & development practices"
}

# 2. Tools that should not pass validation
invalid_tools = [
    # Missing required property: name
    {
  "type": "SoftwareApplication",
  "description": "Deterministic Python code formatter that enforces consistent coding style across software projects, improving code readability, maintainability, and collaboration in research teams.",
  "url": "https://github.com/psf/black",
  "applicationCategory": "CodeQuality",
  "hasQualityDimension": [
    "Maintainability"
  ],
  "ring": "Adopt",
  "segment": "Software engineering & development practices"
},
    # Missing required property: description
    {
  "type": "SoftwareApplication",
  "name": "Black",
  "url": "https://github.com/psf/black",
  "applicationCategory": "CodeQuality",
  "hasQualityDimension": [
    "Maintainability"
  ],
  "ring": "Adopt",
  "segment": "Software engineering & development practices"
}, 
    # Missing required property: url
    {
  "type": "SoftwareApplication",
  "name": "Black",
  "description": "Deterministic Python code formatter that enforces consistent coding style across software projects, improving code readability, maintainability, and collaboration in research teams.",
  "applicationCategory": "CodeQuality",
  "hasQualityDimension": [
    "Maintainability"
  ],
  "ring": "Adopt",
  "segment": "Software engineering & development practices"
},
    # Invalid applicationCategory
    {
  "type": "SoftwareApplication",
  "name": "Black",
  "description": "Deterministic Python code formatter that enforces consistent coding style across software projects, improving code readability, maintainability, and collaboration in research teams.",
  "url": "https://github.com/psf/black",
  "hasQualityDimension": [
    "Maintainability"
  ],
  "ring": "Adopt",
  "segment": "Software engineering & development practices"
}
]


def test_valid_tool():
    """Tests that a valid tool passes validation."""
    validate(instance=valid_tool, schema=schema)


@pytest.mark.parametrize("tool", invalid_tools)
def test_invalid_tools(tool):
    """Tests that invalid tools fail validation."""
    with pytest.raises(ValidationError):
        validate(instance=tool, schema=schema)
