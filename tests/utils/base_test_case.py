import os
from flask_testing import TestCase
from app import create_app, db


class BaseTestCase(TestCase):
    def create_app(self):
        app = create_app("config.TestingConfig")
        app.config.from_mapping(
            SQLALCHEMY_DATABASE_URI="sqlite:///"
            + os.path.join(app.instance_path, "test.db?check_same_thread=False"),
        )

        try:
            os.makedirs(app.instance_path)
        except OSError:
            pass

        return app

    def setUp(self):
        """
        Will be called before every test
        """
        db.create_all()

    def tearDown(self):
        """
        Will be called after every test
        """
        db.drop_all()
