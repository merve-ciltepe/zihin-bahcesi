import sys
import sqlite3
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QMessageBox, QWidget, QTableWidgetItem
)

from girisekrani import Ui_MainWindow as Ui_GirisEkrani
from anaekran import Ui_MainWindow as Ui_AnaEkran
from kayitguncel import Ui_MainWindow as Ui_Kayit
from aliskanlikguncel import Ui_MainWindow as Ui_Aliskanlik
from duygugunlugugüncel import Ui_MainWindow as Ui_DuyguGunlugu





class GirisEkrani(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_GirisEkrani()
        self.ui.setupUi(self)

        self.ui.pushButton_girisyap.clicked.connect(self.giris_kontrol)
        self.ui.pushButton_kayitol.clicked.connect(self.kayit_ekranini_ac)
 
    def giris_kontrol(self):
        eposta = self.ui.lineEdit_email.text().strip()
        sifre = self.ui.lineEdit_sifre.text().strip()

        if not eposta or not sifre:
            QMessageBox.warning(self, "Uyarı", "Lütfen e-posta ve şifre giriniz.")
            return

        try:
            conn = sqlite3.connect("zihin_bahcesi.db")
            cursor = conn.cursor()
            cursor.execute("SELECT kullanici_id, sifre FROM Kullanicilar WHERE email=?", (eposta,))
            sonuc = cursor.fetchone()
            conn.close()

            if sonuc and sonuc[1] == sifre:
                self.ana_pencere = AnaPencere(kullanici_id=sonuc[0])
                self.ana_pencere.show() 
                self.close()
            else:
                QMessageBox.warning(self, "Hata", "E-posta veya şifre hatalı.")
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Veritabanı hatası: {str(e)}")

    def kayit_ekranini_ac(self):
        self.kayit_ekrani = KayitEkrani()
        self.kayit_ekrani.show()

 
class KayitEkrani(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Kayit()
        self.ui.setupUi(self)

        self.ui.pushButton.clicked.connect(self.kayit_ol)

    def kayit_ol(self):
        ad = self.ui.lineEdit_ad.text().strip()
        soyad = self.ui.lineEdit_soyad.text().strip()
        eposta = self.ui.lineEdit_email.text().strip()
        sifre = self.ui.lineEdit_sifre.text().strip()

        if not ad or not soyad or not eposta or not sifre:
            QMessageBox.warning(self, "Eksik Bilgi", "Lütfen tüm alanları doldurunuz.")
            return

        try:
            conn = sqlite3.connect("zihin_bahcesi.db")
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Kullanicilar WHERE email=?", (eposta,))
            if cursor.fetchone():
                QMessageBox.warning(self, "Hata", "Bu e-posta adresi zaten kayıtlı.")
                conn.close()
                return

            cursor.execute("""
                INSERT INTO Kullanicilar (ad, soyad, email, sifre)
                VALUES (?, ?, ?, ?)
            """, (ad, soyad, eposta, sifre))
            conn.commit()
            conn.close()

            QMessageBox.information(self, "Başarılı", "Kayıt başarıyla tamamlandı.")
            self.close()
        except Exception as e:
            QMessageBox.critical(self, "Veritabanı Hatası", str(e))



class AnaPencere(QMainWindow):
    def __init__(self, kullanici_id):
        super().__init__()
        self.ui = Ui_AnaEkran()
        self.ui.setupUi(self)

        self.kullanici_id = kullanici_id
        self.setWindowTitle("Zihin Bahçesi - Ana Sayfa")

        self.ui.pushButton_cikis.clicked.connect(self.close)
        self.ui.pushButton_aliskanlik.clicked.connect(self.aliskanliklari_ac)
        self.ui.pushButton_duygugunluk.clicked.connect(self.duygu_gunlugunu_ac)

    def aliskanliklari_ac(self):
        self.aliskanlik_pencere = AliskanlikPenceresi(self.kullanici_id)
        self.aliskanlik_pencere.show()

    def duygu_gunlugunu_ac(self):
        self.duygu_pencere = DuyguGunluguPenceresi(self.kullanici_id)
        self.duygu_pencere.show()



class AliskanlikPenceresi(QMainWindow):
    def __init__(self, kullanici_id):
        super().__init__()
        self.ui = Ui_Aliskanlik()
        self.ui.setupUi(self)

        self.kullanici_id = kullanici_id
        self.setWindowTitle("Zihin Bahçesi - Alışkanlıklarım")

        self.ui.pushButton_kaydet.clicked.connect(self.aliskanlik_kaydet)
        self.verileri_yukle()

    def aliskanlik_kaydet(self):
        baslik = self.ui.lineEdit_aliskanlik.text().strip()
        tarih = self.ui.dateEdit_tarih.date().toString("yyyy-MM-dd")
        durum_text = self.ui.comboBox.currentText()
        tamamlandi_mi = 1 if durum_text == "Tamamlandı" else 0

        if not baslik:
            QMessageBox.warning(self, "Uyarı", "Lütfen alışkanlık adını girin.")
            return

        try:
            conn = sqlite3.connect("zihin_bahcesi.db")
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO Aliskanliklar (kullanici_id, baslik, tarih, tamamlandi_mi)
                VALUES (?, ?, ?, ?)
            """, (self.kullanici_id, baslik, tarih, tamamlandi_mi))
            conn.commit()
            conn.close()

            QMessageBox.information(self, "Başarılı", "Alışkanlık kaydedildi.")
            self.verileri_yukle()
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Veri kaydedilemedi: {str(e)}")

    def verileri_yukle(self):
        try:
            conn = sqlite3.connect("zihin_bahcesi.db")
            cursor = conn.cursor()
            cursor.execute("""
                SELECT baslik, tarih, tamamlandi_mi
                FROM Aliskanliklar
                WHERE kullanici_id=?
            """, (self.kullanici_id,))
            veriler = cursor.fetchall()
            conn.close()

            self.ui.tableWidget_aliskanlik.setRowCount(len(veriler))
            self.ui.tableWidget_aliskanlik.setColumnCount(3)
            self.ui.tableWidget_aliskanlik.setHorizontalHeaderLabels(["Alışkanlık", "Tarih", "Durum"])

            for satir, veri in enumerate(veriler):
                baslik, tarih, tamamlandi_mi = veri
                durum_yazi = "Tamamlandı" if tamamlandi_mi == 1 else "Tamamlanmadı"
                self.ui.tableWidget_aliskanlik.setItem(satir, 0, QTableWidgetItem(baslik))
                self.ui.tableWidget_aliskanlik.setItem(satir, 1, QTableWidgetItem(tarih))
                self.ui.tableWidget_aliskanlik.setItem(satir, 2, QTableWidgetItem(durum_yazi))
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Veri yüklenemedi: {str(e)}")



class DuyguGunluguPenceresi(QMainWindow):
    def __init__(self, kullanici_id):
        super().__init__()
        self.ui = Ui_DuyguGunlugu()
        self.ui.setupUi(self)

        self.kullanici_id = kullanici_id
        self.setWindowTitle("Zihin Bahçesi - Duygu Günlüğü")

        self.ui.pushButtonkaydetDuygu.clicked.connect(self.duygu_kaydet)
        self.verileri_yukle()

    def duygu_kaydet(self):
        tarih = self.ui.dateEdit_tarihDuygu.date().toString("yyyy-MM-dd")
        duygu = self.ui.comboBox_duygu.currentText()
        notlar = self.ui.textEdit_notlar.toPlainText().strip()

        if not notlar:
            QMessageBox.warning(self, "Uyarı", "Lütfen bir not giriniz.")
            return

        try:
            conn = sqlite3.connect("zihin_bahcesi.db")
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO DuyguGunlugu (kullanici_id, tarih, duygu, notlar)
                VALUES (?, ?, ?, ?)
            """, (self.kullanici_id, tarih, duygu, notlar))
            conn.commit()
            conn.close()

            QMessageBox.information(self, "Başarılı", "Duygu günlüğü kaydedildi.")
            self.verileri_yukle()
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Veri kaydedilemedi: {str(e)}")

    def verileri_yukle(self):
        try:
            conn = sqlite3.connect("zihin_bahcesi.db")
            cursor = conn.cursor()
            cursor.execute("""
                SELECT tarih, duygu, notlar
                FROM DuyguGunlugu
                WHERE kullanici_id=?
            """, (self.kullanici_id,))
            veriler = cursor.fetchall()
            conn.close()

            self.ui.tableWidget_duygular.setRowCount(len(veriler))
            self.ui.tableWidget_duygular.setColumnCount(3)
            self.ui.tableWidget_duygular.setHorizontalHeaderLabels(["Tarih", "Duygu", "Notlar"])

            for satir, veri in enumerate(veriler):
                for sutun, bilgi in enumerate(veri):
                    self.ui.tableWidget_duygular.setItem(satir, sutun, QTableWidgetItem(str(bilgi)))
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Veriler yüklenemedi: {str(e)}")



if __name__ == "__main__":
    app = QApplication(sys.argv)
    pencere = GirisEkrani()
    pencere.show()
    sys.exit(app.exec_()) 
