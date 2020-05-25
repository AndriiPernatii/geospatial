import getopt
import sys
import geopandas as gpd
from fiona import errors as fiona_err

def get_comline_args(argv):
    try:
        options,arguments = getopt.getopt(argv, "i:o:",["input_file=", "output_file="])
    except getopt.GetoptError as err:
        print(str(err))
        sys.exit(2)
    region_fp, output_fp = '', ''
    for option, arg in options:
        if option in ("-i", "--input_file"):
            region_fp = arg
        elif option in ("-o", "--output_file"):
            output_fp = arg
    if not region_fp or not output_fp:
        print('Requires two arguments!')
        sys.exit(2)
    return region_fp, output_fp

def read_files(region_fp, tiles_fp):
    try:
        region = gpd.read_file(region_fp)
        tiles = gpd.read_file(tiles_fp)
        return region, tiles
    except fiona_err.DriverError:
        print('No such file(s) or directory(ies)')
        sys.exit(2)

def spatial_indexing(tiles, region):
    tiles_sindex = tiles.sindex
    bounds = list(region.bounds.values[0])
    tile_idx = list(tiles_sindex.intersection(bounds))
    tile_candidates = tiles.loc[tile_idx]
    final_selection = tile_candidates.loc[tile_candidates.intersects(region['geometry'].values[0])]
    return final_selection

def check_coordinate_systems(region, final_selection):
    if not region.crs == final_selection.crs:
        print('The coordinate systems do not coincide!')
        sys.exit(2)
    else:
        return

def set_analysis(final_selection, region):
    output_frame = gpd.GeoDataFrame()

    for index, row in final_selection.iterrows():
        selection = gpd.GeoDataFrame([final_selection.loc[index]], crs = final_selection.crs)
        for index_, row_ in final_selection.iterrows():
            if index != index_:
                diff_selection = gpd.GeoDataFrame([final_selection.loc[index_]], crs = final_selection.crs)
                selection = gpd.overlay(selection, diff_selection, how='difference')
        if (selection.intersects(region['geometry'].values[0])).bool():
            output_frame = output_frame.append(final_selection.loc[index])
    return output_frame


def main(argv):
    region_fp, output_fp = get_comline_args(argv)

    tiles_fp = 'sentinel2_tiles.geojson'

    region, tiles = read_files(region_fp, tiles_fp)

    final_selection = spatial_indexing(tiles, region)

    check_coordinate_systems(region, final_selection)

    output_frame = set_analysis(final_selection, region)

    output_frame.to_file(output_fp, driver='GeoJSON')

    for index, row in output_frame.iterrows():
        print(row['Name'])

if __name__ == "__main__":
   main(sys.argv[1:])
