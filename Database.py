import time
import numpy as np
import datetime
from tkinter import messagebox
from mysql.connector.errors import Error
import mysql.connector


class Database:

    #Kayıtlı Veriler için Fonksiyonlar

    def connect(self):
        try:
            self.db = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="kbots"
            )
            self.cursor = self.db.cursor()

        except mysql.connector.Error as error:
            print("Veri tabanına bağlantı başarısız. {}".format(error))
            if error.errno == 2003:
                messagebox.showinfo(title="Veri Tabanı Bağlantısı", message="Veri tabanına bağlantı başarısız. Lütfen veri tabanını çalıştırınız.")
                exit()

    def insertProduct(self,TileID,ProductTime,ProductImage):
        SQL = 'INSERT INTO urun (KaroID,UretimZaman,UretimGoruntu) VALUES ('+str(TileID)+',"'+str(ProductTime)+'","'+ProductImage+'")'
        
        self.cursor.execute(SQL)
        self.db.commit()
        print(str(self.cursor.rowcount) + " ürün eklendi. id: "+str(self.cursor.lastrowid))
        return self.cursor.lastrowid

    def insertDefect(self,Area,Loc,DefectType,ProductTime):
        SQL = 'INSERT INTO kusur (Alan,Konum,KusurTurID,KusurZaman) VALUES ("'+str(Area)+'","'+str(Loc)+'",'+str(DefectType)+',"'+str(ProductTime)+'")'
        print(SQL)
        self.cursor.execute(SQL)
        self.db.commit()
        print(str(self.cursor.rowcount) + " kusur eklendi.")
        return self.cursor.rowcount
    
    def insertQualityResult(self,TileID,Percentage,ColorTone):
        SQL = 'INSERT INTO kalite_sonuc (UrunID,Yuzde,RenkTon) VALUES ('+str(TileID)+','+str(Percentage)+','+str(ColorTone)+')'
        print(SQL)
        self.cursor.execute(SQL)
        self.db.commit()
        print(str(self.cursor.rowcount) + " kalite yüzdesi eklendi.")
        return self.cursor.rowcount

    