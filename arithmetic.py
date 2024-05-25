from collections import defaultdict
from decimal import Decimal, getcontext

getcontext().prec = 50


def calculate_frequencies(text: str) -> dict[str, int]:
    frequencies: defaultdict[str, int] = defaultdict(int)

    for char in text:
        frequencies[char] += 1

    return frequencies


def build_intervals(frequencies: dict[str, int]) -> dict[str, tuple[Decimal, Decimal]]:
    total = sum(frequencies.values())
    intervals: dict[str, tuple[Decimal, Decimal]] = {}
    low = Decimal(0)

    for char, freq in frequencies.items():
        high = low + Decimal(freq) / Decimal(total)
        intervals[char] = (low, high)
        low = high

    return intervals


def arithmetic_encode(
    text: str, intervals: dict[str, tuple[Decimal, Decimal]]
) -> Decimal:
    low = Decimal(0)
    high = Decimal(1)

    for char in text:
        char_low, char_high = intervals[char]
        range_ = high - low
        high = low + range_ * char_high
        low = low + range_ * char_low

    return (low + high) / 2


def arithmetic_decode(
    encoded: Decimal, length: int, intervals: dict[str, tuple[Decimal, Decimal]]
) -> str:
    low = Decimal(0)
    high = Decimal(1)
    decoded_text = ""

    for _ in range(length):
        range_ = high - low
        value = (encoded - low) / range_

        for char, (char_low, char_high) in intervals.items():
            if char_low <= value < char_high:
                decoded_text += char
                high = low + range_ * char_high
                low = low + range_ * char_low
                break

    return decoded_text


if __name__ == "__main__":
    original = "HELLO"
    print(f"Original: {original}")

    frequencies = calculate_frequencies(original)
    intervals = build_intervals(frequencies)

    encoded = arithmetic_encode(original, intervals)
    print(f"Encoded: {encoded}")

    decoded = arithmetic_decode(encoded, len(original), intervals)
    print(f"Decoded: {decoded}")

    if original != decoded:
        raise ValueError("Decoded data does not match original data")
