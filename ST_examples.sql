/*select
	ST_Equals(F.geom,G.geom)
from
	test.punkti_points as F,
	test.punkti_points as G
where 
	F.abc = 'F'
and 
	G.abc = 'G'*/



/*
select
	ST_GeometryType(geom)
from
	test.poligoni_polygons
limit 1
*/


/*
select
	ST_Dimension(geom)
from
	test.poligoni_polygons
limit 1
*/


/*select
	ST_SRID(geom)
from
	test.poligoni_polygons
limit 1*/




/*select
	ST_Envelope(geom)
from
	test.poligoni_polygons
limit 1*/


/*select 
	abc,
	ST_Area(geom),
	ST_Perimeter(geom)
from
	test.poligoni_polygons*/



/*select
	abc,
	ST_Centroid(geom)
from
	test.poligoni_polygons*/
	
/*select
	abc,
	ST_Length(geom)
from
	test.liinijas_lines*/


/*select
	ST_Distance(F.geom, G.geom),
	ST_DistanceSphere (ST_Transform(F.geom,4326), ST_Transform(G.geom,4326))
from
	test.punkti_points as F,
	test.punkti_points as G
where 
	F.abc = 'F'
	and 
	G.abc = 'G'*/

/*select
	ST_Distance(D.geom, E.geom)
from
	test.liinijas_lines as D,
	test.liinijas_lines as E
where 
	D.abc = 'D'
	and 
	E.abc = 'E'*/
	
/*select
	ST_Intersects(A.geom, B.geom) as "A ar B",
	ST_Intersects(A.geom, C.geom) as "A ar C",
	ST_Intersects(B.geom, C.geom) as "B ar C"
from
	 test.poligoni_polygons as A,
	 test.poligoni_polygons as B,
	 test.poligoni_polygons as C
where 
	A.abc = 'A'
	and 
	B.abc = 'B'
	and 
	C.abc = 'C'*/


/*select
	ST_Contains (A.geom, F.geom) as "Vai A satur F?",
	ST_Contains (A.geom, G.geom) as "Vai A satur G?"
from
	 test.poligoni_polygons as A,
	 test.punkti_points as F,
	 test.punkti_points as G
where 
	A.abc = 'A'
	and 
	F.abc = 'F'
	and 
	G.abc = 'G'*/

/*select
	ST_Intersection (A.geom,
	B.geom)
from
	test.poligoni_polygons as A,
	test.poligoni_polygons as B
where 
	A.abc = 'A'
	and 
	B.abc = 'B'*/

/*select
	ST_Difference (A.geom,
	B.geom)
from
	test.poligoni_polygons as A,
	test.poligoni_polygons as B
where 
	A.abc = 'A'
	and 
	B.abc = 'B'*/

/*select
	ST_SymDifference (A.geom,
	B.geom)
from
	test.poligoni_polygons as A,
	test.poligoni_polygons as B
where 
	A.abc = 'A'
	and 
	B.abc = 'B'*/

/*select
	ST_Union (A.geom,
	B.geom)
from
	test.poligoni_polygons as A,
	test.poligoni_polygons as B
where 
	A.abc = 'A'
	and 
	B.abc = 'B'*/

/*select
	ST_Union (A.geom,
	B.geom)
from
	test.poligoni_polygons as A,
	test.poligoni_polygons as B
where 
	A.abc = 'A'
	and 
	B.abc = 'B'*/


/*select 
	ST_Union(geom)
from
	test.poligoni_polygons*/


/*select
	punkti.*
from
	test.punkti_points as punkti
join test.poligoni_polygons as poligoni
  on
	ST_Intersects(punkti.geom, poligoni.geom)
where
	poligoni.abc = 'A';*/

/*--Izveido jaunu tabulu ar to līniju segmentiem,
-- kas atrodas poligonā ar abc='A'.
-- Funkcija ST_Intersection izgriež tos līnijas gabalus, kas atrodas iekšpusē:
select
	ST_Intersection(l.geom, p.geom) as geom,
	l.abc as line_abc,
	p.abc as poly_abc
from
	test.liinijas_lines as l
join test.poligoni_polygons as p
  on
	ST_Intersects(l.geom, p.geom)
where
	p.abc = 'A';*/

/*--Sagrupē pēc poligonu atribūta abc un saskaita,
-- cik punktu atrodas katrā poligonā. ST_Contains
-- vai ST_Within pārbauda telpisko attiecību
select
	p.abc as poly_abc,
	COUNT(pt.*) as point_count
from
	test.poligoni_polygons as p
left join test.punkti_points as pt
  on
	ST_Contains(p.geom, pt.geom)
group by
	p.abc;*/


/*--Apkopo līniju garumu (metriem) katrā poligonā.
-- Pirmkārt, iegūst līnijas–poligona šķēlumu,
-- tad izmanto ST_Length un sagrupē pēc poligonu abc:
select
	p.abc as poly_abc,
	SUM(ST_Length(ST_Intersection(l.geom, p.geom))) as total_length
from
	test.poligoni_polygons as p
join test.liinijas_lines as l
  on
	ST_Intersects(l.geom, p.geom)
group by
	p.abc;*/

/*--Izveido X metru buferi ap katru līniju un atlasa poligonus,
-- kurus šis buferis skar.
select
	distinct p.abc as poly_abc,
	l.abc as line_abc
from
	test.liinijas_lines as l
join test.poligoni_polygons as p
  on
	ST_Intersects(ST_Buffer(l.geom, 20000), p.geom);*/

/*--Apvieno visus poligonus, kuriem abc ir vienāds
select
	abc,
	ST_Union(geom) as geom
from
	test.poligoni_polygons
group by
	abc;*/

/*select
	p.abc as poly_abc, 	pt.abc as point_abc,
	ST_Distance(ST_Centroid(p.geom), pt.geom) as distance_m
from
	test.poligoni_polygons as p
cross join lateral (
	select
		pt.*
	from
		test.punkti_points as pt
	order by
		ST_Distance(ST_Centroid(p.geom), pt.geom)
	limit 1 ) as pt;*/

/*--Izmanto ST_Area un grupē pēc abc,
--lai aprēķinātu katras kategorijas kopējo platību
select
	abc,
	ROUND(SUM(ST_Area(geom))) as total_area
from
	test.poligoni_polygons
group by
	abc
order by total_area desc;*/

/*--Izveido jaunu tabulu ar poligonu centroidiem un oriģinālajiem atribūtiem,
--lai vēlāk ērti vizualizētu vai sasaistītu ar citiem datiem:
create table test.polygons_centroids as
select
	abc,
	ST_Centroid(geom) as geom
from
	test.poligoni_polygons;
select * from test.polygons_centroids;*/


/*
--Simetriskā starpība starp poligoniem A un B (tikai A vai tikai B zonas)
--create table test.poly_symdiff_a_b as
select
	ST_SymDifference(a.geom, b.geom) as geom,
	'A Δ B'::text as label
from
	test.poligoni_polygons a
join test.poligoni_polygons b
  on
	a.abc = 'A'
	and b.abc = 'B';
*/

/*--Attiecību klasifikācija starp līnijām un poligonu ‘A’
-- (crosses/touches/within/disjoint)
select
	l.abc as line_abc,
	case
		when ST_Crosses(l.geom, p.geom) then 'crosses'
		when ST_Touches(l.geom, p.geom) then 'touches'
		when ST_Within(l.geom, p.geom) then 'within'
		when ST_Disjoint(l.geom, p.geom) then 'disjoint'
		else 'intersects_other'
	end as relation_to_A
from
	test.liinijas_lines l
left join test.poligoni_polygons p on p.abc = 'A';*/