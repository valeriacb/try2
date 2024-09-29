import os
import logging
from flask import Flask, render_template, request, jsonify
from main import read_file, segmentation, exp_def, kword_finder

app = Flask(__name__)

# Directory path
folder_path = '/Users/valeriacabac/Desktop/try2/new2'

# Setup logging
logging.basicConfig(level=logging.INFO)

def process_cvs(folder_path, user_input):
    """Processes all CVs in the folder and returns keyword match info."""
    cv_match = {}

    # Strip whitespace from the user's input keywords
    user_input = [word.strip() for word in user_input]

    # Use os.scandir for better performance when iterating over directory
    with os.scandir(folder_path) as entries:
        for entry in entries:
            if entry.is_file() and not entry.name.startswith('.'):  # Skip hidden/system files
                file_path = entry.path
                logging.info(f'Processing file: {file_path}')

                try:
                    # Read and clean up the CV content
                    content = read_file(file_path)
                    content = content.replace("•", "").replace("Abilități", "Competențe")

                    # Segment and define experience (assuming these return something useful)
                    segmentation(content)
                    exp_def(content)

                    # Find keyword matches
                    tokens, keywords, keyword_match = kword_finder(content, user_input)

                    keyword_count = len(keyword_match)
                    total_keywords = len(keywords)

                    if keyword_count > 0:
                        # Calculate percentage of matched keywords
                        percentage_matched = (keyword_count / total_keywords) * 100 if total_keywords > 0 else 0
                        cv_match[entry.name] = {
                            'keyword_count': keyword_count,
                            'percentage_matched': percentage_matched,
                            'matched_keywords': keyword_match
                        }
                        
                except Exception as e:
                    logging.error(f"Error processing file {file_path}: {e}")

    return cv_match

@app.route('/')
def index():
    return render_template('index.html')  # Renders the HTML file

@app.route('/process_cvs', methods=['POST'])
def process_cvs_route():
    data = request.get_json()
    keywords = data.get('keywords')

    # Validate input
    if not keywords or not isinstance(keywords, str):
        return jsonify({"error": "Invalid or no keywords provided"}), 400

    # Split keywords by comma and remove leading/trailing whitespace
    user_input = [keyword.strip() for keyword in keywords.split(',')]

    # Process CVs, passing the folder path and user input
    cv_match = process_cvs(folder_path, user_input)

    if not cv_match:
        return jsonify({"message": "No matching CVs found"}), 404

    return jsonify(cv_match)

if __name__ == '__main__':
    app.run(debug=True)
