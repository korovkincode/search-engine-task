import dotenv
from neo4j import GraphDatabase, basic_auth
import os
from typing import List
import json

FILL_DATABASE = False
SEARCH_QUERY = ("Daniel Radcliffe", "Fantasy")


def parseGenres(movieGenresData: dict) -> List[str]:
	genresList = []
	for genreData in movieGenresData["genres"]:
		genresList.append(genreData["name"])
	return genresList

def parseActors(movieCastData: dict) -> List[str]:
	actorList = []
	for actorData in json.loads(movieCastData["cast"]):
		actorList.append(actorData["name"])
	return actorList


class Database(GraphDatabase):
	__URI: str = ""
	__USERNAME: str = ""
	__PASSWORD: str = ""
	
	
	@classmethod
	def setup(cls):
		dotenv.load_dotenv()
		cls.__URI = os.getenv("NEO4J_URI")
		cls.__USERNAME = os.getenv("NEO4J_USERNAME")
		cls.__PASSWORD = os.getenv("NEO4J_PASSWORD")


	@classmethod
	def driver(cls):
		return super().driver(
			cls.__URI, auth=basic_auth(cls.__USERNAME, cls.__PASSWORD)
		)
	

	@classmethod
	def addMovie(cls, title: str, description: str, year: int, genres: List[str], actors: List[str]):
		with cls.driver().session() as session:
			session.run("""
				MERGE (m:Movie {title: $title})
				SET m.description = $description, m.year = $year

				WITH m
				UNWIND $genres AS genreName
					MERGE (g:Genre {name: genreName})
					MERGE (m)-[:HAS_GENRE]->(g)

				WITH m
				UNWIND $actors AS actorName
					MERGE (a:Actor {name: actorName})
					MERGE (a)-[:ACTED_IN]->(m)
				""",
				title=title, description=description, year=year,
				genres=genres, actors=actors
			)


	@classmethod
	def findMovies(cls, actor: str, genre: str) -> List[str]:
		with cls.driver().session() as session:
			queryResults = session.run(
                """
                MATCH (a:Actor {name: $actor})-[:ACTED_IN]->(m:Movie)-[:HAS_GENRE]->(g:Genre {name: $genre})
                RETURN m.title AS movie
                """,
                actor=actor, genre=genre
            )
			return [record["movie"] for record in queryResults]


Database.setup()
try:
	Database.driver().verify_connectivity()
except Exception as e:
	print(f"FAILURE: {e}")
	exit()


with open("movies.json", encoding="utf-8") as moviesFile:
    moviesData = json.load(moviesFile)

with open("credits.json", encoding="utf-8") as creditsFile:
	creditsData = json.load(creditsFile)


if FILL_DATABASE:
	objIndex = 0
	for movieData in moviesData:
		Database.addMovie(
			Database.addMovie,
			movieData["title"], movieData["overview"], int(movieData["release_date"].split("-")[0]),
			parseGenres(movieData), parseActors(creditsData[objIndex])
		)
		objIndex += 1


print(Database.findMovies(*SEARCH_QUERY))
'''
Result:
[
	'Harry Potter and the Half-Blood Prince', 'Harry Potter and the Order of the Phoenix', 'Harry Potter and the Goblet of Fire',
	'Harry Potter and the Prisoner of Azkaban', "Harry Potter and the Philosopher's Stone", 'Harry Potter and the Chamber of Secrets'
]
'''