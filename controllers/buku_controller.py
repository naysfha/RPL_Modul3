# controllers/buku_controller.py
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
        self.view.tabel.bind("<<TreeviewSelect>>", self.isi_form_dari_baris) # Menambahkan ini

        if self.user_role != "admin":
            self.view.btn_simpan.configure(state="disabled", text="Akses Terkunci (Khusus Admin)")
            self.view.btn_hapus.configure(state="disabled")
            self.view.btn_update.configure(state="disabled")
            self.view.entry_judul.configure(state="disabled")
            self.view.entry_penulis.configure(state="disabled")
            self.view.entry_tahun.configure(state="disabled")

        # Menambahkan ini
        self.view.btn_logout.configure(command=self.logout)
        # ----
        
        self.muat_data_tabel()
        
    # Menambahkan ini
    def _kosongkan_form(self):
        self.view.entry_judul.delete(0, 'end')
        self.view.entry_penulis.delete(0, 'end')
        self.view.entry_tahun.delete(0, 'end')
    # ---
    
    def muat_data_tabel(self):
        for item in self.view.tabel.get_children():
            self.view.tabel.delete(item)

        for buku in self.model.get_all_buku():
            self.view.tabel.insert("", "end", values=(
                buku['id_buku'], buku['judul'], buku['penulis'], buku['tahun_terbit']
            ))
    # Menambahkan ini_
    def isi_form_dari_baris(self, event):
        if self.user_role != "admin":
            return

        selected = self.view.tabel.focus()
        if not selected:
            return
        _, judul, penulis, tahun = self.view.tabel.item(selected)['values']

        self._kosongkan_form()
        self.view.entry_judul.insert(0, judul)
        self.view.entry_penulis.insert(0, penulis)
        self.view.entry_tahun.insert(0, tahun)
    # ---
    
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

        if self.model.create_buku(judul, penulis, tahun):
            messagebox.showinfo("Sukses", "Data buku berhasil disimpan!")
            self._kosongkan_form()
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

        id_buku = self.view.tabel.item(selected_item)['values'][0]

        if messagebox.askyesno("Konfirmasi", "Apakah Anda yakin ingin menghapus data ini?"):
            if self.model.delete_buku(id_buku):
                messagebox.showinfo("Sukses", "Data buku berhasil dihapus!")
                self._kosongkan_form()
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

        id_buku = self.view.tabel.item(selected_item)['values'][0]

        judul = self.view.entry_judul.get()
        penulis = self.view.entry_penulis.get()
        tahun = self.view.entry_tahun.get()

        if not judul or not penulis or not tahun:
            messagebox.showwarning("Peringatan", "Semua kolom form harus diisi untuk memperbarui data!")
            return

        if self.model.update_buku(id_buku, judul, penulis, tahun):
            messagebox.showinfo("Sukses", "Data buku berhasil diperbarui!")
            self._kosongkan_form()
            self.muat_data_tabel()
        else:
            messagebox.showerror("Error", "Terjadi kesalahan saat memperbarui data.")

    # Menambahkan ini
    def logout(self):
        if messagebox.askyesno("Logout", "Apakah Anda yakin ingin logout?"):
            self.view.destroy()
            from controllers.auth_controller import AuthController  
            AuthController().run()
    # --- 
    
    def run(self):
        self.view.mainloop()