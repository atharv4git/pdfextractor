from flask import Flask, request, jsonify
import camelot
import requests
import os

app = Flask(__name__)

DOWNLOAD_FOLDER = 'downloads'
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)


@app.route('/upload', methods=['POST'])
def upload_file():
    # Check if the request contains JSON data
    if request.is_json:
        json_data = request.get_json()
        pdf_url = json_data.get('file')

        if pdf_url:
            try:
                # Download the PDF from the provided URL
                pdf_response = requests.get(pdf_url)
                if pdf_response.status_code == 200:
                    # Save the downloaded PDF
                    pdf_path = os.path.join(app.config['DOWNLOAD_FOLDER'], 'downloaded_pdf.pdf')
                    with open(pdf_path, 'wb') as pdf_file:
                        pdf_file.write(pdf_response.content)

                    # Use Camelot to extract tables from the downloaded PDF
                    tables = camelot.read_pdf(pdf_path, pages='all')
                    # Convert tables to a list of JSON objects
                    tables_json = [table.df.to_json(orient='split') for table in tables]

                    return jsonify({'tables': tables_json})

                else:
                    return jsonify({'error': 'Failed to download the PDF from the URL'}), 500

            except Exception as e:
                return jsonify({'error': f'Error extracting tables: {str(e)}'}), 500

        else:
            return jsonify({'error': 'Invalid JSON data: missing "file" field'}), 400

    else:
        return jsonify({'error': 'Invalid JSON request'}), 400


if __name__ == '__main__':
    app.run(debug=True)
