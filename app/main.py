from flask import Flask, jsonify, request, redirect
from app.utils import is_valid_url, generate_short_code
from app.models import save_url_mapping, get_url_mapping, increment_click, short_code_exists

app = Flask(__name__)

@app.route('/')
def health_check():
    return jsonify({
        "status": "healthy",
        "service": "URL Shortener API"
    })

@app.route('/api/health')
def api_health():
    return jsonify({
        "status": "ok",
        "message": "URL Shortener API is running"
    })

@app.route('/api/shorten', methods=['POST'])
def shorten_url():
    data = request.get_json()
    url = data.get('url')
    if not url or not is_valid_url(url):
        return jsonify({"error": "Invalid URL"}), 400

    # Generate unique short code
    for _ in range(5):
        short_code = generate_short_code()
        if not short_code_exists(short_code):
            break
    else:
        return jsonify({"error": "Could not generate unique short code"}), 500

    save_url_mapping(short_code, url)
    return jsonify({
        "short_code": short_code,
        "short_url": request.host_url + short_code
    }), 201

@app.route('/<short_code>')
def redirect_short_url(short_code):
    mapping = get_url_mapping(short_code)
    if not mapping:
        return jsonify({"error": "Short code not found"}), 404
    increment_click(short_code)
    return redirect(mapping["original_url"])

@app.route('/api/stats/<short_code>')
def stats(short_code):
    mapping = get_url_mapping(short_code)
    if not mapping:
        return jsonify({"error": "Short code not found"}), 404
    return jsonify({
        "original_url": mapping["original_url"],
        "clicks": mapping["clicks"],
        "created_at": mapping["created_at"]
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)