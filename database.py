from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
import os
from dotenv import load_dotenv

load_dotenv()

class Database:
    def __init__(self):
        self.client = None
        self.db = None

    def connect(self):
        """MongoDB 연결 설정"""
        try:
            mongodb_uri = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/')
            db_name = os.getenv('DB_NAME', 'prometheus_db')

            self.client = MongoClient(
                mongodb_uri,
                serverSelectionTimeoutMS=5000,
                connectTimeoutMS=10000
            )

            # 연결 테스트
            self.client.admin.command('ping')
            self.db = self.client[db_name]

            print(f"✓ MongoDB connected successfully to {db_name}")
            return True

        except (ConnectionFailure, ServerSelectionTimeoutError) as e:
            print(f"✗ MongoDB connection failed: {str(e)}")
            return False
        except Exception as e:
            print(f"✗ Unexpected error connecting to MongoDB: {str(e)}")
            return False

    def get_db(self):
        """데이터베이스 인스턴스 반환"""
        return self.db

    def close(self):
        """MongoDB 연결 종료"""
        if self.client:
            self.client.close()
            print("✓ MongoDB connection closed")

    def is_connected(self):
        """연결 상태 확인"""
        try:
            if self.client:
                self.client.admin.command('ping')
                return True
        except:
            pass
        return False

# 전역 데이터베이스 인스턴스
db_instance = Database()