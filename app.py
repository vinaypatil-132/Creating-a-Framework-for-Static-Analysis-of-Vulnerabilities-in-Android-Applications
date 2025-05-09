from flask import Flask, request, render_template, send_from_directory, redirect, url_for
import os
import json
from analyzer import analyze_apk, save_json, create_pdf

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
RESULT_FOLDER = 'results'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['RESULT_FOLDER'] = RESULT_FOLDER

# Create directories if they don't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

@app.route('/')
def landing_page():
    return render_template('landing.html')  # Serve the landing page

@app.route('/upload', methods=['GET', 'POST'])
def upload_apk():
    if request.method == 'POST':
        if 'apkfile' not in request.files:
            return "No file part", 400
        
        apk_file = request.files['apkfile']
        if apk_file.filename == '':
            return "No selected file", 400
        
        if apk_file:
            apk_path = os.path.join(app.config['UPLOAD_FOLDER'], apk_file.filename)
            apk_file.save(apk_path)

            # Step 1: Analyze APK
            analysis_result = analyze_apk(apk_path)

            # Step 2: Save JSON
            json_output_path = os.path.join(app.config['RESULT_FOLDER'], 'analysis.json')
            save_json(analysis_result, json_output_path)

            # Step 3: Create PDF
            pdf_output_path = os.path.join(app.config['RESULT_FOLDER'], 'analysis_report.pdf')
            create_pdf(analysis_result, pdf_output_path)

            return render_template('upload.html', json_file='analysis.json', pdf_file='analysis_report.pdf')

    # If GET request, just show the upload form
    return render_template('upload.html')

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(app.config['RESULT_FOLDER'], filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)