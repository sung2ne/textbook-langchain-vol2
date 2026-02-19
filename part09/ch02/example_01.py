# lambda_handler.py
from mangum import Mangum
from app.main import app

# Lambda 핸들러
handler = Mangum(app, lifespan="off")
