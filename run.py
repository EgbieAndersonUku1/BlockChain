from flask_script import Manager, Server
from flask_cors import CORS


from app import create_app


manager = Manager(create_app)
manager.add_command("runserver", Server(use_debugger=True, use_reloader=True))
CORS(create_app())


if __name__ == "__main__":
    manager.run()