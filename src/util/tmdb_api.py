import json
from src.util.config import Config
from src.util.request import requestURLText

class TMDBAPI:
    baseFindURL = 'https://api.themoviedb.org/3/find/{}?api_key={}&language=en-US&external_source=imdb_id'
    baseMovieURL = 'https://api.themoviedb.org/3/movie/{}?api_key={}'
    baseCreditsURL = 'https://api.themoviedb.org/3/movie/{}/credits?api_key={}'
    baseCreditURL = 'https://api.themoviedb.org/3/credit/{}?api_key={}'
    baseVideosURL = 'https://api.themoviedb.org/3/movie/{}/videos?api_key={}'
    baseKeywordURL = 'https://api.themoviedb.org/3/movie/{}/keywords?api_key={}'
    baseKeywordMoviesURL = 'https://api.themoviedb.org/3/keyword/{}/movies?api_key={}&page={}'
    basePersonCreditsURL = 'https://api.themoviedb.org/3/person/{}/movie_credits?api_key={}'
    basePersonURL = 'https://api.themoviedb.org/3/person/{}?api_key={}'
    baseWatchProvidersURL = 'https://api.themoviedb.org/3/movie/{}/watch/providers?api_key={}'
    baseReviewURL = 'https://api.themoviedb.org/3/movie/{}/reviews?api_key={}'
    baseCollectionURL = 'https://api.themoviedb.org/3/collection/{}?api_key={}'
    baseReleaseDatesURL = 'https://api.themoviedb.org/3/movie/{}/release_dates?api_key={}'
    baseMovieDiscover = 'https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=true&language=en-US&page={}&sort_by=vote_count.desc&api_key={}{}'
    apiKey = Config().tmdb_api_key

    def findIMDBResult(self, imdbCode):
        response = requestURLText(self.baseFindURL.format(imdbCode, self.apiKey), cache=False)
        if response is not None and len(response) > 0:
            return json.loads(response)['movie_results']
        else:
            print(f'WARNING: {imdbCode} not found')

    def findIMDBPerson(self, imdbPersonCode):
        return json.loads(requestURLText(self.baseFindURL.format(imdbPersonCode, self.apiKey), cache=False))['person_results']

    def findTMDBCast(self, tmdbCode):
        return json.loads(requestURLText(self.baseCreditsURL.format(tmdbCode, self.apiKey), cache=False))['cast']

    def findTMDBCrew(self, tmdbCode):
        return json.loads(requestURLText(self.baseCreditsURL.format(tmdbCode, self.apiKey), cache=False))['crew']

    def findTMDBCredit(self, creditCode):
        json_response = json.loads(requestURLText(self.baseCreditURL.format(creditCode, self.apiKey), cache=False))
        if 'department' in json_response:
            return json_response['department']

    def getMovieCredits(self, tmdbPersonCode):
        return json.loads(requestURLText(self.basePersonCreditsURL.format(tmdbPersonCode, self.apiKey), cache=False))['cast']

    def getPersonCrewList(self, tmdbCode):
        return json.loads(requestURLText(self.basePersonCreditsURL.format(tmdbCode, self.apiKey), cache=False))['crew']

    def getMovieDetails(self, tmdbCode):
        return json.loads(requestURLText(self.baseMovieURL.format(tmdbCode, self.apiKey), cache=False))

    def getPersonDetails(self, tmdbCode):
        return json.loads(requestURLText(self.basePersonURL.format(tmdbCode, self.apiKey), cache=False))

    def findVideos(self, imdbCode):
        result = self.findIMDBResult(imdbCode)
        if len(result) == 0:
            print('IMDB {} is missing'.format(imdbCode))
            return None, []
        else:
            id = result[0]['id']
            return json.loads(requestURLText(self.baseVideosURL.format(id, self.apiKey), cache=False))

    def getYouTubeTrailers(self, imdbOrTmdbCode):
        if 'imdb.com' in imdbOrTmdbCode:
            videos = self.findVideos(imdbOrTmdbCode)
        else:
            videos = json.loads(requestURLText(self.baseVideosURL.format(imdbOrTmdbCode, self.apiKey), cache=False))
        trailers = [a for a in videos['results'] if a['site'] == 'YouTube' and a['type'] == 'Trailer']
        return trailers

    def findCastList(self, imdbCode):
        result = self.findIMDBResult(imdbCode)
        if len(result) == 0:
            print('IMDB {} is missing'.format(imdbCode))
            return None, []
        else:
            id = result[0]['id']
            return id, self.findTMDBCast(id)

    def findCrewList(self, imdbCode):
        result = self.findIMDBResult(imdbCode)
        if len(result) == 0:
            print('IMDB {} is missing'.format(imdbCode))
            return None, []
        else:
            id = result[0]['id']
            return id, self.findTMDBCrew(id)

    def findKeywords(self, tmdbCode):
        result = json.loads(requestURLText(self.baseKeywordURL.format(tmdbCode, self.apiKey), cache=False))
        return {a['id']: a['name'] for a in result['keywords']}

    def findMoviesForKeywords(self, tmdbKeywordCode):
        results = json.loads(requestURLText(self.baseKeywordMoviesURL.format(tmdbKeywordCode, self.apiKey, 1), cache=False))
        output = results['results']
        return set([a['id'] for a in output])

    def getWatchProviders(self, tmdbCode):
        results = json.loads(requestURLText(self.baseWatchProvidersURL.format(tmdbCode, self.apiKey), cache=False))
        output = results['results'].get('US', {})
        return {key: value if key == 'link' else [a['provider_name'] for a in value] for key, value in output.items()}

    def getCollectionDetails(self, tmdbCollectionCode):
        return json.loads(requestURLText(self.baseCollectionURL.format(tmdbCollectionCode, self.apiKey), cache=False))

    def getCollection(self, tmdbCode):
        details = self.getMovieDetails(tmdbCode)
        return self.getCollectionDetails(details['belongs_to_collection']['id'])

    def getReviews(self, tmdbCode):
        results = json.loads(requestURLText(self.baseReviewURL.format(tmdbCode, self.apiKey), cache=False))
        return results['results']

    def getReleaseDates(self, tmdbCode):
        results = json.loads(requestURLText(self.baseReleaseDatesURL.format(tmdbCode, self.apiKey), cache=False))
        return results['results']

    def searchMovieYear(self, year, maxResults=250):
        results = []
        page = 1
        new_results = json.loads(requestURLText(self.baseMovieDiscover.format(page, self.apiKey, f'&primary_release_year={year}'), cache=False))['results']
        while len(results) < maxResults and len(new_results) > 0:
            results += new_results
            page += 1
            new_results = json.loads(requestURLText(self.baseMovieDiscover.format(page, self.apiKey, f'&primary_release_year={year}'), cache=False))['results']
        return results[:maxResults]