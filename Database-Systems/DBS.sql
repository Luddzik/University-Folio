/* (1) List artists who released a live album and a compilation in the same year */
SELECT DISTINCT A1.Artist
FROM ALBUM AS A1, ALBUM AS A2
WHERE A1.Type = 'LIVE' AND A2.Type = 'COMPILATION' AND A1.Year = A2.Year AND A1.Artist = A2.Artist;

SELECT DISTINCT A1.Artist
FROM ALBUM AS A1, ALBUM AS A2
WHERE A1.Type = 'STUDIO' AND (A2.Type != 'COMPILATION' OR A2.Type != 'LIVE') AND A1.Artist = A2.Artist;

SELECT DISTINCT A1.Title, A1.Artist, A1.Year
FROM ALBUM AS A1, ARTIST AS A
WHERE NOT EXISTS ( SELECT * FROM ALBUM AS A2, ARTIST AS AT WHERE A1.Artist = A2.Artist AND A2.Rating < A1.Rating AND AT.Type = 'BAND')
ORDER BY A1.Year DESC;

SELECT A1.Title, A1.Artist
FROM ALBUM AS A1, ARTIST AS A
WHERE A1.Rating < (SELECT AVG(A2.Rating) FROM ALBUM AS A2 WHERE A1.Artist = A2.Artist AND A1.Year = A2.Year GROUP BY A2.Year) AND A.Country = 'British' AND A1.Artist = A.name;

SELECT DISTINCT T.Album_Title, T.Album_Artist
FROM ALBUM AS A, TRACKLIST AS T
WHERE T.Track_Length<2.34 AND A.Year >(2015-20) AND A.Rating >3 AND T.Album_Title = A.Title AND T.Album_Artist = A.Artist;

SELECT AVG(T.Track_Length), A.Year
FROM ALBUM AS A, TRACKLIST AS T
WHERE T.Track_No > 9 AND A.Year>1989 AND A.Year<2000 AND T.Album_Title = A.Title AND T.Album_Artist = A.Artist
GROUP BY A.Year;

SELECT A.ArtistFROM ALBUM AS A, ALBUM AS A2
WHERE A.Title != A2.Title AND A.Artist = A2.Artist AND A.Type = 'STUDIO' AND A2.Type ='STUDIO' AND ((A.Year > A2.Year AND A.Year > (A2.Year +4)) OR (A.Year < A2.Year AND A.Year < (A2.Year -4)));

SELECT DISTINCT A1.ArtistFROM ALBUM AS A1, ALBUM AS A
WHERE (SELECT COUNT(A.Artist) FROM ALBUM AS A WHERE A.Artist = A1.Artist AND A.Type ='STUDIO') < (SELECT COUNT(A1.Artist) FROM ALBUM AS A1 WHERE A1.Type = 'COMPILATION' OR A1.Type = 'LIVE')
GROUP BY A1.Artist;

SELECT T.Album_Title, SUM(T.Track_Length)
FROM TRACKLIST AS T
GROUP BY T.Album_Title;

SELECT A.Artist                            
FROM ALBUM AS A
WHERE (SELECT COUNT(A1.Type) FROM ALBUM AS A1 WHERE A1.Type ='STUDIO' AND A1.Artist = A.Artist)>=3 AND (SELECT COUNT (A1.Type) FROM ALBUM AS A1 WHERE A1.Type ='LIVE' AND A1.Artist = A.Artist) >=2 AND (SELECT COUNT(A1.Type) FROM ALBUM AS A1 WHERE A1.Type ='COMPILATION' AND A1.Artist = A.Artist) >=1 AND A.Rating >=3;

SELECT DISCTINCT A.Artist               
FROM ALBUM AS A, ARTIST AS AT
WHERE AT.Country='US' AND NOT EXISTS(SELECT * FROM ALBUM AS A2 WHERE A.Artist= A2.Artist AND A.Year>A2.Year) AND A.Rating = 5
GROUP BY A.Artist;

SELECT A.Artist, CAST( (Count(A.Rating) *100.00/ (SELECT COUNT(A1.Rating) FROM ALBUM AS A1 WHERE A1.Artist = A.Artist)) AS DECIMAL(5,2) ) AS p
FROM ALBUM AS A
WHERE A.Rating<3
GROUP BY A.Artist;

SELECT A.Artist                               
FROM ALBUM AS A, ARTIST AS AT
WHERE (SELECT COUNT(A2.Type) FROM ALBUM AS A2, ARTIST AS AT2 WHERE A.Artist = A2.Artist AND AT2.Country = AT.Country AND A2.Type ='STUDIO') > (SELECT COUNT(A2.Type) FROM ALBUM AS A2, ARTIST AS AT2 WHERE A.Artist != A2.Artist AND AT2.Country = AT.Country AND A2.Type='STUDIO')
GROUP BY A.Artist;

SELECT A1.Artist, A1.Title,A2.Artist, A2.Title
FROM ARTIST AS A11, ALBUM AS A1, ALBUM AS A2, ARTIST AS A22
WHERE A11.Name = A1.Artist AND A22.Name = A2.Artist AND A11.Country != A22.Country AND A1.Year = A2.Year AND (A1.Rating > A2.Rating OR A2.Rating > A1.Rating);

SELECT (COUNT(T.Track_No) / A.Rating) AS ratio
FROM TRACKLIST AS T, ALBUM AS A
WHERE T.Album_Artist = A.Artist AND T.Album_Title = A.Title;
