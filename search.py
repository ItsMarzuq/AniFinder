import requests

class AnimeSearch:
    BASE_URL = "https://api.jikan.moe/v4"

    def search(self, query):
        response = requests.get(f"{self.BASE_URL}/anime", params={"q": query})
        response.raise_for_status()
        search_result = response.json()
        return search_result['data']

    def get_details(self, anime_id):
        response = requests.get(f"{self.BASE_URL}/anime/{anime_id}")
        response.raise_for_status()
        anime_details = response.json()
        return anime_details['data']

    def get_top_anime(self):
        response = requests.get(f"{self.BASE_URL}/top/anime")
        response.raise_for_status()
        top_anime = response.json()
        return top_anime['data']

    def get_upcoming_anime(self):
        response = requests.get(f"{self.BASE_URL}/seasons/upcoming")
        response.raise_for_status()
        upcoming_anime = response.json()
        return upcoming_anime['data']

    def get_recommendations(self, genres, limit=5):
        response = requests.get(f"{self.BASE_URL}/anime", params={"genres": ','.join(str(g['mal_id']) for g in genres), "limit": limit})
        response.raise_for_status()
        recommendations = response.json()
        return recommendations['data']