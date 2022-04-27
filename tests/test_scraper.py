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

    def test_scrape_player_codes(self):
        """"""
        scraper = FbRefScraper(level=logging.WARNING)

        expected = {'Max Aarons': '774cf58b',
                    'Nathan AkÃ©': 'eaeca114',
                    'Eric Bailly': 'a1232f4e',
                    'Aaron Cresswell': '4f974391'}

        actual = scraper.scrape_player_codes()

        for squad in expected.keys():
            self.assertEqual(expected[squad], actual[squad])

    def test_scrape_squad_summaries(self):
        """"""

        expected = {
            'stats': ['players_used',
                      'avg_age',
                      'possession',
                      'games',
                      'games_starts',
                      'minutes',
                      'minutes_90s',
                      'goals',
                      'assists',
                      'goals_pens',
                      'pens_made',
                      'pens_att',
                      'cards_yellow',
                      'cards_red',
                      'goals_per90',
                      'assists_per90',
                      'goals_assists_per90',
                      'goals_pens_per90',
                      'goals_assists_pens_per90',
                      'xg',
                      'npxg',
                      'xa',
                      'npxg_xa',
                      'xg_per90',
                      'xa_per90',
                      'xg_xa_per90',
                      'npxg_per90',
                      'npxg_xa_per90'],

            'possession': ['players_used',
                           'possession',
                           'minutes_90s',
                           'touches',
                           'touches_def_pen_area',
                           'touches_def_3rd',
                           'touches_mid_3rd',
                           'touches_att_3rd',
                           'touches_att_pen_area',
                           'touches_live_ball',
                           'dribbles_completed',
                           'dribbles',
                           'dribbles_completed_pct',
                           'players_dribbled_past',
                           'nutmegs',
                           'carries',
                           'carry_distance',
                           'carry_progressive_distance',
                           'progressive_carries',
                           'carries_into_final_third',
                           'carries_into_penalty_area',
                           'miscontrols',
                           'dispossessed',
                           'pass_targets',
                           'passes_received',
                           'passes_received_pct',
                           'progressive_passes_received'],

            'shooting': ['players_used',
                         'minutes_90s',
                         'goals',
                         'shots_total',
                         'shots_on_target',
                         'shots_on_target_pct',
                         'shots_total_per90',
                         'shots_on_target_per90',
                         'goals_per_shot',
                         'goals_per_shot_on_target',
                         'average_shot_distance',
                         'shots_free_kicks',
                         'pens_made',
                         'pens_att',
                         'xg',
                         'npxg',
                         'npxg_per_shot',
                         'xg_net',
                         'npxg_net']}

        scraper = FbRefScraper(level=logging.WARNING)

        # Check each
        for stat in expected.keys():
            for vs in (True, False):
                self.assertEqual(expected[stat], list(scraper.scrape_squad_summaries(stat=stat, vs=vs).columns))

if __name__ == '__main__':
    logging.basicConfig(level=logging.WARNING)
    unittest.main()
