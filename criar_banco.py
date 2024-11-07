from ola_mundo import database, app
from ola_mundo.models import Usuario, Foto


with app.app_context():
    database.create_all()