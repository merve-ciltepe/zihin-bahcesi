import sqlite3

def veritabani_olustur():
    conn = sqlite3.connect("zihin_bahcesi.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Kullanicilar (
        kullanici_id INTEGER PRIMARY KEY AUTOINCREMENT,
        ad TEXT NOT NULL,
        soyad TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        sifre TEXT NOT NULL
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Aliskanliklar (
        aliskanlik_id INTEGER PRIMARY KEY AUTOINCREMENT,
        kullanici_id INTEGER NOT NULL,
        baslik TEXT NOT NULL,
        aciklama TEXT,
        hedef_sayi INTEGER DEFAULT 0,
        tamamlandi_mi BOOLEAN DEFAULT 0,
        tarih DATE,
        FOREIGN KEY (kullanici_id) REFERENCES Kullanicilar(kullanici_id) ON DELETE CASCADE ON UPDATE CASCADE
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS DuyguGunlugu (
        gunluk_id INTEGER PRIMARY KEY AUTOINCREMENT,
        kullanici_id INTEGER NOT NULL,
        tarih DATE NOT NULL,
        duygu TEXT NOT NULL,
        notlar TEXT,
        FOREIGN KEY (kullanici_id) REFERENCES Kullanicilar(kullanici_id) ON DELETE CASCADE ON UPDATE CASCADE
    );
    """)

    conn.commit()
    conn.close()
    print("Veritabanı ve tablolar oluşturuldu.")

if __name__ == "__main__":
    veritabani_olustur()
