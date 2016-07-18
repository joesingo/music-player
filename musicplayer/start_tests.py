import unittest

from test.queue_tests import QueueTests
from test.music_player_tests import MusicPlayerTests


if __name__ == "__main__":

    loader = unittest.TestLoader()

    suites_list = []
    for test_class in [MusicPlayerTests, QueueTests]:
        suite = loader.loadTestsFromTestCase(test_class)
        suites_list.append(suite)

    runner = unittest.TextTestRunner()
    runner.run(unittest.TestSuite(suites_list))
