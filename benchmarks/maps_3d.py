import numpy as np
from gammapy.data import DataStore
from gammapy.maps import MapAxis, WcsGeom
from gammapy.cube import MapDataset, MapDatasetMaker
import astropy.units as u


N_OBS = 100
OBS_ID = 110380


def run_benchmark():
    data_store = DataStore.from_dir("$GAMMAPY_DATA/cta-1dc/index/gps/")
    obs_ids = OBS_ID * np.ones(N_OBS)
    observations = data_store.get_observations(obs_ids)

    energy_axis = MapAxis.from_bounds(
        0.1, 10, nbin=10, unit="TeV", name="energy", interp="log"
    )
    geom = WcsGeom.create(
        skydir=(0, 0),
        binsz=0.05,
        width=(10, 8),
        coordsys="GAL",
        proj="CAR",
        axes=[energy_axis],
    )

    stacked = MapDataset.create(geom)
    for obs in observations:
        maker = MapDatasetMaker(geom, offset_max=4.0 * u.deg)
        dataset = maker.run(obs)
        stacked.stack(dataset)


if __name__ == "__main__":
    run_benchmark()