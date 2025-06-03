import sys
from os.path import abspath, dirname

# Adiciona o diretório ao path do Python
sys.path.append(dirname(abspath(__file__)))

from .modules.app import app

if __name__ == '__main__':
    app.run(debug=True)