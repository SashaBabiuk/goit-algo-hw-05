import unittest

from search_algorithms import boyer_moore_search, kmp_search, rabin_karp_search


class SearchAlgorithmsTest(unittest.TestCase):
    algorithms = (boyer_moore_search, kmp_search, rabin_karp_search)

    def test_common_cases(self) -> None:
        cases = (
            ("hello world", "world"),
            ("aaaaab", "aab"),
            ("алгоритм пошуку", "пошук"),
            ("short", "long pattern"),
            ("text", ""),
            ("", ""),
            ("abc", "z"),
        )
        for text, pattern in cases:
            for algorithm in self.algorithms:
                with self.subTest(algorithm=algorithm.__name__, pattern=pattern):
                    self.assertEqual(algorithm(text, pattern), text.find(pattern))


if __name__ == "__main__":
    unittest.main()
