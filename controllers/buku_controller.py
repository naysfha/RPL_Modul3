# NaylaSyafha_F5212510020
import tkinter.messagebox as messagebox
from models.buku_model import BukuModel
from views.buku_view import BukuView

class BukuController:
    def __init__(self, user_role="anggota"):
        self.user_role = user_role
        self.model = BukuModel()
        self.view = BukuView()

        self.view.title(f"Sistem Manajemen Perpustakaan - Mode: {self.user_role.upper()}")

        self.view.btn_simpan.configure(command=self.simpan_data)
        self.view.btn_hapus.configure(command=self.hapus_data)
        self.view.btn_update.configure(command=self.update_data)

        if self.user_role != "admin":
            self.view.btn_simpan.configure(state="disabled", text="Akses Terkunci (Khusus Admin)")
            self.view.btn_hapus.configure(state="disabled")
            self.view.btn_update.configure(state="disabled")
            self.view.entry_judul.configure(state="disabled")
            self.view.entry_penulis.configure(state="disabled")
            self.view.entry_tahun.configure(state="disabled")

        self.muat_data_tabel()

    def muat_data_tabel(self):
        for item in self.view.tabel.get_children():
            self.view.tabel.delete(item)

        data_buku = self.model.get_all_buku()

        for buku in data_buku:
            self.view.tabel.insert("", "end", values=(buku['id_buku'], buku['judul'], buku['penulis'], buku['tahun_terbit']))

    def simpan_data(self):
        if self.user_role != "admin":
            messagebox.showwarning("Akses Ditolak", "Anda tidak memiliki izin untuk menambah data!")
            return

        judul = self.view.entry_judul.get()
        penulis = self.view.entry_penulis.get()
        tahun = self.view.entry_tahun.get()

        if not judul or not penulis or not tahun:
            messagebox.showwarning("Peringatan", "Semua kolom form harus diisi!")
            return

        berhasil = self.model.create_buku(judul, penulis, tahun)

        if berhasil:
            messagebox.showinfo("Sukses", "Data buku berhasil disimpan!")
            self.view.entry_judul.delete(0, 'end')
            self.view.entry_penulis.delete(0, 'end')
            self.view.entry_tahun.delete(0, 'end')
            self.muat_data_tabel()
        else:
            messagebox.showerror("Error", "Terjadi kesalahan saat menyimpan data.")

    def hapus_data(self):
        if self.user_role != "admin":
            messagebox.showwarning("Akses Ditolak", "Anda tidak memiliki izin untuk menghapus data!")
            return

        selected_item = self.view.tabel.focus()
        if not selected_item:
            messagebox.showwarning("Peringatan", "Pilih data buku yang ingin dihapus!")
            return

        item_data = self.view.tabel.item(selected_item)
        id_buku = item_data['values'][0]

        konfirmasi = messagebox.askyesno("Konfirmasi", "Apakah Anda yakin ingin menghapus data ini?")
        if konfirmasi:
            berhasil = self.model.delete_buku(id_buku)
            if berhasil:
                messagebox.showinfo("Sukses", "Data buku berhasil dihapus!")
                self.muat_data_tabel()
            else:
                messagebox.showerror("Error", "Terjadi kesalahan saat menghapus data.")

    def update_data(self):
        if self.user_role != "admin":
            messagebox.showwarning("Akses Ditolak", "Anda tidak memiliki izin untuk memperbarui data!")
            return

        selected_item = self.view.tabel.focus()
        if not selected_item:
            messagebox.showwarning("Peringatan", "Pilih data buku yang ingin diperbarui!")
            return

        item_data = self.view.tabel.item(selected_item)
        id_buku = item_data['values'][0]

        judul = self.view.entry_judul.get()
        penulis = self.view.entry_penulis.get()
        tahun = self.view.entry_tahun.get()

        if not judul or not penulis or not tahun:
            messagebox.showwarning("Peringatan", "Semua kolom form harus diisi untuk memperbarui data!")
            return

        berhasil = self.model.update_buku(id_buku, judul, penulis, tahun)
        if berhasil:
            messagebox.showinfo("Sukses", "Data buku berhasil diperbarui!")
            self.view.entry_judul.delete(0, 'end')
            self.view.entry_penulis.delete(0, 'end')
            self.view.entry_tahun.delete(0, 'end')
            self.muat_data_tabel()
        else:
            messagebox.showerror("Error", "Terjadi kesalahan saat memperbarui data.")

    def run(self):
        self.view.mainloop()