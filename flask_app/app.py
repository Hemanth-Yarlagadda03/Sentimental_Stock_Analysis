from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os
from datetime import datetime
from process_sentiment import process_sentiment  # Import your processing function

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'flask_app/uploads'
app.config['VISUALIZATIONS_FOLDER'] = 'flask_app/visualizations'

# Route to upload HTML file
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)
            results = process_sentiment(file_path)  # Process sentiment and generate plots
            return redirect(url_for('display_results'))
    return render_template('upload.html')

# Route to display results
@app.route('/results')
def display_results():
    plots = []
    for filename in os.listdir(app.config['VISUALIZATIONS_FOLDER']):
        if filename.endswith('.png'):
            plots.append(filename)
    return render_template('results.html', plots=plots)

# Route to serve images
@app.route('/visualizations/<filename>')
def serve_image(filename):
    return send_from_directory(app.config['VISUALIZATIONS_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
