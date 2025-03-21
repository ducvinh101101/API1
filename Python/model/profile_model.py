from flask import jsonify
from sqlalchemy import create_engine, MetaData, Table, select
from sqlalchemy.exc import SQLAlchemyError


class ProfileModel():
    def __init__(self, engine=None):
        try:
            if engine:
                self.engine = engine  # Nếu có engine được truyền vào, sử dụng nó
            else:
                server = 'DESKTOP-PIULBJ0\\SQLEXPRESS'
                database = 'BookMoth'
                driver = 'ODBC Driver 17 for SQL Server'
                conn_str = f'mssql+pyodbc://@{server}/{database}?trusted_connection=yes&driver={driver}'
                self.engine = create_engine(conn_str)

            self.metadata = MetaData()
            self.Profiles = Table("Profiles", self.metadata, autoload_with=self.engine)
            self.Works = Table("Works", self.metadata, autoload_with=self.engine)

            print('✅ Connected to database successfully!')
        except Exception as e:
            print(f'❌ Connection failed: {e}')

    def getProfileID(self, id):
        try:
            with self.engine.connect() as conn:
                stmt = select(self.Profiles.c.profile_id, self.Profiles.c.first_name, self.Profiles.c.last_name, self.Profiles.c.avatar).where(self.Profiles.c.profile_id == id)
                result = conn.execute(stmt).fetchone()
                if result:
                    profile_id, first_name, last_name, avatar = result
                    profile_ = {
                        'profile_id': profile_id,
                        'first_name': first_name,
                        'last_name': last_name,
                        'avatar': avatar
                    }

                    return jsonify({"message": "✅ Lấy thành công!", "data": profile_}), 200
                else:
                    return jsonify({"message": "❌ Không tìm thấy hồ sơ!"}), 404
        except Exception as e:
            return jsonify({"error": f"❌ Query failed: {e}"}), 500

    def getAvatarPath(self, id):
        """Lấy đường dẫn file avatar từ database theo profile_id"""
        try:
            with self.engine.connect() as conn:
                stmt = select(self.Profiles.c.avatar).where(self.Profiles.c.profile_id == id)
                result = conn.execute(stmt).fetchone()

                if result and result.avatar:
                    return result.avatar  # Trả về đường dẫn ảnh từ DB
                else:
                    return None  # Không tìm thấy avatar
        except Exception as e:
            print(f"❌ Query failed: {e}")
            return None


    def getUrlAvatar(self, id):
        """Lấy đường dẫn link avata theo id profile"""
        return f"http://127.0.0.1:5000/avatar_profile/{id}" if id else None

    def getBooks(self):
        """Lấy danh sách các sách và trả về dữ liệu kèm cover_url đầy đủ"""
        try:
            with self.engine.connect() as conn:
                stmt = select(self.Works.c.work_id, self.Works.c.title, self.Works.c.cover_url)
                result = conn.execute(stmt).fetchall()

                if result:
                    books = []
                    for row in result:
                        work_id, title, cover_url = row
                        full_cover_url = f"http://127.0.0.1:5000/covers/{cover_url}" if cover_url else None
                        books.append({
                            "work_id": work_id,
                            "title": title,
                            "cover_url": full_cover_url
                        })

                    return jsonify({"data": books}), 200
                else:
                    return jsonify({"message": "❌ Không tìm thấy sách!"}), 404
        except Exception as e:
            return jsonify({"error": f"❌ Query failed: {e}"}), 500

    def getBookId(self, id):
        """Lấy sách có id và trả về dữ liệu kèm cover_url đầy đủ"""
        try:
            with self.engine.connect() as conn:
                stmt = select(self.Works.c.work_id, self.Works.c.title, self.Works.c.cover_url).where(
                    self.Works.c.work_id == id)
                result = conn.execute(stmt).fetchone()

                if result:
                    work_id, title, cover_url = result
                    full_cover_url = f"http://127.0.0.1:5000/covers/{cover_url}" if cover_url else None

                    book = {
                        "work_id": work_id,
                        "title": title,
                        "cover_url": full_cover_url
                    }

                    return jsonify({"data": book}), 200  # Trả về object, không phải danh sách
                else:
                    return jsonify({"message": "❌ Không tìm thấy sách!"}), 404
        except Exception as e:
            return jsonify({"error": f"❌ Query failed: {e}"}), 500




