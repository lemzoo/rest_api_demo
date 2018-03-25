from flask_script import Manager, Server, Shell

from blog.main import bootstrap_app
from blog.model import BaseModel

app = bootstrap_app()
manager = Manager(app)


manager.add_command("runserver", Server())
manager.add_command("shell", Shell())


@manager.command
def init_db():
    engine = manager.app.engine
    print('*************************************')
    print('*** Initialized Data Model schema ***')
    print('### *** ###')
    BaseModel.metadata.drop_all(engine)
    BaseModel.metadata.create_all(engine)
    print('*** Data Model schema is initialized successfully ***')
    print('*****************************************************')


if __name__ == "__main__":
    manager.run()
