from WEB import create_app
from WEB.config import DevelopmentConfig, ProductionConfig
import os

env = os.getenv("FLASK_ENV")
if env != "development":
    app = create_app(ProductionConfig)
else:
    app = create_app(DevelopmentConfig)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")