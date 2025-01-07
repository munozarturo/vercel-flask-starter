import sys
from pathlib import Path

root_dir = Path(__file__).parent
sys.path.append(str(root_dir))

from api.index import app

if __name__ == "__main__":
    app.run()
