import fasts2
import ee

ee.Initialize()

params = {
    "lat": 36.80065496560349,
    "lon": -119.68553947009042,
    "start_date": "2020-01-01",
    "end_date": "2020-12-31",
    "level": "L2A",
    "download_dir": "data",
    "max_cloud_cover": 0.01,
    "resolution": 10,
    "bands": ["B2", "B3", "B4", "B8"],
    "patch_size": 2560,
    "nworkers": 10
}

params = fasts2.S2GoogleTask(**params)
params.download_s2()
