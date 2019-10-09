
import logging 
import argparse 
from werkzeug.debug import DebuggedApplication

# from appdir import app 
# import appdir.model as m 

from applib.lib.helper import get_config
from applib import app 

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

	app_ins = create_app()
	app_ins.run()
	# further settings will appear here 



# +-------------------------+-------------------------+
# +-------------------------+-------------------------+

if __name__ == '__main__':
	main()
