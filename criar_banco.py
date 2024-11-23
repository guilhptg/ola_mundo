from ola_mundo import database, app
from ola_mundo.models import Usuario, Foto, Contato, Categoria, Tag


with app.app_context():
    database.create_all()