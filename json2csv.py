import geopandas as gpd
import pandas as pd
import json
import os
from shapely.geometry import MultiPolygon, Point


def convert_geojson_to_csv(city_geojson_file, district_geojson_dir, csv_file):
    # 读取福州市的 GeoJSON 文件
    city_gdf = gpd.read_file(city_geojson_file)

    # 创建一个空的行列表
    rows = []

    # 顶层：福州市
    city_name = "福州市"
    city_level = 0
    city_hierarchy = "0-0"

    # 合并所有区县的地理轮廓以创建福州市的地理轮廓
    city_geometry = city_gdf.geometry.union_all()
    city_center = city_geometry.centroid

    # 添加福州市信息
    rows.append(
        [
            city_name,
            city_level,
            city_hierarchy,
            json.dumps({"type": "Point", "coordinates": list(city_center.coords[0])}),
            json.dumps(city_geometry.__geo_interface__),
        ]
    )

    # 遍历福州市的 GeoJSON 文件中的各区县
    for index, feature in city_gdf.iterrows():
        district_name = feature.get("name")
        district_id = feature.get("id")
        district_hierarchy = f"{city_hierarchy}-{index}"
        district_geometry = feature.geometry
        district_center = district_geometry.centroid

        # 添加区县信息
        rows.append(
            [
                district_name,
                city_level + 1,
                district_hierarchy,
                json.dumps(
                    {"type": "Point", "coordinates": list(district_center.coords[0])}
                ),
                json.dumps(district_geometry.__geo_interface__),
            ]
        )

        # 读取区县的 GeoJSON 文件
        district_geojson_file = os.path.join(
            district_geojson_dir, f"{district_id}.geojson"
        )
        if os.path.exists(district_geojson_file):
            district_gdf = gpd.read_file(district_geojson_file)

            # 遍历区县的 GeoJSON 文件中的各乡镇
            for d_index, d_feature in district_gdf.iterrows():
                township_name = d_feature.get("name")
                township_hierarchy = f"{district_hierarchy}-{d_index}"
                township_geometry = d_feature.geometry
                township_center = township_geometry.centroid

                # 添加乡镇信息
                rows.append(
                    [
                        township_name,
                        city_level + 2,
                        township_hierarchy,
                        json.dumps(
                            {
                                "type": "Point",
                                "coordinates": list(township_center.coords[0]),
                            }
                        ),
                        json.dumps(township_geometry.__geo_interface__),
                    ]
                )

    # 将行列表转换为 DataFrame
    df = pd.DataFrame(rows)

    # 保存为 CSV 文件，不包含标题
    df.to_csv(csv_file, index=False, header=False)
    print(f"转换成功: {csv_file}")


# 设置文件路径
city_geojson_file = "data/350000/350100.geojson"
district_geojson_dir = "data/350000/350100"  # 存放各区县的 GeoJSON 文件的目录
csv_file = "output/350100.csv"

# 执行转换
convert_geojson_to_csv(city_geojson_file, district_geojson_dir, csv_file)
