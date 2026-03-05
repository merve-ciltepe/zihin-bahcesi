import sqlite3

def baglanti_olustur():
    try:
        conn = sqlite3.connect("zihin_bahcesi.db")
        print("Veritabanına bağlantı başarılı.")
        return conn
    except sqlite3.Error as e:
        print(f"Veritabanı bağlantı hatası: {e}")
        return None

if __name__ == "__main__":
    baglanti_olustur()
