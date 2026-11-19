import unittest

from citykit.models import Shop
from citykit.render.faq import build_faq


class FaqTests(unittest.TestCase):
    def test_only_verified_fields_are_used(self):
        shop = Shop(name="Магазин", address="ул. Центральная, 5")
        answers = " ".join(answer for _, answer in build_faq(shop))
        self.assertIn("Центральная", answers)
        self.assertNotIn("доставка", answers.lower())

    def test_missing_data_asks_to_confirm(self):
        pairs = build_faq(Shop(name="Магазин"))
        self.assertEqual(len(pairs), 1)
        self.assertIn("Уточните", pairs[0][1])


if __name__ == "__main__":
    unittest.main()
