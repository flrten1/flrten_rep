from flask import Flask, request, redirect, render_template, jsonify
import string
import random
import sqlite3

app = Flask(__name__)

def create_table():
    conn = sqlite3.connect('links.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS links
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  original_url TEXT NOT NULL,
                  short_url TEXT NOT NULL,
                  click_count INTEGER DEFAULT 0)''')
    conn.commit()
    conn.close()

def generate_short_link():
    characters = string.ascii_letters + string.digits
    short_link = ''.join(random.choice(characters) for i in range(6))
    return short_link

def add_link_to_database(original_url, short_url):
    conn = sqlite3.connect('links.db')
    c = conn.cursor()
    c.execute("INSERT INTO links (original_url, short_url) VALUES (?, ?)", (original_url, short_url))
    conn.commit()
    conn.close()

def get_original_url(short_url):
    conn = sqlite3.connect('links.db')
    c = conn.cursor()
    c.execute("SELECT original_url FROM links WHERE short_url=?", (short_url,))
    original_url = c.fetchone()
    conn.close()
    return original_url[0] if original_url else None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/shorten', methods=['POST'])
def shorten_url():
    original_url = request.json.get('url')
    if not original_url:
        return jsonify({'error': 'Invalid URL'}), 400

    short_url = generate_short_link()
    add_link_to_database(original_url, short_url)
    return jsonify({'short_url': short_url}), 200

@app.route('/statistics', methods=['GET', 'POST'])
def statistics():
    if request.method == 'POST':
        short_url = request.form.get('short_url')
        if short_url:
            statistics_data = get_statistics_data(short_url)
            return render_template('statistics.html', statistics_data=statistics_data)
        else:
            return render_template('statistics.html')
    else:
        return render_template('statistics.html')

    
@app.route('/get_statistics', methods=['POST'])
def get_statistics():
    short_url = request.form.get('short_url')
    if not short_url:
        return render_template('statistics.html', statistics_data={}, error_message=None)

    conn = sqlite3.connect('links.db')
    c = conn.cursor()
    c.execute("SELECT click_count FROM links WHERE short_url=?", (short_url,))
    row = c.fetchone()
    conn.close()

    if row:
        click_count = row[0]
        return render_template('statistics.html', statistics_data={short_url: click_count}, error_message=None)
    else:
        return render_template('statistics.html', statistics_data={}, error_message="Short URL not found")


    
@app.route('/<short_url>')
def redirect_to_original(short_url):
    original_url = get_original_url(short_url)
    if original_url:
        increment_click_count(short_url)
        return redirect(original_url)
    else:
        return render_template('not_found.html')

def increment_click_count(short_url):
    conn = sqlite3.connect('links.db')
    c = conn.cursor()
    c.execute("UPDATE links SET click_count = click_count + 1 WHERE short_url=?", (short_url,))
    conn.commit()
    conn.close()    

if __name__ == '__main__':
    create_table()
    app.run(debug=True, port=80, host='0.0.0.0')
