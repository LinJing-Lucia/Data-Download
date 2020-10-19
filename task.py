#-*- coding:utf-8 -*-
from netCDF4 import Dataset
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import matplotlib.ticker as mticker
from libtiff import TIFF
import os
import string
def read(data):
    # Run the following cell to see the MERRA2 metadata. This line will print attribute and variable information. From the 'variables(dimensions)' list, choose which variable(s) to read in below:
    print(data)

    # Read in variables:

    # longitude and latitude
    lons = data.variables['lon']
    lats = data.variables['lat']
    lon, lat = np.meshgrid(lons, lats)
    # 2-meter eastward wind m/s
    ws = data.variables['SPEEDLML']
    # Replace _FillValues with NaNs:
    ws_nans = ws[:]

    _FillValueU2M = ws._FillValue

    ws_nans[ws_nans == _FillValueU2M] = np.nan

    # NOTE: the MERRA-2 file contains hourly data for 24 hours (t=24). To get the daily mean wind speed, take the average of the hourly wind speeds:

    ws_avg = np.nanmean(ws_nans, axis=0)
    return ws_avg

def draw(lon,lat,ws_avg):
    # Plot windspeed: set contour levels, then draw the filled contours and a colorbar
    fig = plt.figure(figsize=(8, 4))
    ax = plt.axes(projection=ccrs.Robinson())
    ax.set_global()
    ax.coastlines(resolution="110m", linewidth=1)
    ax.gridlines(linestyle='--', color='black')
    clevs = np.arange(0, 19, 1)
    plt.contourf(lon, lat, ws_avg, clevs, transform=ccrs.PlateCarree(), cmap=plt.cm.jet)
    plt.title('全球风速数据集(2018-2019年)_数据缩略图', size=14)
    cb = plt.colorbar(ax=ax, orientation="vertical", pad=0.02, aspect=16, shrink=0.8)
    cb.set_label('m/s', size=12, rotation=0, labelpad=15)
    cb.ax.tick_params(labelsize=10)

    # Save figure as PNG:
    fig.savefig('G:/MERRA2_2m_ws.png', format='png', dpi=120)

def output(ws_month_avg,name):
    # Set the figure size, projection, and extent
    outfilepath = "G:\\"+ name
    out_tiff = TIFF.open(outfilepath, mode='w')
    out_tiff.write_image(ws_month_avg, compression=None)
    out_tiff.close()

if __name__ == '__main__':
    # Open the NetCDF4 file (add a directory path if necessary) for reading:

    filePath = r"G:\2020年数据汇交——南大数据资源点\全球风速数据集(2018-2019)\全球风速数据集(2018-2019)-数据实体"  # tiff文件路径
    files = os.listdir(filePath)
    for f in files:
        if (os.path.splitext(f)[1] != '.nc4'):
            continue
        strPath = filePath + "\\" + f
        data = Dataset(strPath, mode='r',encoding="gbk")
        ws_month_avg = read(data)
        name=os.path.splitext(f)[0][27:34]+".tif"
        output(ws_month_avg,name)








