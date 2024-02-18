r"""°°°
neccesary imports
°°°"""
# |%%--%%| <x4gjWbV1nZ|aEHctwYIh7>
import pygrib
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
from glob import glob

# |%%--%%| <aEHctwYIh7|VQmXztv618>
r"""°°°
calulating nearest avaliable point by taking needed lon and lat, and fact lon and lat
°°°"""
# |%%--%%| <VQmXztv618|HFgYxpy5sV>


def find_nearest(x, y, gridx, gridy):
    distance = (gridx - x) ** 2 + (gridy - y) ** 2
    idx = np.where(distance == distance.min())

    return [idx[0][0], idx[1][0]]


# |%%--%%| <HFgYxpy5sV|ITUOC4IVfQ>
r"""°°°
read all files avalible in folder and extraction of needed paramets to lists, takes about 20 minutes for 1 file. Could be optimised somehow. take date from regulary temperature to then use it as an index for dataframe. 
°°°"""
# |%%--%%| <ITUOC4IVfQ|OkPdlcoqI6>
PATHTOFILE = "D:/testfolder/weather_ai/data/adaptor.mars.internal-1708206937.3622236-13929-10-d088092a-075d-483d-b234-a16a63f300db.grib"}

t2 = []
u10 = []
v10 = []
mean_evaporation = []
benjamin_feir = []
cloud_base_height = []
mean_sea_level_pressure = []
mean_vartically_integrated_moisture = []
precipitation_type = []
sea_surface_temperature = []
snow_density = []
snowfall = []
surface_net_long_wave = []
surface_pressure = []
total_cloud_cover = []
total_column_cloud_liquid = []
total_precipitation = []
dates = []


list_of_files = glob(
    PATHTOFILE
)

for infile in sorted(list_of_files):
    print("Open file: %s" % infile)
    grbs = pygrib.open(infile)

    t2_grb = grbs.select(name="2 metre temperature")
    u10_grb = grbs.select(name="10 metre U wind component")
    v10_grb = grbs.select(name="10 metre V wind component")
    mean_evaporation_grb = grbs.select(name="Mean evaporation rate")
    benjamin_feir_grb = grbs.select(name="Benjamin-Feir index")
    cloud_base_height_grb = grbs.select(name="Cloud base height")
    mean_sea_level_pressure_grb = grbs.select(name="Mean sea level pressure")
    mean_vartically_integrated_moisture_grb = grbs.select(
        name="Mean vertically integrated moisture divergence"
    )
    precipitation_type_grb = grbs.select(name="Precipitation type")
    sea_surface_temperature_grb = grbs.select(name="Sea surface temperature")
    snow_density_grb = grbs.select(name="Snow density")
    snowfall_grb = grbs.select(name="Snowfall")
    surface_net_long_wave_grb = grbs.select(
        name="Surface net long-wave (thermal) radiation"
    )
    surface_pressure_grb = grbs.select(name="Surface pressure")
    total_cloud_cover_grb = grbs.select(name="Total cloud cover")
    total_column_cloud_liquid_grb = grbs.select(name="Total column cloud liquid water")
    total_precipitation_grb = grbs.select(name="Total precipitation")

    for i in range(1, len(t2_grb)):
        t2.append(t2_grb[i].values)
        u10.append(u10_grb[i].values)
        v10.append(v10_grb[i].values)
        mean_evaporation.append(mean_evaporation_grb[i].values)
        benjamin_feir.append(benjamin_feir_grb[i].values)
        cloud_base_height.append(cloud_base_height_grb[i].values)
        mean_sea_level_pressure.append(mean_sea_level_pressure_grb[i].values)
        mean_vartically_integrated_moisture.append(
            mean_vartically_integrated_moisture_grb[i].values
        )
        precipitation_type.append(precipitation_type_grb[i].values)
        sea_surface_temperature.append(sea_surface_temperature_grb[i].values)
        snow_density.append(snow_density_grb[i].values)
        snowfall.append(snowfall_grb[i].values)
        surface_net_long_wave.append(surface_net_long_wave_grb[i].values)
        surface_pressure.append(surface_pressure_grb[i].values)
        total_cloud_cover.append(total_cloud_cover_grb[i].values)
        total_column_cloud_liquid.append(total_column_cloud_liquid_grb[i].values)
        total_precipitation.append(total_precipitation_grb[i].values)

        dates.append(t2_grb[i].validDate)

    grbs.close()


# |%%--%%| <OkPdlcoqI6|EsXIgZ84EJ>
r"""°°°
look at avalible coordinates, then we will use them to find nearest point avalible
°°°"""
# |%%--%%| <EsXIgZ84EJ|pjRAXvbTSd>

lats, lons = t2_grb[0].latlons()

# |%%--%%| <pjRAXvbTSd|lhdbaBcBFu>
idx = find_nearest(65.54, 57.16, lons, lats)

# |%%--%%| <lhdbaBcBFu|eyLj1UJz6i>
r"""°°°
Create dataframe using lists that we filled earlier, using date of parametr temperature as an index.
°°°"""
# |%%--%%| <eyLj1UJz6i|IkYMZT6Vu2>


t2 = np.array(t2)
v10 = np.array(v10)
u10 = np.array(u10)
mean_evaporation = np.array(mean_evaporation)
benjamin_feir = np.array(benjamin_feir)
cloud_base_height = np.array(cloud_base_height)
mean_sea_level_pressure = np.array(mean_sea_level_pressure)
mean_vartically_integrated_moisture = np.array(mean_vartically_integrated_moisture)
precipitation_type = np.array(precipitation_type)
sea_surface_temperature = np.array(sea_surface_temperature)
snow_density = np.array(snow_density)
snowfall = np.array(snowfall)
surface_net_long_wave = np.array(surface_net_long_wave)
surface_pressure = np.array(surface_pressure)
total_cloud_cover = np.array(total_cloud_cover)
total_column_cloud_liquid = np.array(total_column_cloud_liquid)
total_precipitation = np.array(total_precipitation)


data = {
    "t2": t2[:, idx[0], idx[1]],
    "v10": v10[:, idx[0], idx[1]],
    "u10": u10[:, idx[0], idx[1]],
    "mean_evaporation": mean_evaporation[:, idx[0], idx[1]],
    # "benjamin_feir": benjamin_feir[:, idx[0], idx[1]],
    "cloud_base_height": cloud_base_height[:, idx[0], idx[1]],
    "mean_sea_level_pressure": mean_sea_level_pressure[:, idx[0], idx[1]],
    "mean_vertically_integrated_moisture": mean_vartically_integrated_moisture[
        :, idx[0], idx[1]
    ],
    "precipitation_type_code": precipitation_type[:, idx[0], idx[1]],
    "sea_surface_temperature": sea_surface_temperature[:, idx[0], idx[1]],
    "snow_density": snow_density[:, idx[0], idx[1]],
    "snowfall": snowfall[:, idx[0], idx[1]],
    "surface_net_long_wave": surface_net_long_wave[:, idx[0], idx[1]],
    "surface_pressure": surface_pressure[:, idx[0], idx[1]],
    "total_cloud_cover": total_cloud_cover[:, idx[0], idx[1]],
    "total_column_cloud_liquid": total_column_cloud_liquid[:, idx[0], idx[1]],
    "total_precipitation": total_precipitation[:, idx[0], idx[1]],
}
df = pd.DataFrame(data, index=dates)
print(df)

# |%%--%%| <IkYMZT6Vu2|S0teVPxFfB>

print(lons[idx[0], idx[1]], lats[idx[0], idx[1]])

# |%%--%%| <S0teVPxFfB|vOqq9Hy4Ri>
r"""°°°
save dataframe to csv for later analyzing and filling
°°°"""
# |%%--%%| <vOqq9Hy4Ri|9oKAfA1H4n>
PATHTOSAVE = 'DATA2023_2024.csv'

df.to_csv('PATHTOSAVE', sep=";")
