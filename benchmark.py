"""Порівняння швидкості трьох алгоритмів пошуку підрядка."""

from pathlib import Path
from timeit import repeat
from typing import Callable

from search_algorithms import boyer_moore_search, kmp_search, rabin_karp_search

SearchFunction = Callable[[str, str], int]
BASE_DIR = Path(__file__).resolve().parent
REPEAT_COUNT = 5
SEARCH_COUNT = 100

ALGORITHMS: dict[str, SearchFunction] = {
    "Боєра—Мура": boyer_moore_search,
    "Кнута—Морріса—Пратта": kmp_search,
    "Рабіна—Карпа": rabin_karp_search,
}

ARTICLES = {
    "Стаття 1": {
        "path": BASE_DIR / "стаття 1.txt",
        "existing": "алгоритми та структури даних",
        "missing": "квантовий гіперпростір",
    },
    "Стаття 2": {
        "path": BASE_DIR / "стаття 2.txt",
        "existing": "рекомендаційної системи",
        "missing": "квантовий гіперпростір",
    },
}


def read_article(path: Path) -> str:
    """Читає надані статті, збережені у Windows-1251."""
    return path.read_text(encoding="cp1251")


def measure(function: SearchFunction, text: str, pattern: str) -> float:
    """Повертає найменший середній час одного пошуку в секундах."""
    measurements = repeat(
        lambda: function(text, pattern),
        repeat=REPEAT_COUNT,
        number=SEARCH_COUNT,
    )
    return min(measurements) / SEARCH_COUNT


def run_benchmark() -> dict[str, dict[str, dict[str, float]]]:
    results: dict[str, dict[str, dict[str, float]]] = {}

    for article_name, article in ARTICLES.items():
        text = read_article(article["path"])
        results[article_name] = {}

        for pattern_type in ("existing", "missing"):
            pattern = article[pattern_type]
            expected = text.find(pattern)
            results[article_name][pattern_type] = {}

            for algorithm_name, function in ALGORITHMS.items():
                actual = function(text, pattern)
                if actual != expected:
                    raise RuntimeError(
                        f"{algorithm_name}: отримано {actual}, очікувалося {expected}"
                    )
                results[article_name][pattern_type][algorithm_name] = measure(
                    function, text, pattern
                )

    return results


def print_results(results: dict[str, dict[str, dict[str, float]]]) -> None:
    labels = {"existing": "існуючий", "missing": "вигаданий"}
    totals = {name: 0.0 for name in ALGORITHMS}

    print(f"Кількість запусків в одному замірі: {SEARCH_COUNT}\n")
    for article_name, patterns in results.items():
        print(article_name)
        article_totals = {name: 0.0 for name in ALGORITHMS}
        for pattern_type, timings in patterns.items():
            print(f"  {labels[pattern_type].capitalize()} підрядок:")
            for algorithm_name, seconds in timings.items():
                microseconds = seconds * 1_000_000
                print(f"    {algorithm_name:<28} {microseconds:10.2f} мкс")
                article_totals[algorithm_name] += seconds
                totals[algorithm_name] += seconds
            fastest = min(timings, key=timings.get)
            print(f"    Найшвидший: {fastest}")
        fastest_for_article = min(article_totals, key=article_totals.get)
        print(f"  Загалом для тексту: {fastest_for_article}\n")

    print(f"Найшвидший в цілому: {min(totals, key=totals.get)}")


if __name__ == "__main__":
    print_results(run_benchmark())
