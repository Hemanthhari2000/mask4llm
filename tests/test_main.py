import re
from typing import NamedTuple

import pytest

from mask4llm.masking import mask, unmask


class MaskParamTestType(NamedTuple):
    text: str
    patterns: str
    expected_keys: list[str]


class UnMaskParamTestType(NamedTuple):
    masked_text: str
    mask_map: dict[str, str]
    expected: str


mask_param_test_cases = [
    MaskParamTestType(
        "Hello, my name is Locke. John Locke",
        r"John Locke",
        ["John Locke"],
    ),
    MaskParamTestType(
        "Hello, my name is Locke. John Locke",
        r"Locke",
        ["Locke"],
    ),
    MaskParamTestType(
        "Email: user@example.com, Ph: 123-45-6789",
        r"\d{3}-\d{2}-\d{4}|\w+@\w+\.\w+",
        ["user@example.com", "123-45-6789"],
    ),
    MaskParamTestType(
        "Sensitive: abc123abc",
        r"abc|abc123abc",
        ["abc"],
    ),
    MaskParamTestType(
        "This is a safe content.",
        r"notfound",
        [],
    ),
    MaskParamTestType(
        "",
        r".*",
        [],
    ),
    MaskParamTestType(
        "",
        r"",
        [],
    ),
    MaskParamTestType(
        "some text",
        r"",
        [],
    ),
    MaskParamTestType(
        "Path: /usr/bin/env; Token: $HOME",
        r"/usr/bin/env|\$HOME",
        ["/usr/bin/env", "$HOME"],
    ),
    MaskParamTestType(
        "Contact: john.doe@email.com or jane.smith@company.org",
        r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
        ["john.doe@email.com", "jane.smith@company.org"],
    ),
    MaskParamTestType(
        "Phone: (555) 123-4567, SSN: 123-45-6789",
        r"\(\d{3}\) \d{3}-\d{4}|\d{3}-\d{2}-\d{4}",
        ["(555) 123-4567", "123-45-6789"],
    ),
    MaskParamTestType(
        "IP addresses: 192.168.1.1 and 10.0.0.1",
        r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b",
        ["192.168.1.1", "10.0.0.1"],
    ),
    MaskParamTestType(
        "Names: José María, François, and Müller",
        r"\b[A-Za-zÀ-ÿ]+\b",
        ["Names", "José", "María", "François", "and", "Müller"],
    ),
    MaskParamTestType(
        "Credit cards: 4111-1111-1111-1111, 5555 6666 7777 8888",
        r"\b\d{4}[- ]\d{4}[- ]\d{4}[- ]\d{4}\b",
        ["4111-1111-1111-1111", "5555 6666 7777 8888"],
    ),
    MaskParamTestType(
        "URLs: https://example.com and http://test.org/path",
        r"https?://[^\s]+",
        ["https://example.com", "http://test.org/path"],
    ),
    MaskParamTestType(
        "API keys: sk-1234567890abcdef, pk_test_abcdef123456",
        r"\bsk-\w+|\bpk_\w+",
        ["sk-1234567890abcdef", "pk_test_abcdef123456"],
    ),
    MaskParamTestType(
        "Overlapping: aaa bbb aaa",
        r"aaa|bbb",
        ["aaa", "bbb"],
    ),
    MaskParamTestType(
        "Case sensitive: Test TEST test",
        r"(?i)test",
        ["Test", "TEST", "test"],
    ),
    MaskParamTestType(
        "Very long text with sensitive data" * 100,
        r"sensitive data",
        ["sensitive data"],
    ),
]

unmask_param_test_cases = [
    UnMaskParamTestType(
        "My password is <<MASK_abc123>>",
        {"secret": "<<MASK_abc123>>"},
        "My password is secret",
    ),
    UnMaskParamTestType(
        "Secrets: <<MASK_aaa111>>, <<MASK_bbb222>>",
        {"foo": "<<MASK_aaa111>>", "bar": "<<MASK_bbb222>>"},
        "Secrets: foo, bar",
    ),
    UnMaskParamTestType(
        "<<MASK_aaa111>> loves <<MASK_aaa111>>",
        {"John": "<<MASK_aaa111>>"},
        "John loves John",
    ),
    UnMaskParamTestType(
        "Nothing to unmask here",
        {"secret": "<<MASK_xyz>>"},
        "Nothing to unmask here",
    ),
    UnMaskParamTestType(
        "<<MASK_1>> and <<MASK_2>> are different",
        {"one": "<<MASK_1>>", "two": "<<MASK_2>>"},
        "one and two are different",
    ),
    UnMaskParamTestType(
        "User: <<MASK_abc123>>, Email: <<MASK_def456>>",
        {"john.doe": "<<MASK_abc123>>", "john@example.com": "<<MASK_def456>>"},
        "User: john.doe, Email: john@example.com",
    ),
    UnMaskParamTestType(
        "Multiple <<MASK_xyz789>> occurrences <<MASK_xyz789>> here",
        {"SECRET": "<<MASK_xyz789>>"},
        "Multiple SECRET occurrences SECRET here",
    ),
    UnMaskParamTestType(
        "Empty mask map test",
        {},
        "Empty mask map test",
    ),
    UnMaskParamTestType(
        "No masks in text",
        {"key": "<<MASK_value>>"},
        "No masks in text",
    ),
    UnMaskParamTestType(
        "<<MASK_111111>> <<MASK_222222>> <<MASK_333333>>",
        {"first": "<<MASK_111111>>", "second": "<<MASK_222222>>", "third": "<<MASK_333333>>"},
        "first second third",
    ),
    UnMaskParamTestType(
        "Complex: <<MASK_a1b2c3>> and <<MASK_d4e5f6>> with text",
        {"José María": "<<MASK_a1b2c3>>", "François Müller": "<<MASK_d4e5f6>>"},
        "Complex: José María and François Müller with text",
    ),
    UnMaskParamTestType(
        "URLs: <<MASK_url111>> and <<MASK_url222>>",
        {"https://example.com": "<<MASK_url111>>", "http://test.org/path": "<<MASK_url222>>"},
        "URLs: https://example.com and http://test.org/path",
    ),
    UnMaskParamTestType(
        "API keys: <<MASK_sk123>> and <<MASK_pk456>>",
        {"sk-1234567890abcdef": "<<MASK_sk123>>", "pk_test_abcdef123456": "<<MASK_pk456>>"},
        "API keys: sk-1234567890abcdef and pk_test_abcdef123456",
    ),
]


def is_valid_mask_format(mask: str) -> bool:
    return re.fullmatch(r"<<MASK_[a-f0-9]{6}>>", mask) is not None


@pytest.mark.parametrize("mask_case", mask_param_test_cases)
def test_mask_replaces_expected_patterns(mask_case: MaskParamTestType) -> None:
    text, patterns, expected_keys = mask_case
    masked_text, masks = mask(text, patterns)

    for key in expected_keys:
        assert key not in masked_text
        assert key in masks
        assert is_valid_mask_format(masks[key])

    assert set(masks.keys()) == set(expected_keys)


@pytest.mark.parametrize("unmask_case", unmask_param_test_cases)
def test_unmask(unmask_case: UnMaskParamTestType) -> None:
    masked_text, mask_map, expected = unmask_case
    assert unmask(masked_text, mask_map) == expected


def test_mask_preserves_text_structure() -> None:
    """Test that masking preserves the overall text structure."""
    text = "Hello world! This is a test."
    patterns = r"world"
    masked_text, masks = mask(text, patterns)

    # Original structure should be preserved except for masked words
    assert "Hello" in masked_text
    assert "!" in masked_text
    assert "This is a test." in masked_text
    assert "world" not in masked_text


def test_mask_handles_regex_groups() -> None:
    """Test masking with regex groups."""
    text = "Date: 2023-12-25"
    patterns = r"(\d{4})-(\d{2})-(\d{2})"
    masked_text, masks = mask(text, patterns)

    # Should mask the full match, not individual groups
    assert "2023-12-25" not in masked_text
    assert "Date:" in masked_text
    assert "2023-12-25" in masks


def test_unmask_partial_matches() -> None:
    """Test unmasking when only some masks are present."""
    masked_text = "Hello <<MASK_abc123>> and <<MASK_missing>>"
    mask_map = {"world": "<<MASK_abc123>>"}
    result = unmask(masked_text, mask_map)

    assert result == "Hello world and <<MASK_missing>>"


def test_mask_empty_patterns_list() -> None:
    """Test masking with empty patterns."""
    text = "Some text here"
    patterns = ""
    masked_text, masks = mask(text, patterns)

    assert masked_text == text
    assert masks == {}


def test_mask_no_matches() -> None:
    """Test masking when patterns don't match anything."""
    text = "Clean text with no sensitive data"
    patterns = r"\d{10}"  # 10-digit number pattern
    masked_text, masks = mask(text, patterns)

    assert masked_text == text
    assert masks == {}
