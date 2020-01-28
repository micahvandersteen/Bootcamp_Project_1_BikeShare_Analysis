import geopandas as gpd
import numpy as np
import pandas as pd


# # Read in the shapefiles of city census tracts ( with their geometry)
m_census_gdf = gpd.read_file("Census_subsets/Mpls_CensusTracts.shp")
# # convert the GEOID field to an integer for merging later
m_census_gdf = m_census_gdf.astype({'GEOID': 'int64'})
b_census_gdf = gpd.read_file("Census_subsets/Bos_CensusTracts.shp")
b_census_gdf = b_census_gdf.astype({'GEOID': 'int64'})
p_census_gdf = gpd.read_file("Census_subsets/Por_CensusTracts.shp")
p_census_gdf = p_census_gdf.astype({'GEOID': 'int64'})

# # Read in the ACS census data from the census api
m_census_df = pd.read_csv('census_output/m_census_25.csv', index_col=0)
b_census_df = pd.read_csv('census_output/b_census_25.csv', index_col=0)
p_census_df = pd.read_csv('census_output/p_census_25.csv', index_col=0)

# # Merge the census api data to the census geometry data adn export to csv
m_merged = m_census_gdf.merge(m_census_df, on='GEOID')
# m_merged.to_csv('census_output/m_merged.csv')
b_merged = b_census_gdf.merge(b_census_df, on='GEOID')
# b_merged.to_csv('census_output/b_merged.csv')
p_merged = p_census_gdf.merge(p_census_df, on='GEOID')
# p_merged.to_csv('census_output/p_merged.csv')

# pull in the merged census info that includes the top 25 data
# m_merged_25 = pd.read_csv('census_output/m_merged_25.csv', index_col=0)
# b_merged_25 = pd.read_csv('census_output/b_merged_25.csv', index_col=0)
# p_merged_25 = pd.read_csv('census_output/p_merged_25.csv', index_col=0)


# # Read in the bike trips info
m_bike_df = pd.read_csv('census_output/m_bike.csv', index_col=0)
m_bike_df = m_bike_df.rename(columns={"start station longitude":"s_longitude", "start station latitude":"s_latitude",
    "end station longitude":"e_longitude", "end station latitude":"e_latitude"})
b_bike_df = pd.read_csv('census_output/b_bike.csv', index_col=0)
b_bike_df = b_bike_df.rename(columns={"start station longitude":"s_longitude", "start station latitude":"s_latitude",
    "end station longitude":"e_longitude", "end station latitude":"e_latitude"})
p_bike_df = pd.read_csv('census_output/p_bike.csv', index_col=0)
p_bike_df = p_bike_df.rename(columns={"StartLongitude":"s_longitude", "StartLatitude":"s_latitude",
    "EndLongitude":"e_longitude", "EndLatitude":"e_latitude"})


# Create geo dfs from the city bike data
m_bike_gdf = gpd.GeoDataFrame(
    m_bike_df, geometry=gpd.points_from_xy(m_bike_df.s_longitude, m_bike_df.s_latitude))
b_bike_gdf = gpd.GeoDataFrame(
    b_bike_df, geometry=gpd.points_from_xy(b_bike_df.s_longitude, b_bike_df.s_latitude))
p_bike_gdf = gpd.GeoDataFrame(
    p_bike_df, geometry=gpd.points_from_xy(p_bike_df.s_longitude, p_bike_df.s_latitude))
print("------------------------------------")
print(" Geo dfs have been created from the bike data")
#
# Warning---- takes a long time to run!!!!!
# Spatial join
m_sjoin = gpd.sjoin(m_merged, m_bike_gdf, how="inner", op='intersects')
m_sjoin.to_csv('census_output/m_sjoin.csv')
print("------------------------------------")
print("Minneapolis data has been joined")
b_sjoin = gpd.sjoin(b_merged, b_bike_gdf, how="inner", op='intersects')
b_sjoin.to_csv('census_output/b_sjoin.csv')
print("------------------------------------")
print("Boston data has been joined")
p_sjoin = gpd.sjoin(p_merged, p_bike_gdf, how="inner", op='intersects')
p_sjoin.to_csv('census_output/p_sjoin.csv')
print("------------------------------------")
print("Portland data has been joined")

print("------------------------------------")
print("Success!")
