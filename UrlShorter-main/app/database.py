import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from app.models.url import URL, Base
from dotenv import load_dotenv
from datetime import datetime, timedelta


HOST = 'localhost'
PORT = '3306'

load_dotenv()

class MySQLDatabase:
    def __init__(self, username, password, host, port, database_name, driver='pymysql'):
        self.username = username
        self.password = password
        self.host = host
        self.port = port
        self.database_name = database_name
        self.driver = driver
    
        self.connection_string = "sqlite:///url_shorter.sqlite3"

        self.engine = create_engine(self.connection_string, echo=True)
        Base.metadata.create_all(self.engine)

        self.Session = sessionmaker(bind=self.engine)

    def add_url(self, short_code: str, original_url: str, expires_at: datetime = None):
        """Добавление новой записи с URL и TTL"""
        if expires_at is None and ttl_hours == 0:
            expires_at = None
        with self.Session() as session:
            try:
                new_url = URL(short_code=short_code, original_url=original_url, expires_at=expires_at)
                session.add(new_url)
                session.commit()
                print(f"URL с коротким кодом {short_code} добавлен с TTL {expires_at} часов.")
            except SQLAlchemyError as e:
                print(f"Ошибка добавления URL: {e}")
                session.rollback()

    def url_exists(self, original_url):
        """Проверка, существует ли URL в базе данных"""
        with self.Session() as session:
            result = session.query(URL).filter_by(original_url=original_url).first()
            return result is not None 

    def get_url_by_short_code(self, short_code):
        """Получение URL по короткому коду"""
        with self.Session() as session:
            result = session.query(URL).filter_by(short_code=short_code).first()
            return result

    def get_short_code_by_url(self, original_url):
        """Получение короткого кода по оригинальному URL"""
        with self.Session() as session:
            result = session.query(URL).filter_by(original_url=original_url).first()
            if result:
                return result.short_code
            return None 

    def update_clicks(self, short_code):
        """Увеличение числа кликов на URL"""
        with self.Session() as session:
            try:
                url = session.query(URL).filter_by(short_code=short_code).first()
                if url:
                    url.clicks += 1
                    session.commit()
                    print(f"Клики для {short_code} увеличены.")
                else:
                    print(f"URL с коротким кодом {short_code} не найден.")
            except SQLAlchemyError as e:
                print(f"Ошибка при обновлении кликов: {e}")
                session.rollback()

    def get_all_urls(self):
        """Получение всех URL"""
        with self.Session() as session:
            result = session.query(URL).all()
            return result

    def delete_url(self, short_code):
        """Удаление URL по короткому коду"""
        with self.Session() as session:
            try:
                url = session.query(URL).filter_by(short_code=short_code).first()
                if url:
                    session.delete(url)
                    session.commit()
                    print(f"URL с коротким кодом {short_code} удален.")
                else:
                    print(f"URL с коротким кодом {short_code} не найден.")
            except SQLAlchemyError as e:
                print(f"Ошибка при удалении URL: {e}")
                session.rollback()

    def close(self):
        """Закрытие соединения с базой данных"""
        self.engine.dispose()

def get_db():
    db = MySQLDatabase(
        username=os.getenv('MYSQL_USER'), 
        password=os.getenv('MYSQL_PASSWORD'), 
        database_name=os.getenv('DB_NAME'),
        host=HOST, 
        port=PORT
    )
    try:
        yield db
    finally:
        db.close()