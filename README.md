# Information-Integration-project 
## About:
Project integrates IMDB (via OMDB api) and TMDB into one query "database", movies can be queried via their respective ids in either database or their title.
Result includes Title, release date, runtime, production companies, imdb and cast.
## Usage:
1. Run [Main.py](Main.py)
2. Enter a movie title or imdbID
3. If a correpsonding movie (or mulitple) is found the results from both databases will be combined and displayed, if not no result will be displayed and you can enter another movie title or imdbID
## Caveats:

* API keys have been removed, making the project non-working
* 4 Students worked on the project, Markus worked mostly on querying OMDB and TMDB and parts of the main interface, while others worked on the mediator and similarity measures. 
* Comments are a mix of english and german since we never agreed on a default language.
* Entity Resolution is not working correctly sometimes resulting in some of the cast and production company being listed more than once.