#-- 11.slaids -----------------------------------------------------------------------------------------
# Importē nepieciešamās bibliotēkas (Import the required libraries)
from sqlalchemy import create_engine
import pandas as pd

# Izveidojam engine objektu savienojumam ar PostgreSQL/PostGIS datubāzi 
# (Create an engine for connecting to the PostgreSQL/PostGIS database)
#engine = create_engine('postgresql+psycopg2://username:password@localhost:5432/my_database')
engine = create_engine('postgresql+psycopg2://postgres:postgres@localhost:5432/postgres')

#-- 13.slaids -----------------------------------------------------------------------------------------
# Izpildām vienkāršu vaicājumu, piemēram, datubāzes versijas noskaidrošanai
# (Execute a simple query, e.g., to check the database version)
test_query = "SELECT version();"
version_df = pd.read_sql(test_query, engine)

# Izdrukāsim rezultātu (Print out the result)
with pd.option_context('display.max_colwidth', None):
  print(version_df)

#-- 15.slaids -----------------------------------------------------------------------------------------

# Definējam SQL vaicājumu, lai iegūtu katra poligona platību un perimetru
# (Define an SQL query to get each polygon's area and perimeter)

#Example 1
# query_area = """
# SELECT 
#     abc, 
#     ST_Area(geom) AS area,            -- poligona platība (polygon area)
#     ST_Perimeter(geom) AS perimeter   -- poligona perimetrs (polygon perimeter)
# FROM test.poligoni_polygons;
# """

# # Izpildām vaicājumu un iegūstam rezultātus DataFrame formātā
# # (Execute the query and get results as a DataFrame)
# area_df = pd.read_sql(query_area, engine)

# # Apskatām pirmos rezultātu ierakstus (View the first few result records)
# print(area_df.head())

#-- 17.slaids -----------------------------------------------------------------------------------------
#Example 2
# a
# Vaicājums, lai pārbaudītu vai poligoni A, B, C savstarpēji krustojas
# (Query to check if polygons A, B, C intersect each other)
# query_intersects = """
# SELECT 
#     ST_Intersects(A.geom, B.geom) AS intersects_A_B,  -- A un B krustojas? (do A and B intersect?)
#     ST_Intersects(A.geom, C.geom) AS intersects_A_C,  -- A un C krustojas? (do A and C intersect?)
#     ST_Intersects(B.geom, C.geom) AS intersects_B_C   -- B un C krustojas? (do B and C intersect?)
# FROM 
#     test.poligoni_polygons AS A,
#     test.poligoni_polygons AS B,
#     test.poligoni_polygons AS C
# WHERE 
#     A.abc = 'A' AND B.abc = 'B' AND C.abc = 'C';
# """
# bool_df = pd.read_sql(query_intersects, engine)
# print(bool_df)

#-- 18.slaids -----------------------------------------------------------------------------------------
# b
# Vaicājums, lai atrastu visus punktus, kas atrodas poligonā ar abc='A'
# (Query to find all points that lie within the polygon where abc='A')
# query_points_in_A = """
# SELECT 
#     pt.abc point_ABC,            
#     p.abc as poly_ABC   
# FROM 
#     test.punkti_points AS pt
# JOIN 
#     test.poligoni_polygons AS p
# ON 
#     ST_Intersects(pt.geom, p.geom)
# WHERE 
#     p.abc = 'A';
# """
# points_df = pd.read_sql(query_points_in_A, engine)
# print(points_df.head())

#-- 19.slaids -----------------------------------------------------------------------------------------
# Aprēķinām divu poligonu A un B kopējo laukumu (ST_Intersection)
# Compute the overlapping area of two polygons A and B (ST_Intersection)
# query = """
# SELECT ST_AsText(ST_Intersection(A.geom, B.geom)) AS intersection_wkt
# FROM test.poligoni_polygons AS A
# JOIN test.poligoni_polygons AS B
#   ON A.abc = 'A' AND B.abc = 'B';
# """
# # Izpildām SQL vaicājumu un iegūstam rezultātu DataFrame formātā
# # Execute the SQL query and get the result in a DataFrame
# df_intersection = pd.read_sql(query, engine)

# # Izdrukājam iegūto ģeometriju WKT formātā (gaidāms, ka tā būs poligons, kas ir A un B pārklāšanās)
# # Print the resulting geometry in WKT format (expected to be the polygon representing A ∩ B)
# print("Intersection A∩B (WKT):", df_intersection['intersection_wkt'][0])

#-- 24.slaids -----------------------------------------------------------------------------------------
# # Izgriežam to līniju segmentus, kas atrodas poligonā ar abc='A' (izmantojot ST_Intersection)
# # Extract the line segments that lie within polygon 'A' (using ST_Intersection for clipping)
# query_lines = """
# SELECT 
#     ST_AsText(ST_Intersection(l.geom, p.geom)) AS segment_wkt, 
#     l.abc AS line_abc,
#     p.abc AS poly_abc
# FROM test.liinijas_lines AS l
# JOIN test.poligoni_polygons AS p
#   ON ST_Intersects(l.geom, p.geom)
# WHERE p.abc = 'A';
# """
# df_segments = pd.read_sql(query_lines, engine)
# # Parāda pilnu saturu, neapgriežot teksta kolonnas
# with pd.option_context('display.max_colwidth', None):
#     # Parādām dažus iegūtos segmentus (WKT formātā) un to identifikatorus
#     # Display a few of the resulting segments (WKT format) with their identifiers
#     print(df_segments[['line_abc','poly_abc','segment_wkt']].head())

# #-- 21.slaids -----------------------------------------------------------------------------------------
# # Aprēķinām poligona A daļu, kas neietilpst poligonā B (ST_Difference)
# # Compute the part of polygon A that is not inside polygon B (ST_Difference)
# query = """
# SELECT ST_AsText(ST_Difference(A.geom, B.geom)) AS difference_wkt
# FROM test.poligoni_polygons AS A, test.poligoni_polygons AS B
# WHERE A.abc = 'A' AND B.abc = 'B';
# """
# df_difference = pd.read_sql(query, engine)
# print("A \\ B (Difference) WKT:", df_difference['difference_wkt'][0])

# #-- 22.slaids -----------------------------------------------------------------------------------------
# # Aprēķinām poligonu A un B simetrisko starpību – zonas, kas ir tikai A vai tikai B
# # Compute the symmetric difference of polygons A and B – areas that are only in A or only in B
# query = """
# SELECT 
#     ST_AsText(ST_SymDifference(A.geom, B.geom)) AS symdiff_wkt,
#     'A Δ B'::text AS label
# FROM test.poligoni_polygons AS A
# JOIN test.poligoni_polygons AS B
#   ON A.abc = 'A' AND B.abc = 'B';
# """
# df_symdiff = pd.read_sql(query, engine)
# print("Symmetric difference A Δ B (WKT):", df_symdiff['symdiff_wkt'][0])

# #-- 23.slaids -----------------------------------------------------------------------------------------
# # Aprēķinām poligonu A un B apvienojumu vienā ģeometrijā (ST_Union)
# # Compute the union of polygon A and B into a single geometry (ST_Union)
# query = """
# SELECT ST_AsText(ST_Union(A.geom, B.geom)) AS union_wkt
# FROM test.poligoni_polygons AS A
# JOIN test.poligoni_polygons AS B
#   ON A.abc = 'A' AND B.abc = 'B';
# """
# df_union_ab = pd.read_sql(query, engine)
# print("Union of A and B (WKT):", df_union_ab['union_wkt'][0])

# #-- 25.slaids -----------------------------------------------------------------------------------------
# # Izveidojam jaunu tabulu ar līniju segmentiem poligonā A, izmantojot CREATE TABLE ... AS SELECT
# # Create a new table with line segments inside polygon A using CREATE TABLE ... AS SELECT
# from sqlalchemy import text

# # SQL vaicājums
# create_query = text("""
# CREATE TABLE test.line_segments_in_A AS
# SELECT 
#     ST_Intersection(l.geom, p.geom) AS geom,
#     l.abc AS line_abc,
#     p.abc AS poly_abc
# FROM test.liinijas_lines AS l
# JOIN test.poligoni_polygons AS p
#   ON ST_Intersects(l.geom, p.geom)
# WHERE p.abc = 'A';
# """)

# # Atver savienojumu ar datubāzi un izpilda vaicājumu
# # Open connection and execute the query
# with engine.connect() as connection:
#     connection.execute(create_query)
#     connection.commit()   # Apstiprina izmaiņas (Commit the transaction)

#-- 26.slaids -----------------------------------------------------------------------------------------
# # Pārbaudām jaunās tabulas datus un, piemēram, saskaitām katra poligona iekšējo līniju kopgarumu
# # Verify the new table's data and e.g. calculate total length of segments inside each polygon
# MansSQL = """
# select
# 	poly_abc,
# 	COUNT(*) as segment_count,
# 	SUM(ST_Length(geom)) as total_length
# from
# 	test.line_segments_in_A
# group by
# 	poly_abc;
# """
# df_check = pd.read_sql(MansSQL, engine)
# print(df_check)

# #-- 27.slaids -----------------------------------------------------------------------------------------
# -*- coding: utf-8 -*-
# LV: Nolasa PostGIS tabulu test.poligoni_polygons un saglabā abc, perimetru un platību HTML formātā.
# EN: Reads PostGIS table test.poligoni_polygons and saves abc, perimeter, and area as an HTML report.
from sqlalchemy import create_engine, text
import pandas as pd
import os
# ===== 1) Savienojums ar datubāzi =====
# LV: Aizstājiet lietotājvārdu, paroli, hostu un datubāzi ar saviem.
# EN: Replace username, password, host, and database with your own settings.
#                      'postgresql+psycopg2://username:password@localhost:5432/my_database')
engine = create_engine("postgresql+psycopg2://postgres:postgres@localhost:5432/postgres")
# HTML faila ceļš (kur saglabāt rezultātu)
# Path to output HTML file
html_out = "poligoni_report.html"
# ===== 2) Nolasa datus no PostGIS =====
# LV: Atlasām abc, perimetru un platību. ST_Perimeter atgriež garumu (km), ST_Area – platību (km2).
# EN: Select abc, perimeter, and area. ST_Perimeter returns length (km), ST_Area returns area (km2).
with engine.connect() as conn:
    df = pd.read_sql(text("""
select
	abc,
	ROUND((ST_Perimeter(geom)/ 1000)::numeric, 1) as perimetrs_km,
	ROUND((ST_Area(geom)/ 1000000)::numeric, 1) as platiba_km2
from test.poligoni_polygons order by abc;"""),conn)
# ===== 3) Saglabā rezultātu HTML formātā =====
# LV: Saglabā pandas DataFrame kā HTML tabulu (bez indeksa)
# EN: Save the pandas DataFrame as an HTML table (without index)
df.to_html(html_out, index=False)
print("HTML pārskats saglabāts: ")
print(f"   {os.path.abspath(html_out)}")