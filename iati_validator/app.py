"""The app module, containing the app factory function."""
from os import environ

from flask import Flask, render_template

from . import commands, public
from .extensions import cache, csrf_protect, db, debug_toolbar, migrate, webpack


def create_app(config_object='iati_validator.settings'):
    """Application factory.

    As explained here:
    http://flask.pocoo.org/docs/patterns/appfactories/.

    :param config_object: The configuration object to use.
    """
    app = Flask(__name__.split('.')[0])
    app.config.from_object(config_object)
    register_extensions(app)
    register_blueprints(app)
    register_errorhandlers(app)
    register_shellcontext(app)
    register_commands(app)
    register_template_filters(app)
    return app


def register_extensions(app):
    """Register Flask extensions."""
    cache.init_app(app)
    db.init_app(app)
    csrf_protect.init_app(app)
    debug_toolbar.init_app(app)
    migrate.init_app(app, db)
    webpack.init_app(app)


def register_blueprints(app):
    """Register Flask blueprints."""
    app.register_blueprint(public.views.blueprint)


def register_template_filters(app):
    """Register template filters."""
    def commify(value):
        """Add number group commas to a number."""
        return format(int(value), ',d')

    def pluralise(word, count, singular=None, plural=None):
        """Pluralise a word."""
        if count == 1:
            return singular if singular else word
        return plural if plural else word + 's'

    @app.context_processor
    def inject_git_sha():  # pylint: disable=unused-variable
        """Add git_sha to template variables."""
        return dict(git_sha=environ.get('HEROKU_SLUG_COMMIT'))

    app.jinja_env.filters['commify'] = commify
    app.jinja_env.filters['pluralise'] = pluralise


def register_errorhandlers(app):
    """Register error handlers."""
    def render_error(error):
        """Render error template."""
        # If a HTTPException, pull the `code` attribute; default to 500
        error_code = getattr(error, 'code', 500)
        return render_template('{0}.html'.format(error_code)), error_code
    for errcode in [401, 404, 500]:
        app.errorhandler(errcode)(render_error)


def register_shellcontext(app):
    """Register shell context objects."""
    def shell_context():
        """Shell context objects."""
        return {
            'db': db,
        }

    app.shell_context_processor(shell_context)


def register_commands(app):
    """Register Click commands."""
    app.cli.add_command(commands.lint)
