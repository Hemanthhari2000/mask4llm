import re
from typing import NamedTuple

import pytest

from mask4llm.main import mask


class MaskParamTestType(NamedTuple):
    text: str
    patterns: str
    expected_keys: list[str]


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
