from flask import Flask, render_template, request, url_for
from db.image_db import mock_db

app = Flask(__name__, template_folder='template')
db_connection = mock_db()


@app.route("/")
def index():
    returned_urls = db_connection.home_page()
    return render_template('index.html', value = returned_urls)


@app.route("/image", methods = ['POST'])
def display():
    image_id = int(request.form['image_id'])
    current_image = db_connection.data_from_id(image_id)
    related_id = db_connection.search(current_image['category'])
    related_id.remove(image_id)
    related_images = db_connection.data_from_id(related_id)
    data_set = (current_image, related_images)
    return render_template('display_image.html', value=data_set)
        



@app.route("/search", methods = ['POST'])
def search():
    key = request.form['key']
    key = key.split(',')
    returned_urls = db_connection.search(key)
    related_images = db_connection.data_from_id(returned_urls)

    return render_template('index.html', value =related_images)


if __name__ == "__main__":
  app.run()