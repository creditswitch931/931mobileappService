
import logging 
import argparse 
from werkzeug.debug import DebuggedApplication

# from appdir import app 
# import appdir.model as m 

from applib.lib.helper import get_config
from applib import app 
from applib import model as m 

# sentry integration 


# to control sentry logging 
cfg = get_config("SENTRY")
if cfg.get("enabled") == '0':
    import sentry_sdk
    from sentry_sdk.integrations.flask import FlaskIntegration
    from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration

    sentry_sdk.init(cfg['url'], 
                    integrations=[FlaskIntegration(), SqlalchemyIntegration()]
                    )

    print("=== SENTRY ENABLED ===")
 

# +-------------------------+-------------------------+
# +-------------------------+-------------------------+


def create_app(): 
    
    cfg = get_config('FLASK')
    app.config.update(
        **cfg
    )
 
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)

    if app.debug:
        app.wsgi_app = DebuggedApplication(app.wsgi_app, evalex=True)

    return app


# +-------------------------+-------------------------+
# +-------------------------+-------------------------+


def main(): 
 
    parser = argparse.ArgumentParser()
    
    parser.add_argument('-s', "--start_server", action="store_true", 
                        help='To start the flask built in sever',
                        default=False)

    parser.add_argument('-c', "--create_db", action="store_true", 
                        help="To create the app db", 
                        default=False)

    parser.add_argument('-d', "--drop_db", action="store_true", 
                        help="To drop the app db tables", 
                        default=False)


    args = parser.parse_args()  

    
    if args.start_server:
        app_ins = create_app()
        app_ins.run()
        

    if args.create_db:
        m.create_tbl()
 

    if args.drop_db:
        m.drop_tbl()



# +-------------------------+-------------------------+
# +-------------------------+-------------------------+


if __name__ == '__main__':
	main()


