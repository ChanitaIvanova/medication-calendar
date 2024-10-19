from flask import Flask, send_from_directory
import os

app = Flask(__name__)
docs_directory = os.path.join(os.getcwd(), '_build', 'html')  # Adjust the path if necessary

@app.route('/docs/<path:filename>')
def serve_docs(filename):
    return send_from_directory(docs_directory, filename)

@app.route('/docs/')
def serve_docs_index():
    return send_from_directory(docs_directory, 'index.html')

if __name__ == '__main__':
    app.run(port=7000)