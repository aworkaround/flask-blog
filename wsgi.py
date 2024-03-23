import os
from main import app

DEBUG_MODE = os.getenv('DEBUG_MODE') == 'True'

if __name__ == '__main__':
    app.run(debug=DEBUG_MODE)