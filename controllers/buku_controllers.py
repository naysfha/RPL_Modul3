# Nayla Syafha_F5212510020
from tkinter import messagebox
from models.buku_model import BukuModel
from views.buku_view import BukuView

class BukuController:
    def __init__(self):
        self.model = BukuModel()
        self.view = BukuView()

        self.view.btn_simpan.configure(command=self.simpan_data)

        self.muat_data_tabel()

    def muat_data_tabel(self):
        for item in self.view.tabel.get_children():
            self.view.tabel.delete(item)

        data_buku = self.model.get_all_buku()

        for buku in data_buku:
            self.view.tabel.insert ("", "end", values=(buku["id_buku"], buku["judul"], buku["penulis"], buku["tahun_terbit"]))

    def simpan_data(self):
        judul = self.view.entry_judul.get()
        penulis = self.view.entry_penulis.get()
        tahun = self.view.entry_tahun.get()

        if not judul or not penulis or not tahun:
            messagebox.showwarning("Peringatan", "Semua data harus diisi!")
            return

        berhasil = self.model.create_buku(judul, penulis, tahun)
        
        if berhasil:
            messagebox.showwarning("Sukses", "Data buku berhasil disimpan!")
            self.view.entry_judul.delete(0, 'end')
            self.view.entry_penulis.delete(0, 'end')
            self.view.entry_tahun.delete(0, 'end')
            # Muat ulang tabel agar data terbaru muncul
            self.muat_data_tabel()
        else:
            messagebox.showwarning("Error", "Terjadi keselahan saat menyimpan data.")
            
    def run(self):
        self.view.mainloop()

