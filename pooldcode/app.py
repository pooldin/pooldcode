import os
import boto
from boto.s3.bucket import Bucket
from flask import Flask
from pooldcode import index


class App(Flask):

    def __init__(self, *args, **kw):
        super(App, self).__init__(*args, **kw)
        self.configure()

    def configure(self):
        self.url_map.strict_slashes = False
        settings = os.environ.get('APPCODE_CONFIG')
        settings = settings or 'pooldcode.settings.dev'
        self.config.from_object('pooldcode.settings.base')
        self.config.from_object(settings)
        self.from_env('AUTH_USERNAME')
        self.from_env('AUTH_PASSWORD')
        self.configure_s3()
        self.configure_blueprints()

    def from_env(self, *keys):
        for key in keys:
            if key:
                envvar = 'CODE_%s' % key
                if envvar in os.environ and os.environ[envvar]:
                    self.config[key] = os.environ[envvar]

    def configure_s3(self):
        self.s3 = boto.connect_s3()
        self.bucket = self.config.get('S3_BUCKET')
        self.bucket = Bucket(self.s3, name=self.bucket)
        self.teardown_appcontext(self.teardown_s3)

    def configure_blueprints(self):
        self.register_blueprint(index.plan)

    def teardown_s3(self, response):
        self.s3.close()
