from typing import List
import os
import gpxpy
from typing import Optional


def get_file_list(root_path_list: List, file_ending: str = 'gpx') -> List[str]:
    flists_all = [os.listdir(root) for root in root_path_list]
    flist = []
    for i, flist_all in enumerate(flists_all):
        root = root_path_list[i]
        for ff in flist_all:
            if ff.endswith(file_ending):
                flist.append(os.path.join(root, ff))
    return flist

def get_gpx_list(root_path_list: List, file_ending: str = 'gpx', year: Optional[int] = None) -> List[gpxpy.gpx.GPX]:
    gpx_list = []
    file_list = get_file_list(root_path_list, file_ending)
    for ffile in file_list:
        gfile = open(ffile, 'r')
        try:
            gpx = gpxpy.parse(gfile)
        except:
            continue
        # Funny movescount activities have not start time and cause crash:
        start_time = gpx.get_time_bounds().start_time

        if (start_time is not None and start_time.isocalendar()[0] == year) or year is None:
            gpx_list.append(gpx)
    return gpx_list
