import unittest
import logging

from modules.scraper import FbRefScraper


class TestFbRefScraper(unittest.TestCase):
    """"""

    def test_scrape_squad_codes(self):
        """"""
        scraper = FbRefScraper(level=logging.WARNING)

        expected = {'Arsenal': '18bb7c10',
                    'Aston Villa': '8602292d',
                    'Brentford': 'cd051869',
                    'Brighton': 'd07537b9',
                    'Burnley': '943e8050',
                    'Chelsea': 'cff3d9bb',
                    'Crystal Palace': '47c64c55',
                    'Everton': 'd3fd31cc',
                    'Leeds United': '5bfb9659',
                    'Leicester City': 'a2d435b3',
                    'Liverpool': '822bd0ba',
                    'Manchester City': 'b8fd03ef',
                    'Manchester Utd': '19538871',
                    'Newcastle Utd': 'b2b47a98',
                    'Norwich City': '1c781004',
                    'Southampton': '33c895d4',
                    'Tottenham': '361ca564',
                    'Watford': '2abfe087',
                    'West Ham': '7c21e445',
                    'Wolves': '8cec06e1'}

        actual = scraper.scrape_squad_codes()

        for squad in expected.keys():
            self.assertEqual(expected[squad], actual[squad])


if __name__ == '__main__':
    logging.basicConfig(level=logging.WARNING)
    unittest.main()
