import os


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-change-me")
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "mysql+pymysql://root:1234@localhost/tienda_contabilidad",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
