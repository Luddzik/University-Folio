/* 
Name: Ludwik Bacmaga

Coursework for Database Systems
*/

/*For Part 1*/
/* Create Tables*/
CREATE TYPE artisttype AS ENUM ('PERSON','BAND');

CREATE TYPE albumtype AS ENUM('STUDIO','LIVE','COMPILATION');

CREATE TABLE ARTIST(                                    
Name varchar(50) NOT NULL,
Type artisttype,
Country varchar(50),
UNIQUE(Name),
PRIMARY KEY(Name));


CREATE TABLE ALBUM(                  
Title varchar(50) NOT NULL,
Artist varchar(50) NOT NULL,
Year integer,
Type albumtype,
Rating integer,
FOREIGN KEY(Artist) REFERENCES ARTIST(Name),
PRIMARY KEY(Title,Artist));


CREATE TABLE TRACKLIST(              
Album_Title varchar(50) NOT NULL,
Album_Artist varchar(50) NOT NULL,
Track_No integer NOT NULL,
Track_Title varchar(50),
Track_Length decimal,
FOREIGN KEY(Album_Title,Album_Artist) REFERENCES ALBUM(Title,Artist),
PRIMARY KEY(Album_Title,Album_Artist,Track_No));

/*Add data into tables, creating database*/
INSERT INTO ARTIST VALUES ('Rise Against', 'BAND', 'US');
INSERT INTO ARTIST VALUES ('Strawberry King', 'PERSON', 'Norway');
INSERT INTO ARTIST VALUES ('Kelly Clarkson', 'PERSON', 'US');
INSERT INTO ARTIST VALUES ('U2', 'BAND', 'US');
INSERT INTO ARTIST VALUES ('Maroon5', 'BAND', 'British');

INSERT INTO ALBUM VALUES ('The Black Market', 'Rise Against', 2014, 'STUDIO', 4);
INSERT INTO ALBUM VALUES ('I Tunes From Inland Lakes', 'Strawberry King', 2013, 'LIVE', 2);
INSERT INTO ALBUM VALUES ('Breakaway', 'Kelly Clarkson', 2004, 'COMPILATION', 4);
INSERT INTO ALBUM VALUES ('Hands All Over', 'Maroon5', 2011, 'LIVE', 4);
INSERT INTO ALBUM VALUES ('War', 'U2', 1983, 'COMPILATION', 3);
INSERT INTO ALBUM VALUES ('Not This Again', 'Strawberry King', 2013, 'COMPILATION', 4);

INSERT INTO TRACKLIST VALUES ('The Black Market', 'Rise Against', 1, 'The Great Die-Off', 3.40);
INSERT INTO TRACKLIST VALUES ('The Black Market', 'Rise Against', 2, 'The Black Market', 4.17);
INSERT INTO TRACKLIST VALUES ('The Black Market', 'Rise Against', 3, 'Sudden Life', 4.08);
INSERT INTO TRACKLIST VALUES ('The Black Market', 'Rise Against', 4, 'Bridges', 4.07);
INSERT INTO TRACKLIST VALUES ('The Black Market', 'Rise Against', 5, 'Awake Too Long', 3.12);

INSERT INTO TRACKLIST VALUES ('I Tunes From Inland Lakes', 'Strawberry King', 1, 'Someday', 3.20);
INSERT INTO TRACKLIST VALUES ('I Tunes From Inland Lakes', 'Strawberry King', 2, 'My Sleeping Animals', 3.57);
INSERT INTO TRACKLIST VALUES ('I Tunes From Inland Lakes', 'Strawberry King', 3, 'Dream In', 4.51);
INSERT INTO TRACKLIST VALUES ('I Tunes From Inland Lakes', 'Strawberry King', 4, 'Lullaby For Him', 3.54);
INSERT INTO TRACKLIST VALUES ('I Tunes From Inland Lakes', 'Strawberry King', 5, 'Riot', 3.33);

INSERT INTO TRACKLIST VALUES ('Breakaway', 'Kelly Clarkson', 1, 'Breakaway', 3.57);
INSERT INTO TRACKLIST VALUES ('Breakaway', 'Kelly Clarkson', 2, 'Gone', 3.27);
INSERT INTO TRACKLIST VALUES ('Breakaway', 'Kelly Clarkson', 3, 'Addicted', 3.57);
INSERT INTO TRACKLIST VALUES ('Breakaway', 'Kelly Clarkson', 4, 'Walk Away', 3.08);
INSERT INTO TRACKLIST VALUES ('Breakaway', 'Kelly Clarkson', 5, 'Hear Me', 3.56);

INSERT INTO TRACKLIST VALUES ('Hands All Over', 'Maroon5', 1, 'Misery', 3.36);
INSERT INTO TRACKLIST VALUES ('Hands All Over', 'Maroon5', 2, 'Stutter', 3.14);
INSERT INTO TRACKLIST VALUES ('Hands All Over', 'Maroon5', 3, 'Hands All Over', 3.13);
INSERT INTO TRACKLIST VALUES ('Hands All Over', 'Maroon5', 4, 'Runaway', 3.01);
INSERT INTO TRACKLIST VALUES ('Hands All Over', 'Maroon5', 5, 'Last Chance', 3.10);

INSERT INTO TRACKLIST VALUES ('War', 'U2', 1, 'Seconds', 3.09);
INSERT INTO TRACKLIST VALUES ('War', 'U2', 2, 'New Year Day', 5.38);
INSERT INTO TRACKLIST VALUES ('War', 'U2', 3, 'Like A Song..', 4.48);
INSERT INTO TRACKLIST VALUES ('War', 'U2', 4, 'The Refugee', 3.40);
INSERT INTO TRACKLIST VALUES ('War', 'U2', 5, 'Red Light', 3.46);

INSERT INTO TRACKLIST VALUES ('Not This Again', 'Strawberry King', 1, 'One More Time', 3.12);
INSERT INTO TRACKLIST VALUES ('Not This Again', 'Strawberry King', 2, 'Forgive Me', 1.20);
INSERT INTO TRACKLIST VALUES ('Not This Again', 'Strawberry King', 3, 'A Day To Remember', 2.56);
INSERT INTO TRACKLIST VALUES ('Not This Again', 'Strawberry King', 4, 'Hakuna Matata', 5.10);
INSERT INTO TRACKLIST VALUES ('Not This Again', 'Strawberry King', 5, 'This Is Lost', 3.34);

/*Tables*/
SELECT * FROM ARTIST;
      name       |  type  | country 
-----------------+--------+---------
 Rise Against    | BAND   | US
 Strawberry King | PERSON | Norway
 Kelly Clarkson  | PERSON | US
 U2              | BAND   | US
 Maroon5         | BAND   | British
(5 rows)

SELECT * FROM ALBUM;
           title           |     artist      | year |    type     | rating 
---------------------------+-----------------+------+-------------+--------
 The Black Market          | Rise Against    | 2014 | STUDIO      |      4
 I Tunes From Inland Lakes | Strawberry King | 2013 | LIVE        |      2
 Breakaway                 | Kelly Clarkson  | 2004 | COMPILATION |      4
 Hands All Over            | Maroon5         | 2011 | LIVE        |      4
 War                       | U2              | 1983 | COMPILATION |      3
 Not This Again            | Strawberry King | 2013 | COMPILATION |      4
(6 rows)

SELECT * FROM TRACKLIST;
        album_title        |  album_artist   | track_no |     track_title     | track_length 
---------------------------+-----------------+----------+---------------------+--------------
 The Black Market          | Rise Against    |        1 | The Great Die-Off   |         3.40
 The Black Market          | Rise Against    |        2 | The Black Market    |         4.17
 The Black Market          | Rise Against    |        3 | Sudden Life         |         4.08
 The Black Market          | Rise Against    |        4 | Bridges             |         4.07
 The Black Market          | Rise Against    |        5 | Awake Too Long      |         3.12
 I Tunes From Inland Lakes | Strawberry King |        1 | Someday             |         3.20
 I Tunes From Inland Lakes | Strawberry King |        2 | My Sleeping Animals |         3.57
 I Tunes From Inland Lakes | Strawberry King |        3 | Dream In            |         4.51
 I Tunes From Inland Lakes | Strawberry King |        4 | Lullaby For Him     |         3.54
 I Tunes From Inland Lakes | Strawberry King |        5 | Riot                |         3.33
 Breakaway                 | Kelly Clarkson  |        1 | Breakaway           |         3.57
 Breakaway                 | Kelly Clarkson  |        2 | Gone                |         3.27
 Breakaway                 | Kelly Clarkson  |        3 | Addicted            |         3.57
 Breakaway                 | Kelly Clarkson  |        4 | Walk Away           |         3.08
 Breakaway                 | Kelly Clarkson  |        5 | Hear Me             |         3.56
 Hands All Over            | Maroon5         |        1 | Misery              |         3.36
 Hands All Over            | Maroon5         |        2 | Stutter             |         3.17
 Hands All Over            | Maroon5         |        3 | Hands All Over      |         3.13
 Hands All Over            | Maroon5         |        4 | Runaway             |         3.01
 Hands All Over            | Maroon5         |        5 | Last Chance         |         3.10
 War                       | U2              |        1 | Seconds             |         3.09
 War                       | U2              |        2 | New Year Day        |         5.38
 War                       | U2              |        3 | Like A Song..       |         4.48
 War                       | U2              |        4 | The Refugee         |         3.40
 War                       | U2              |        5 | Red Light           |         3.46
 Not This Again            | Strawberry King |        1 | One More Time       |         3.12
 Not This Again            | Strawberry King |        2 | Forgive me          |         1.20
 Not This Again            | Strawberry King |        3 | A Day To Remember   |         2.56
 Not This Again            | Strawberry King |        4 | Hakuna Matata       |         5.10
 Not This Again            | Strawberry King |        5 | This Is Lost        |         3.34
(30 rows)

/*For Part 2*/
/*(1) List artists who released a live album and a compilation in the same year*/
SELECT DISTINCT A1.Artist
FROM ALBUM AS A1, ALBUM AS A2
WHERE A1.Type = 'LIVE' AND A2.Type = 'COMPILATION' AND A1.Year = A2.Year AND A1.Artist = A2.Artist;

/*(2) List artists who have only released studio albums.*/
SELECT DISTINCT A1.Artist
FROM ALBUM AS A1, ALBUM AS A2
WHERE A1.Type = 'STUDIO' AND (A2.Type != 'COMPILATION' OR A2.Type != 'LIVE') AND A1.Artist = A2.Artist;

/*(3) List albums which have a higher rating than every previous album by the same band.*/
SELECT DISTINCT A1.Title, A1.Artist, A1.Year
FROM ALBUM AS A1, ARTIST AS A
WHERE NOT EXISTS ( SELECT * FROM ALBUM AS A2, ARTIST AS AT WHERE A1.Artist = A2.Artist AND A2.Rating < A1.Rating AND AT.Type = 'BAND')
ORDER BY A1.Year DESC;

/*(4) List live albums released by British artists and having a higher rating than the average rating of all albums released in the same year.*/
SELECT A1.Title, A1.Artist
FROM ALBUM AS A1, ARTIST AS A
WHERE A1.Rating < (SELECT AVG(A2.Rating) FROM ALBUM AS A2 WHERE A1.Artist = A2.Artist AND A1.Year = A2.Year GROUP BY A2.Year) AND A.Country = 'British' AND A1.Artist = A.name;

/*(5) List songs shorter than 2 minutes and 34 seconds from albums rated 4 or 5 stars and released in the last 20 years. Include the album title and artist name in the output.*/
SELECT DISTINCT T.Album_Title, T.Album_Artist
FROM ALBUM AS A, TRACKLIST AS T
WHERE T.Track_Length<2.34 AND A.Year >(2015-20) AND A.Rating >3 AND T.Album_Title = A.Title AND T.Album_Artist = A.Artist;

/*(6) Find the average total running time of all albums released in the ’90s and having at least 10 tracks. (Assume no track is missing in the tracklist)*/
SELECT AVG(T.Track_Length), A.Year
FROM ALBUM AS A, TRACKLIST AS T
WHERE T.Track_No > 9 AND A.Year>1989 AND A.Year<2000 AND T.Album_Title = A.Title AND T.Album_Artist = A.Artist
GROUP BY A.Year;

/*(7) List artists who have never released two consecutive studio albums more than 4 years apart.*/
SELECT A.ArtistFROM ALBUM AS A, ALBUM AS A2
WHERE A.Title != A2.Title AND A.Artist = A2.Artist AND A.Type = 'STUDIO' AND A2.Type ='STUDIO' AND ((A.Year > A2.Year AND A.Year > (A2.Year +4)) OR (A.Year < A2.Year AND A.Year < (A2.Year -4)));

/*(8) List artists who have released more live and compilation albums (together) than studio ones.*/
SELECT DISTINCT A1.ArtistFROM ALBUM AS A1, ALBUM AS A
WHERE (SELECT COUNT(A.Artist) FROM ALBUM AS A WHERE A.Artist = A1.Artist AND A.Type ='STUDIO') < (SELECT COUNT(A1.Artist) FROM ALBUM AS A1 WHERE A1.Type = 'COMPILATION' OR A1.Type = 'LIVE')
GROUP BY A1.Artist;

/*(9) Assuming that the last track of every album is always present, list albums without missing tracks and their total running time.*/
SELECT T.Album_Title, SUM(T.Track_Length)
FROM TRACKLIST AS T
GROUP BY T.Album_Title;
/* I know that in this this query we need to compare to count the tracks for each album and compare it to the maximum track number to see if they are equal.

/*(10) Among artists who have released at least 3 studio albums, 2 live albums and one compilation, list those whose every album is rated no less than 3.*/
SELECT A.Artist                            
FROM ALBUM AS A
WHERE (SELECT COUNT(A1.Type) FROM ALBUM AS A1 WHERE A1.Type ='STUDIO' AND A1.Artist = A.Artist)>=3 AND (SELECT COUNT (A1.Type) FROM ALBUM AS A1 WHERE A1.Type ='LIVE' AND A1.Artist = A.Artist) >=2 AND (SELECT COUNT(A1.Type) FROM ALBUM AS A1 WHERE A1.Type ='COMPILATION' AND A1.Artist = A.Artist) >=1 AND A.Rating >=3;

/*(11) Find the number of US bands whose debut album was rated 5 stars. (Assume that there is only one such album per artist)*/
SELECT DISCTINCT A.Artist               
FROM ALBUM AS A, ARTIST AS AT
WHERE AT.Country='US' AND NOT EXISTS(SELECT * FROM ALBUM AS A2 WHERE A.Artist= A2.Artist AND A.Year>A2.Year) AND A.Rating = 5
GROUP BY A.Artist;

/*(12) For every artist, find the percentage p of their albums rated less than 3. Return artist names with a lower p first and include p in the output as a number between 0 and 100 with 2 decimal digits.*/
SELECT A.Artist, CAST( (Count(A.Rating) *100.00/ (SELECT COUNT(A1.Rating) FROM ALBUM AS A1 WHERE A1.Artist = A.Artist)) AS DECIMAL(5,2) ) AS p
FROM ALBUM AS A
WHERE A.Rating<3
GROUP BY A.Artist;

/*(13) List artists who released no fewer studio albums than any other artist from the same country.*/
SELECT A.Artist                               
FROM ALBUM AS A, ARTIST AS AT
WHERE (SELECT COUNT(A2.Type) FROM ALBUM AS A2, ARTIST AS AT2 WHERE A.Artist = A2.Artist AND AT2.Country = AT.Country AND A2.Type ='STUDIO') > (SELECT COUNT(A2.Type) FROM ALBUM AS A2, ARTIST AS AT2 WHERE A.Artist != A2.Artist AND AT2.Country = AT.Country AND A2.Type='STUDIO')
GROUP BY A.Artist;

/*(14) List pairs of albums released by artists of different countries in the same year and such that one has a higher rating than the other.*/
SELECT A1.Artist, A1.Title,A2.Artist, A2.Title
FROM ARTIST AS A11, ALBUM AS A1, ALBUM AS A2, ARTIST AS A22
WHERE A11.Name = A1.Artist AND A22.Name = A2.Artist AND A11.Country != A22.Country AND A1.Year = A2.Year AND (A1.Rating > A2.Rating OR A2.Rating > A1.Rating);

/*(15) Sort albums by the ratio (highest first) between their rating and the number of tracks they consist of. (Assume no track is missing in the tracklist)*/
SELECT (COUNT(T.Track_No) / A.Rating) AS ratio
FROM TRACKLIST AS T, ALBUM AS A
WHERE T.Album_Artist = A.Artist AND T.Album_Title = A.Title;
