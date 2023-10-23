from flask import Flask, request, jsonify
from main import df, cosine_sim
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
# Your get_recommendations function
def get_recommendations(movie_title, cosine_sim, num_recommendations=5):
    # ... (Your existing function code)
    idx = df[df['Original Title'] == movie_title].index[0]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:(num_recommendations+1)]  # Top N similar movies (excluding itself)
    movie_indices = [i[0] for i in sim_scores]
    return df[['Original Title', 'Weighted Rating']].iloc[movie_indices]

# Define an API route to get movie recommendations
@app.route('/get_recommendations', methods=['GET'])
def get_movie_recommendations():
    movie_title = request.args.get('movie_title', default='', type=str)
    
    if not movie_title:
        return jsonify({"error": "Please provide a movie title as a query parameter."}), 400
    
    recommendations = get_recommendations(movie_title, cosine_sim)
    
    if recommendations.empty:
        return jsonify({"message": "No recommendations found for the given movie."}), 404
    
    # Convert the DataFrame to a list of dictionaries
    recommendations_list = recommendations.to_dict(orient='records')
    
    return jsonify(recommendations_list)

if __name__ == '__main__':
    app.run(debug=True)
