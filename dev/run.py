import os
from pooldcode import app

if __name__ == '__main__':
    host = os.environ.get('HOST') or '0.0.0.0'
    port = int(os.environ.get('PORT', 5000))
    app.run(host=host, port=port)
