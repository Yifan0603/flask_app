#db: employeedb
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

class FlaskAppWrapper:
    db = None
    def __init__(self, app, configs):
        self.app = app
        self.configs(**configs)

    def configs(self, **configs):
        for config, value in configs.items():
            self.app.config[config] = value
        #self.app.url_map.strict_slashes = False #mọi route đều đc tạo 
        self.init_db()
        
    def init_db(self):    
        self.db = SQLAlchemy(self.app) 
        migrate = Migrate(self.app, self.db)
 
    def add_endpoint(self, endpoint=None, endpoint_name=None, handler=None, methods=['GET'], *args, **kwargs):
        self.app.add_url_rule(endpoint, endpoint_name, handler, methods=methods, *args, **kwargs)
 
    def run(self, **kwargs):
        self.app.run(**kwargs)
