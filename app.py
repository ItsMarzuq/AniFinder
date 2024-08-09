from flask import Flask, request, render_template, redirect, url_for, session
from search import AnimeSearch

app = Flask(__name__)
app.config.from_pyfile('config.py')
search = AnimeSearch()


@app.route('/')
def homepage():
    top_anime = search.get_top_anime()
    upcoming_anime = search.get_upcoming_anime()
    return render_template('home.html', top_anime=top_anime, upcoming_anime=upcoming_anime)

@app.route('/search')
def index():
    query = request.args.get('query')
    results = []
    if query:
        results = search.search(query)
    return render_template('index.html', results=results, query=query)

@app.route('/details/<int:anime_id>')
def details(anime_id):
    details = search.get_details(anime_id)
    recommendations = search.get_recommendations(details['genres'])
    is_in_wishlist = anime_id in session.get('wishlist', [])
    return render_template('details.html', anime=details, recommendations=recommendations, is_in_wishlist=is_in_wishlist)

@app.route('/wishlist', methods=['GET'])
def wishlist():
    wishlist_anime_ids = session.get('wishlist', [])
    wishlist_anime = [search.get_details(anime_id) for anime_id in wishlist_anime_ids]
    return render_template('wishlist.html', wishlist=wishlist_anime)

@app.route('/add_to_wishlist/<int:anime_id>', methods=['POST'])
def add_to_wishlist(anime_id):
    wishlist = session.get('wishlist', [])
    if anime_id not in wishlist:
        wishlist.append(anime_id)
    session['wishlist'] = wishlist
    return redirect(url_for('details', anime_id=anime_id))

@app.route('/remove_from_wishlist/<int:anime_id>', methods=['POST'])
def remove_from_wishlist(anime_id):
    wishlist = session.get('wishlist', [])
    if anime_id in wishlist:
        wishlist.remove(anime_id)
    session['wishlist'] = wishlist
    return redirect(url_for('details', anime_id=anime_id))

if __name__ == '__main__':
    app.run(debug=True)
