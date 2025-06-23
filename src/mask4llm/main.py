import re
import uuid


def mask(text: str, patterns: str) -> tuple[str, dict[str, str]]:
    masks_map: dict[str, str] = {}
    if text and patterns:
        for match in re.finditer(patterns, text):
            original = match.group(0)
            if original not in masks_map:
                placeholder = f"<<MASK_{uuid.uuid4().hex[:6]}>>"
                masks_map[original] = placeholder
                text = text.replace(original, placeholder)
    return text, masks_map


def unmask(masked_text: str, mask_map: dict[str, str]) -> str:
    for original, placeholder in mask_map.items():
        masked_text = masked_text.replace(placeholder, original)
    return masked_text


if __name__ == "__main__":
    text = "Hello, John!"
    patterns = r"John"
    masked_text, masks_map = mask(text, patterns)
    print(f"Original Text: {text}")
    print(f"Masked Text: {masked_text}")
    print(f"Mask Maps: {masks_map}")
