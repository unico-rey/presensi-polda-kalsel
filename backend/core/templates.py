from fastapi.templating import Jinja2Templates

# Memberitahu FastAPI di mana lokasi folder HTML berada
templates = Jinja2Templates(directory="frontend/templates")