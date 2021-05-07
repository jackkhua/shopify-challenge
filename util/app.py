from flask import Flask, render_template, request, url_for,redirect
from db.image_db import mock_db
import os
from werkzeug.utils import secure_filename

app = Flask(__name__, template_folder='template')
db_connection = mock_db()


@app.route("/")
def index():
    returned_urls = db_connection.home_page()
    return render_template('index.html', value = returned_urls)

# The reason for this being a POST method is that since I didn't implement security layer, this avoid users
# access images by adding url parameters
@app.route("/image", methods = ['POST'])
def display():
    image_id = int(request.form['image_id'])
    current_image = db_connection.data_from_id(image_id)
    related_id = db_connection.search(current_image['category'])
    related_id.remove(image_id)
    related_images = db_connection.data_from_id(related_id)
    data_set = (current_image, related_images)
    return render_template('display_image.html', value=data_set)
        
# For the same reason it would be great to have a security layer since it's an image repository for users, so having it
# in POST avoid URL parameters access
@app.route("/search", methods = ['POST'])
def search():
    key = request.form['key']
    key = key.split(',')
    returned_urls = db_connection.search(key)
    related_images = db_connection.data_from_id(returned_urls)

    return render_template('index.html', value =related_images)

@app.route("/upload", methods = ['POST'])
def upload():
    title = request.form.get('title', False)
    tags = request.form.get('tags', False)
    if title and tags:
        new_image = request.files['upload_file']
        new_image.save(os.path.join(os.getcwd(), 'static', secure_filename(new_image.filename)))
        print(secure_filename(new_image.filename))
        db_connection.upload_new_image(title, tags, secure_filename(new_image.filename))
        return redirect(url_for('index'))
    else:
        return 'please enter title and tags'

if __name__ == "__main__":
  app.run()