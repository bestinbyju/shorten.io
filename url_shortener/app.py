from flask import Flask, request, jsonify, render_template
import string, random

app = Flask(__name__)

url_map = {}

def generate_code(length=5):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/process", methods=["POST"])
def process():
    data = request.get_json()          
    long_url = data.get("message", "") 

    if not long_url:
        return jsonify({"reply": "Please enter a URL!"})

    
    code = generate_code()
    while code in url_map:  
        code = generate_code()

    
    url_map[code] = long_url

   
    short_url = f"http://localhost:5000/{code}"
    return jsonify({"reply": f"Short URL: {short_url}"})

@app.route("/<code>")
def redirect_url(code):
    if code in url_map:
        return f"""<h3>Redirecting to <a href="{url_map[code]}">{url_map[code]}</a></h3>"""
    return "URL not found", 404

if __name__ == "__main__":
    app.run(debug=True)