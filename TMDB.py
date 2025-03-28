import requests
from Movie import Movie


class TMDB:
    search_url = 'https://api.themoviedb.org/3/search/movie'
    query = '&query='
    movie_url = 'https://api.themoviedb.org/3/movie/'
    find_id_url = 'https://api.themoviedb.org/3/find/'
    credits = '/credits'
    api_key = '<key_removed>'
    languange = '&lang=en_US'

    # Gibt Ergebnisse für Suchanfrage mittels movieName zurück;
    # Zurückgegbene Liste ist leer, falls keine Ergebnisse gefunden wurden

    def search(self, movie_name):
        r = requests.get(self.search_url + self.api_key + self.query + movie_name)
        dic = r.json()
        movies = []
        if int(dic['total_results']) >= 1:
            print('Fetching ' + str(dic['total_results']) + ' results on ' + str(dic['total_pages']) + ' pages from TMDB')
            i = 1
            while i <= dic['total_pages']:
                print('Fetching details for results on page: ' + str(i))
                req = requests.get(self.search_url + self.api_key + self.query + movie_name + '&page=' + str(i))
                current_page = req.json()
                movies.extend(create_movies(self, current_page['results']))
                i += 1
        else:
            print('Nothing found')
            movies = []
        print('Finished fetching ' + str(dic['total_results']) + ' results from TMDB')
        return movies

    def search_id(self, imdb_id):
        r = requests.get(self.find_id_url + str(imdb_id) + self.api_key + '&external_source=imdb_id')
        search_result = r.json()
        movies = []
        if 'movie_results' in search_result:
            if len(search_result['movie_results']) >= 1:
                print('Fetching result from TMDB')
                movies.extend(create_movies(self, search_result['movie_results']))
            else:
                print('Nothing found')
        return movies


# Request details for each result in results;
# if details does not contain a release_date element or the element is empty, the year will be set to 0;
# if details does not contain a imdb_id element or the element is emtpy or "None", imdb_id will be set to -1;

def create_movies(self, results):
    movies = []
    for element in results:
        r = requests.get(self.movie_url + str(element['id']) + self.api_key)
        details = r.json()
        cast = get_cast(self, element)
        if 'release_date' in details:  # Check whether details even contains a release date
            if str(details['release_date']) and not details['release_date'].isspace():
                year = details['release_date'].split('-')[0]
            else:
                year = 0
        else:
            year = 0
        if 'imdb_id' in details:  # Check whether details even contains a imdb_id
            if str(details['imdb_id']) and not str(details['imdb_id']).isspace() and not str(
                    details['imdb_id']).lower() == 'none':
                imdb_id = details['imdb_id']
            else:
                imdb_id = -1
        else:
            imdb_id = -1
        if 'production_companies' in details:
            production = set()
            for production_company in details['production_companies']:
                production.add(production_company['name'])
        else:
            production = set()
        if 'runtime' in details:
            runtime = details['runtime']
        else:
            runtime = 0
        movie = Movie(element['title'], year, imdb_id)
        movie.setProduction(production)
        movie.setRuntime(runtime)
        movie.setActors(cast)
        movies.append(movie)
    return movies


def get_cast(self, element):
    r = requests.get(self.movie_url + str(element['id']) + '/credits' + self.api_key)
    cast = r.json()
    cast_members = set()
    if 'cast' in cast:
        for member in cast['cast']:
            cast_members.add(member['name'])
    return cast_members


if __name__ == "__main__":
    s = TMDB()
    result = s.search_id('tt2911666')
    for element in result:
        print(element.string())
