"""Алгоритми пошуку першого входження підрядка в тексті."""


def boyer_moore_search(text: str, pattern: str) -> int:
    """Повертає індекс першого збігу, використовуючи правило поганого символу."""
    pattern_length = len(pattern)
    text_length = len(text)

    if pattern_length == 0:
        return 0
    if pattern_length > text_length:
        return -1

    last_occurrence = {char: index for index, char in enumerate(pattern)}
    shift = 0

    while shift <= text_length - pattern_length:
        pattern_index = pattern_length - 1

        while pattern_index >= 0 and pattern[pattern_index] == text[shift + pattern_index]:
            pattern_index -= 1

        if pattern_index < 0:
            return shift

        mismatched_char = text[shift + pattern_index]
        shift += max(1, pattern_index - last_occurrence.get(mismatched_char, -1))

    return -1


def _build_lps(pattern: str) -> list[int]:
    """Створює таблицю найдовших власних префіксів, що є суфіксами."""
    lps = [0] * len(pattern)
    prefix_length = 0
    index = 1

    while index < len(pattern):
        if pattern[index] == pattern[prefix_length]:
            prefix_length += 1
            lps[index] = prefix_length
            index += 1
        elif prefix_length:
            prefix_length = lps[prefix_length - 1]
        else:
            lps[index] = 0
            index += 1

    return lps


def kmp_search(text: str, pattern: str) -> int:
    """Повертає індекс першого збігу алгоритмом Кнута—Морріса—Пратта."""
    if not pattern:
        return 0
    if len(pattern) > len(text):
        return -1

    lps = _build_lps(pattern)
    text_index = 0
    pattern_index = 0

    while text_index < len(text):
        if text[text_index] == pattern[pattern_index]:
            text_index += 1
            pattern_index += 1
            if pattern_index == len(pattern):
                return text_index - pattern_index
        elif pattern_index:
            pattern_index = lps[pattern_index - 1]
        else:
            text_index += 1

    return -1


def rabin_karp_search(text: str, pattern: str) -> int:
    """Повертає індекс першого збігу алгоритмом Рабіна—Карпа."""
    pattern_length = len(pattern)
    text_length = len(text)

    if pattern_length == 0:
        return 0
    if pattern_length > text_length:
        return -1

    base = 256
    modulus = 1_000_000_007
    high_order = pow(base, pattern_length - 1, modulus)
    pattern_hash = 0
    window_hash = 0

    for index in range(pattern_length):
        pattern_hash = (pattern_hash * base + ord(pattern[index])) % modulus
        window_hash = (window_hash * base + ord(text[index])) % modulus

    for start in range(text_length - pattern_length + 1):
        if pattern_hash == window_hash and text[start : start + pattern_length] == pattern:
            return start

        if start < text_length - pattern_length:
            window_hash = (window_hash - ord(text[start]) * high_order) % modulus
            window_hash = (window_hash * base + ord(text[start + pattern_length])) % modulus

    return -1
