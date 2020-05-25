import unittest
import geoscript
import geopandas as gpd
import sys

test_frame1 = gpd.read_file('path_to_region')
test_frame2 = gpd.read_file('path_to_tiles')
test_frame3 = gpd.read_file('path_to_selection')
test_frame4 = gpd.read_file('path_to_output')


class TestGeoScript(unittest.TestCase):

    def test_get_comline_args(self):
        self.assertRaises(SystemExit, geoscript.get_comline_args, [])

    def test_read_files(self):
        self.assertRaises(SystemExit, geoscript.get_read_files, test_frame1, test_frame2)

    def test_spacial_indexing(self):
        self.assertEqual(geoscript.spacial_indexing(test_frame1, test_frame2), test_frame3)

    def test_check_coordinate_systems(self):
        self.assertRaises(SystemExit, geoscript.check_coordinate_systems, test_frame1, test_frame2)

    def test_set_analysis(self):
        self.assertEqual(geoscript.set_analysis(test_frame3, test_frame1), test_frame4)
