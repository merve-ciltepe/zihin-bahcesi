import sqlite3
from PyQt5.QtWidgets import QWidget, QTableWidgetItem, QMessageBox
from aliskanlikguncel import Ui_Form  # Qt Designer'dan gelen arayüz

class AliskanlikEkrani(QWidget):
    def __init__(self, kullanici_id):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.kullanici_id = kullanici_id

        # Butonlara işlev bağla
        self.ui.btn_kaydet.clicked.connect(self.aliskanlik_kaydet)
        self.ui.btn_listele.clicked.connect(self.aliskanlik_listele)

    def aliskanlik_kaydet(self):
        baslik = self.ui.lineEdit_baslik.text().strip()
        aciklama = self.ui.textEdit_aciklama.toPlainText().strip()
        hedef_sayi = self.ui.spinBox_hedef.value()
        tarih = self.ui.dateEdit_tarih.text()

        if not baslik:
            QMessageBox.warning(self, "Uyarı", "Başlık boş olamaz.")
            return

        try:
            conn = sqlite3.connect("zihin_bahcesi.db")
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO Aliskanliklar (kullanici_id, baslik, aciklama, hedef_sayi, tamamlandi_mi, tarih)
                VALUES (?, ?, ?, ?, 0, ?)
            """, (self.kullanici_id, baslik, aciklama, hedef_sayi, tarih))
            conn.commit()
            conn.close()

            QMessageBox.information(self, "Başarılı", "Alışkanlık kaydedildi.")
            self.ui.lineEdit_baslik.clear()
            self.ui.textEdit_aciklama.clear()
            self.ui.spinBox_hedef.setValue(0)
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Kayıt başarısız: {str(e)}")

    def aliskanlik_listele(self):
        try:
            conn = sqlite3.connect("zihin_bahcesi.db")
            cursor = conn.cursor()
            cursor.execute("""
                SELECT baslik, aciklama, hedef_sayi, tamamlandi_mi, tarih
                FROM Aliskanliklar
                WHERE kullanici_id = ?
            """, (self.kullanici_id,))
            veriler = cursor.fetchall()
            conn.close()

            self.ui.tabloAliskanliklar.setRowCount(0)
            for satir, veri_satiri in enumerate(veriler):
                self.ui.tabloAliskanliklar.insertRow(satir)
                for sutun, veri in enumerate(veri_satiri):
                    if sutun == 3:
                        veri = "Evet" if veri else "Hayır"
                    self.ui.tabloAliskanliklar.setItem(satir, sutun, QTableWidgetItem(str(veri)))
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Listeleme hatası: {str(e)}")
