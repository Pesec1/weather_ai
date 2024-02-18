# |%%--%%| <OF5l0xZfkl|iMAszyslsm>

import pygrib
from matplotlib import pyplot as plt
import numpy as np

# |%%--%%| <iMAszyslsm|aEHctwYIh7>

grbs = pygrib.open(
    "D:\\testfolder\\weather_ai\\data\\adaptor.mars.internal-1708206937.3622236-13929-10-d088092a-075d-483d-b234-a16a63f300db.grib"
)

# |%%--%%| <aEHctwYIh7|x3esNotTiG>

for grb in grbs:
    print(grb)

# |%%--%%| <x3esNotTiG|qfj2lbf6Tx>grbs[1:25]
grbs[1:40]
# |%%--%%| <qfj2lbf6Tx|ckPxFFXIKQ>

for key in grb.keys():
    print(key)
# |%%--%%| <ckPxFFXIKQ|pwaAq5kYjs>
u10GrbWind = grbs.select(name="10 metre U wind component")[0]
v10GrbWind = grbs.select(name="10 metre V wind component")[0]
t2GrbTemperature = grbs.select(name="2 metre temperature")[0]
benjaminFeirIndexGrb = grbs.select(name="Benjamin-Feir index")[0]
cloudBasedHeightGrd = grbs.select(name="Cloud base height")[0]
meanEvaporationRateGrb = grbs.select(name="Cloud base height")[0]


# |%%--%%| <pwaAq5kYjs|PXEOl92398>

u10Wind = u10GrbWind.values
v10Wind = v10GrbWind.values
t2Temperature = t2GrbTemperature.values

print(u10Wind.shape, v10Wind.shape, t2Temperature.shape)

# |%%--%%| <PXEOl92398|WSfazSr5Qs>

lats, lons = u10GrbWind.latlons()
print(lats.shape, lons.shape, lats.min(), lats.max(), lons.min(), lons.max())

# |%%--%%| <WSfazSr5Qs|b5rEDlVX2A>

print(lats, lons)

# |%%--%%| <b5rEDlVX2A|sh8jdfC9gz>

from mpl_toolkits.basemap import Basemap

# |%%--%%| <sh8jdfC9gz|vX9zd1utg3>

fig = plt.figure(figsize=(16, 35))
m = Basemap(
    llcrnrlon=37.5,
    llcrnrlat=55.72,
    urcrnrlon=37.7,
    urcrnrlat=55.77,
)

m.drawcoastlines()
m.drawcountries()

skip = 20

cs = m.contourf(lons, lats, t2Temperature)
qv = m.quiver(
    lons[::skip, ::skip],
    lats[::skip, ::skip],
    u10Wind[::skip, ::skip],
    v10Wind[::skip, ::skip],
)

# |%%--%%| <vX9zd1utg3|HFgYxpy5sV>


def find_nearest(x, y, gridx, gridy):
    distance = (gridx - x) ** 2 + (gridy - y) ** 2
    idx = np.where(distance == distance.min())

    return [idx[0][0], idx[1][0]]


# |%%--%%| <HFgYxpy5sV|q6UYMoDFkf>

idx = find_nearest(65.5, 57.1522, lons, lats)

print(lons[idx[0], idx[1]], lats[idx[0], idx[1]])

# |%%--%%| <q6UYMoDFkf|tFHHrYvmh6>

u10 = []
v10 = []
t2 = []
dates = []

from glob import glob

list_of_files = glob("D:/testfolder/weather_ai/data/adaptor.mars.internal*")

for infile in sorted(list_of_files):
    print("Open file: %s" % infile)
    grbs = pygrib.open(infile)

    u10_grb = grbs.select(name="10 metre U wind component")[0]
    v10_grb = grbs.select(name="10 metre V wind component")[0]
    t2_grb = grbs.select(name="2 metre temperature")[0]

    u10.append(u10_grb.values)
    v10.append(v10_grb.values)
    t2.append(t2_grb.values)
    dates.append(u10_grb.validDate)
    grbs.close()

lats, lons = u10_grb.latlons()

# |%%--%%| <tFHHrYvmh6|pNgYi3bWQh>

import pandas as pd

data = {
    "u10": u10[:, idx[0], idx[1]],
    "v10": v10[:, idx[0], idx[1]],
    "t2": t2[:, idx[0], idx[1]],
}

df = pd.DataFrame(data, index=dates)
print(df)

# |%%--%%| <pNgYi3bWQh|OkPdlcoqI6>


t2 = []
dates = []

from glob import glob

list_of_files = glob(
    "D:/testfolder/weather_ai/data/adaptor.mars.internal-1708206937.3622236-13929-10-d088092a-075d-483d-b234-a16a63f300db.grib"
)

for infile in sorted(list_of_files):
    print("Open file: %s" % infile)
    grbs = pygrib.open(infile)

    t2_grb = grbs.select(name="2 metre temperature")
    print(t2_grb)
    for value in t2_grb:
        t2.append(value.values)
        dates.append(value.validDate)

    print(t2)
    print(dates)
    grbs.close()


# |%%--%%| <OkPdlcoqI6|pjRAXvbTSd>

lats, lons = t2_grb[0].latlons()

# |%%--%%| <pjRAXvbTSd|lhdbaBcBFu>
idx = find_nearest(65.54, 57.16, lons, lats)

# |%%--%%| <lhdbaBcBFu|IkYMZT6Vu2>

import pandas as pd


t2 = np.array(t2)

data = {"t2": t2[:, idx[0], idx[1]]}
df = pd.DataFrame(data, index=dates)
print(df)

# |%%--%%| <IkYMZT6Vu2|S0teVPxFfB>

print(lons[idx[0], idx[1]], lats[idx[0], idx[1]])

# |%%--%%| <S0teVPxFfB|9oKAfA1H4n>


df.to_csv("data.csv", sep=";")
