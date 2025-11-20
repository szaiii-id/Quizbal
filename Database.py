import sqlite3
import json
import os

class DatabaseManager:
    def __init__(self, db_name="quiz_data.db"):
        self.db_name = db_name
        self.init_db()

    def init_db(self):
        """Membuat tabel jika belum ada."""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS custom_questions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT NOT NULL,
                question TEXT NOT NULL,
                question_image TEXT,
                options TEXT NOT NULL,
                answer TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()

    def add_question(self, category, question, image_path, options_list, answer):
        """Menambahkan soal baru ke database."""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        options_json = json.dumps(options_list)
        cursor.execute('''
            INSERT INTO custom_questions (category, question, question_image, options, answer)
            VALUES (?, ?, ?, ?, ?)
        ''', (category.lower(), question, image_path, options_json, answer))
        conn.commit()
        conn.close()

    def update_question(self, question_id, category, question, image_path, options_list, answer):
        """Update soal yang sudah ada."""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        options_json = json.dumps(options_list)
        cursor.execute('''
            UPDATE custom_questions 
            SET category=?, question=?, question_image=?, options=?, answer=?
            WHERE id=?
        ''', (category.lower(), question, image_path, options_json, answer, question_id))
        conn.commit()
        conn.close()

    def delete_question(self, question_id):
        """Hapus soal dari database."""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM custom_questions WHERE id=?', (question_id,))
        conn.commit()
        conn.close()

    def get_all_questions(self, category=None):
        """Mengambil semua soal custom."""
        if not os.path.exists(self.db_name): 
            return []
            
        conn = sqlite3.connect(self.db_name)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        if category:
            cursor.execute('SELECT * FROM custom_questions WHERE category = ?', (category.lower(),))
        else:
            cursor.execute('SELECT * FROM custom_questions')
            
        rows = cursor.fetchall()
        results = []
        for row in rows:
            results.append({
                "id": row['id'],
                "category": row['category'],
                "question": row['question'],
                "question_image": row['question_image'],
                "options": json.loads(row['options']),
                "answer": row['answer']
            })
        conn.close()
        return results

    def get_custom_questions(self, category):
        """Mengambil soal untuk gameplay."""
        questions = self.get_all_questions(category)
        for q in questions:
            q.pop('id', None)
        return questions

    def get_all_categories(self, default_categories):
        """Mengambil daftar semua kategori."""
        categories = set(default_categories)
        
        if os.path.exists(self.db_name):
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute("SELECT DISTINCT category FROM custom_questions")
            rows = cursor.fetchall()
            for row in rows:
                categories.add(row[0])
            conn.close()
        
        return list(categories)