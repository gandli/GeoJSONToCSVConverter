import geopandas as gpd
import pandas as pd
import json
from shapely.geometry import MultiPolygon, Point

def convert_geojson_to_csv(geojson_file, csv_file):
    # 读取 GeoJSON 文件
    gdf = gpd.read_file(geojson_file)

    # 创建一个空的行列表
    rows = []

    # 创建一个ID计数器
    id_counter = 1

    # 顶层：福州市
    city_name = "福州市"
    city_level = 0
    city_hierarchy = "0-0"
    
    # 合并所有区县的地理轮廓以创建福州市的地理轮廓
    city_geometry = gdf.geometry.union_all()
    city_center = city_geometry.centroid

    # 添加福州市信息
    rows.append([city_name, city_level, city_hierarchy, 
                 json.dumps({"type": "Point", "coordinates": list(city_center.coords[0])}), 
                 json.dumps(city_geometry.__geo_interface__)])

    # 遍历 GeoJSON 文件中的各区县
    for index, feature in gdf.iterrows():
        district_name = feature['name']
        district_hierarchy = f"{city_hierarchy}-{index}"
        district_geometry = feature.geometry
        district_center = district_geometry.centroid

        # 添加区县信息
        rows.append([district_name, city_level + 1, district_hierarchy, 
                     json.dumps({"type": "Point", "coordinates": list(district_center.coords[0])}), 
                     json.dumps(district_geometry.__geo_interface__)])

    # 将行列表转换为 DataFrame
    df = pd.DataFrame(rows)

    # 保存为 CSV 文件，不包含标题
    df.to_csv(csv_file, index=False, header=False)
    print(f"转换成功: {csv_file}")

# 设置文件路径
geojson_file = '350100.geojson'
csv_file = '350100.csv'

# 执行转换
convert_geojson_to_csv(geojson_file, csv_file)
