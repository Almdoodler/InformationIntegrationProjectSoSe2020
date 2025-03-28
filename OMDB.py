import requests
from Movie import Movie
import math


class OMDB:
    search_url = 'https://www.omdbapi.com/?apikey=3c011de4&s='
    movie_url = 'https://www.omdbapi.com/?apikey=3c011de4&i='

    """ Gibt Ergebnisse für Film-Suchanfrage 'movieName' zurück. 
    return: movies (list<Movie>) """

    def search(self, movieName):
        r = requests.get(self.search_url + movieName)
        dic = r.json()
        movies = []

        if dic['Response'] == "False":
            print('Failed to fetch results from OMDB')

        elif int(dic['totalResults']) > 0:
            print('Fetching results from OMDB')
            elements = self.cleanResult(dic['Search'], 'movie')
            pages = math.ceil(int(dic['totalResults']) / 10)
            for i in range(2, pages):
                r = requests.get(self.search_url + movieName + '&page=' + str(i))
                elements = elements + self.cleanResult(r.json()['Search'], 'movie')

            for element in elements:
                movies.append(self.createMovie(element))

            for movie in movies:
                r = requests.get(self.movie_url + movie.getImbID())
                dic = r.json()
                production = False
                runtime = False
                acts = False
                keys = dic.keys()

                for key in keys:
                    if key == "Production":
                        if not dic['Production'] == 'N/A':
                            production = True
                            pSet = set()
                            pSet.add(dic['Production'])
                            movie.setProduction(pSet)
                    elif key == "Runtime":
                        if not dic['Runtime'] == 'N/A':
                            runtime = True
                            movie.setRuntime(dic['Runtime'])
                    elif key == "Actors":
                        acts = True
                        actors = set()
                        for actor in dic['Actors'].split(','):
                            if not actor == 'N/A':
                                actors.add(actor.lstrip(' '))
                        movie.setActors(actors)

                if not production:
                    movie.setProduction(set())
                if not runtime:
                    movie.setRuntime(0)
                if not acts:
                    movie.setActors([])
                # print(movie.string())
        print('Finished fetching results from OMDB')
        return movies

    """ Gibt Ergebnis für Film-Suchanfrage 'id' zurück. 
    return: movies (Movie)"""

    def search_id(self, id):
        r = requests.get(self.movie_url + id)
        dic = r.json()
        # print(dic)
        movies = []

        if dic['Response'] == "False":
            print('Failed to fetch results from OMDB')

        else:
            print('Fetching results from OMDB')
            movie = self.createMovie(dic)
            production = False
            runtime = False
            acts = False
            keys = dic.keys()

            for key in keys:
                if key == "Production":
                    production = True
                    pSet = set()
                    pSet.add(dic['Production'])
                    movie.setProduction(pSet)
                elif key == "Runtime":
                    runtime = True
                    movie.setRuntime(dic['Runtime'])
                elif key == "Actors":
                    acts = True
                    actors = set()
                    for actor in dic['Actors'].split(','):
                        if not actor == 'N/A':
                            actors.add(actor.lstrip(' '))
                    movie.setActors(actors)

            if not production:
                movie.setProduction("N/A")
            if not runtime:
                movie.setRuntime(0)
            if not acts:
                movie.setActors([])
            movies.append(movie)
            # print("movie ", movie.string())

        return movies

    """ Entfernt alle anderen Elemente außer Elemente mit type:filter
    return elements (dic) """

    def cleanResult(self, dic, filter):
        delete = []
        for i in range(0, len(dic)):
            if dic[i]['Type'] != filter:
                delete.append(i)
        delete.sort(reverse=True)
        for index in delete:
            del (dic[index])

        return dic

    def createMovie(self, element):

        keys = element.keys()
        con_title = False
        con_year = False
        con_imdbID = False
        for key in keys:
            if key == "Title":
                title = element['Title']
                con_title = True
            elif key == "Year":
                year = element['Year']
                con_year = True
            elif key == "imdbID":
                imdbID = element['imdbID']
                con_imdbID = True

        if not con_title:
            title = 0

        if not con_year:
            year = 0

        if not con_imdbID:
            imdbID = -1

        return Movie(title, year, imdbID)


if __name__ == "__main__":
    s = OMDB()
    s.search_id('tt2911666')
    s.search_id('Naruto')
