from flask import Flask, jsonify
import os

app = Flask(__name__)

@app.route('/')
@app.route('/api')
def index():
    return jsonify({
        'status': 'ok',
        'message': 'Flask is working on Vercel',
        'cwd': os.getcwd(),
        'files': os.listdir('.')
    })

@app.route('/api/test')
def test():
    return jsonify({
        'status': 'test ok',
        'python_version': os.sys.version
    })

# Vercelが直接呼び出す関数
def handler(environ, start_response):
    """WSGI handler for Vercel"""
    return app(environ, start_response)
