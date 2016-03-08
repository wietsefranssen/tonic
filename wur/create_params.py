# first run: source activate tonic 
from tonic.models.vic.grid_params import soil, snow, veg, veg_class, Cols, Desc, calc_grid, grid_params, write_netcdf, read_netcdf
import numpy as np

workPath = '/home/wietse/Documents/Projects/VIC/VIC_testsetups/image_test/Wietse/input/VIC_params/'

n_veg_classes = 11
root_zones = 3
months_per_year = 12

# Read the soil parameters
soil_dict = soil(workPath + 'LibsAndParams_vic_website/global_soil_param_new', c=Cols(nlayers=root_zones))

# Read the snow parameters
snow_dict = snow(workPath + 'LibsAndParams_vic_website/global_snowbands_new', soil_dict, c=Cols(snow_bands=5))

# Read the veg parameter file
veg_dict = veg(workPath + 'LibsAndParams_vic_website/global_veg_param_new', soil_dict, lai_index=True, veg_classes=n_veg_classes)

# Read the veg library file
veg_lib = veg_class(workPath + 'LibsAndParams_vic_website/world_veg_lib.txt', skiprows=2)

# Determine the grid shape
#target_grid, target_attrs = calc_grid(soil_dict['lats'], soil_dict['lons'])
target_grid, target_attrs = read_netcdf(workPath + 'LibsAndParams_vic_website/mask_EU.nc')

# Grid all the parameters
grid_dict = grid_params(soil_dict, target_grid, version='5.0.dev',
                        veg_dict=veg_dict, veglib_dict=veg_lib, snow_dict=snow_dict)

# Write a netCDF file with all the parameters
write_netcdf(workPath + 'LibsAndParams_vic_website/params.vic5_EU.nc', target_attrs,
             target_grid=target_grid,
             soil_grid=grid_dict['soil_dict'],
             snow_grid=grid_dict['snow_dict'],
             veglib_dict=veg_lib,
             veg_grid=grid_dict['veg_dict'],
             version='5.0.dev')
