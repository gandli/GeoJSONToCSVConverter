# GeoJSONToCSVConverter

![alt text](image.png)

## 项目简介

这是一个将 GeoJSON 文件格式转换成符合 Quick BI CSV 文件格式的 Python 脚本。

## Quick BI CSV文件格式说明

```
CSV 文件格式如下：
区块名称：江苏省。
所属层级：第一层，以0开始。
层级索引：0-0表示是第一层第一个区块，以此类推，0-0-0表示是江苏省中的第一个区块南京市。
区块中心点：{"type":"Point","coordinates":[119.486506,32.983991]}
（是以 WKT 标准定义的单个点格式，coordinates 是当前区块的中心点经纬度。）
区块围栏：{"type":"MultiPolygon","coordinates":[[[[118.408205,34.435512]...[118.40495,34.42774],[118.395184,34.427053],[118.379974,34.415545],[118.353203,34.417435],[118.352248,34.422845],[118.320931,34.421342]]]]}（是以 WKT 标准定义的面（Polygon）或者多面（MultiPolygon）格式 coordinates 是当前区块的围栏经纬度。）
```

## 使用说明

1. 安装依赖包：

    ```sh
    pip install -r requirements.txt
    ```

2. 运行转换脚本：

    ```sh
    python json2csv.py
    ```

3. 生成的 350100.csv 文件将保存在项目根目录下。

## 目录说明

- **json2csv.py**：主脚本文件，包含转换逻辑

## 数据来源

- [POI数据](https://www.poi86.com/)
