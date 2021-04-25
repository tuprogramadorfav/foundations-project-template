from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from great_project import app, db

migrate = Migrate(app, db)
manager = Manager(app)

if __name__ == "__main__":
    manager.run()