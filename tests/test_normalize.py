import unittest

from citykit.match.normalize import normalize_address, normalize_text
from citykit.match.tokens import jaccard, tokenize


class NormalizeTests(unittest.TestCase):
    def test_yo_becomes_e(self):
        self.assertEqual(normalize_text("Магазин «Тёплый дом»"), "магазин теплый дом")

    def test_address_variants(self):
        left = normalize_address("Артиллерийская ул., 5")
        right = normalize_address("Артиллерийская улица 5")
        self.assertEqual(left, right)

    def test_jaccard_for_identical_tokens(self):
        self.assertEqual(jaccard(tokenize("Цветы"), tokenize("Цветы")), 1.0)


if __name__ == "__main__":
    unittest.main()
