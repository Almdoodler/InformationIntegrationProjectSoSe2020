from OMDB import *
from TMDB import *
from SimilarityMeasure import *
from Movie import *
import operator


class Mediator:

    def showData(self, value, method):
        omdb = OMDB()
        tmdb = TMDB()
        movies = []
        if method == "1":
            r1 = omdb.search(value)
            r1 = sorted(r1, key=operator.attrgetter("imdbID"), reverse=False)
            r2 = tmdb.search(value)
            r1 = sorted(r1, key=operator.attrgetter("imdbID"), reverse=False)
        elif method == "2":
            r1 = omdb.search_id(value)
            r1 = sorted(r1, key=operator.attrgetter("imdbID"), reverse=False)
            r2 = tmdb.search_id(value)
            r1 = sorted(r1, key=operator.attrgetter("imdbID"), reverse=False)


        print("Result length omdb (r1)", len(r1))
        print("Result length tmdb (r2)", len(r2))
        print("number of results ", len(r1) + len(r2))

        "Kombiniert die movies von r1 und r2 nach der imdb id"
        print('Removing duplicates based on imdb_id')
        for i in reversed(range(0, len(r1))):
            for j in reversed(range(0, len(r2))):
                if r1[i].getImbID() == r2[j].getImbID():
                    # Setze actor und production in r1 auf die Vereinigung der Mengen von r1 und r2
                    actors = r1[i].getActors()|r2[j].getActors()
                    r1[i].setActors(actors)
                    production = r1[i].getProduction()|r2[j].getProduction()
                    r1[i].setProduction(production)
                    del(r2[j])
                    break
        print("Result length omdb", len(r1))
        print("Result length tmdb ", len(r2))
        print("number of results ", len(r1) + len(r2))
  

        "Kombiniert die movies nach similiraity measure"
        sm = SimilarityMeasure()
        similarities = [[-1 for x in range(len(r1))] for y in range(len(r2))]
        print("similirarities ", len(similarities))
        "Berechnet für jeden  film in r2 die Ähnlichkeit zu den Filmen in r1 und schreibt den Wert similarities ein"
        for j in range(0, len(r2)):
            similarity = 0
            for i in range(0, len(r1)):
                x = sm.similar(str(r2[j].getRuntime()), str(r1[i].getRuntime()))
                x = x + sm.similar(str(r2[j].getYear()), str(r1[i].getYear()))
                x = x + sm.similar(str(r2[j].getTitle()), str(r1[i].getTitle()))
                a1 = sorted(r1[i].getActors())
                a2 = sorted(r2[j].getActors())
                seperator = ','
                x = x + sm.similar(seperator.join(a1), seperator.join(a2))

                p1 = sorted(r1[i].getProduction())
                p2 = sorted(r2[j].getProduction())
                seperator = ','
                x = x + sm.similar(seperator.join(p1), seperator.join(p2))

                if similarity < x / 5:
                    similarity = x / 5
                    if (similarity > 0.5):
                        similarities[j][i] = similarity

        "Für jeden Film in r1 wird der Film aus r2 ausgewählt, mit der größten Ähnlichkeit"
        duplicate = []
        used = []
        if len(similarities) > 0:
            for i in range(0, len(r1)):
                max_index = -1
                max_value = -1
                for j in range(0, len(r2)):
                    if (similarities[j][i] > max_value):
                        max_index = j
                        max_value = similarities[j][i]
                if max_index not in used:
                    duplicate.append(max_index)
                    similarities[j] = [-1] * len(r1)
                    used.append(max_index)

        """
        for i in range(0, len(r1)):
            if duplicate[i] > -1:
                print(r1[i].string())
                print(similarities[duplicate[i]][i])
                print(r2[duplicate[i]].string())
                print('----------------------------------------')
            else:
                print(r1[i].string())
                print(similarities[duplicate[i]][i])
                print('----------------------------------------')
        """
        print('Removing duplicates based on similarity')
        "Löscht die Filme aus r2, welche ein identisches Objekt in r1 (wahrscheinlich) besitzen"
        duplicate = sorted(duplicate, reverse= True)
        for index in duplicate:
            
            if index > -1:
                del(r2[index])
        
        print("Result length omdb", len(r1))
        print("Result length tmdb ", len(r2))
        r = r1 + r2

        for movie in r:
            print(movie.string())
            print('----------------------------------------')


if __name__ == "__main__":
    m = Mediator()
    m.showData('tt2911666','2')
    #m.showData('John WIck','1')

