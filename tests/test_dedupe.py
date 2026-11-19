import unittest

from citykit.match.dedupe import dedupe, is_noise
from citykit.models import Shop


class DedupeTests(unittest.TestCase):
    def test_noise_rows_are_removed(self):
        shop = Shop(name="Банкомат", address="ул. Центральная, 1")
        self.assertTrue(is_noise(shop))

    def test_same_shop_with_address_variant(self):
        first = Shop(name="Тёплый дом", address="Артиллерийская ул., 5")
        second = Shop(name="Теплый дом", address="Артиллерийская улица 5")
        kept, removed = dedupe([first, second], threshold=0.8)
        self.assertEqual(len(kept), 1)
        self.assertEqual(removed, 1)

    def test_different_shops_are_kept(self):
        first = Shop(name="Аптека", address="ул. Садовая, 1")
        second = Shop(name="Цветы", address="ул. Лесная, 9")
        kept, removed = dedupe([first, second])
        self.assertEqual((len(kept), removed), (2, 0))


if __name__ == "__main__":
    unittest.main()
