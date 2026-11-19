import tempfile
import unittest
from pathlib import Path

from citykit.publish.sitemap import build_sitemap, update_lastmod


class SitemapTests(unittest.TestCase):
    def test_build_sitemap_contains_loc(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            page = root / "index.html"
            page.write_text("<html></html>", encoding="utf-8")
            xml = build_sitemap([str(page)], root, "https://example.org")
            self.assertIn("<loc>https://example.org/</loc>", xml)

    def test_update_lastmod_changes_existing_url(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "sitemap.xml"
            path.write_text(
                '<urlset><url><loc>https://example.org/shop-53.html</loc></url></urlset>',
                encoding="utf-8",
            )
            changed = update_lastmod(path, "shop-53", "2026-11-19")
            self.assertTrue(changed)
            self.assertIn("<lastmod>2026-11-19</lastmod>", path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
