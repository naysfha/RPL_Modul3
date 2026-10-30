import tkinter.messagebox as messagebox
from models.anggota_model import AnggotaModel
from views.anggota_view import AnggotaView

class AnggotaController:
    def __init__(self):
        self.model = AnggotaModel()
        self.view = AnggotaView()

        self.view.btn_simpan.configure(command=self.simpan_data)
        self.view.btn_hapus.configure(command=self.hapus_data)
        self.view.btn_update.configure(command=self.update_data)
        self.view.tabel.bind("<<TreeviewSelect>>", self.isi_form_dari_baris)

        self.muat_data_tabel()

    def _kosongkan_form(self):
        self.view.entry_nama.delete(0, 'end')
        self.view.entry_alamat.delete(0, 'end')

    def muat_data_tabel(self):
        for item in self.view.tabel.get_children():
            self.view.tabel.delete(item)
        for a in self.model.get_all_anggota():
            self.view.tabel.insert("", "end", values=(a['id_anggota'], a['nama'], a['alamat']))

    def isi_form_dari_baris(self, event):
        selected = self.view.tabel.focus()
        if not selected:
            return
        _, nama, alamat = self.view.tabel.item(selected)['values']
        self._kosongkan_form()
        self.view.entry_nama.insert(0, nama)
        self.view.entry_alamat.insert(0, alamat)

    def simpan_data(self):
        nama = self.view.entry_nama.get()
        alamat = self.view.entry_alamat.get()
        if not nama or not alamat:
            messagebox.showwarning("Peringatan", "Semua kolom form harus diisi!")
            return
        if self.model.create_anggota(nama, alamat):
            messagebox.showinfo("Sukses", "Data anggota berhasil disimpan!")
            self._kosongkan_form()
            self.muat_data_tabel()
        else:
            messagebox.showerror("Error", "Terjadi kesalahan saat menyimpan data.")

    def hapus_data(self):
        selected = self.view.tabel.focus()
        if not selected:
            messagebox.showwarning("Peringatan", "Pilih data anggota yang ingin dihapus!")
            return
        id_anggota = self.view.tabel.item(selected)['values'][0]
        if messagebox.askyesno("Konfirmasi", "Apakah Anda yakin ingin menghapus data ini?"):
            if self.model.delete_anggota(id_anggota):
                messagebox.showinfo("Sukses", "Data anggota berhasil dihapus!")
                self._kosongkan_form()
                self.muat_data_tabel()
            else:
                messagebox.showerror("Error", "Terjadi kesalahan saat menghapus data.")

    def update_data(self):
        selected = self.view.tabel.focus()
        if not selected:
            messagebox.showwarning("Peringatan", "Pilih data anggota yang ingin diperbarui!")
            return
        id_anggota = self.view.tabel.item(selected)['values'][0]
        nama = self.view.entry_nama.get()
        alamat = self.view.entry_alamat.get()
        if not nama or not alamat:
            messagebox.showwarning("Peringatan", "Semua kolom form harus diisi untuk memperbarui data!")
            return
        if self.model.update_anggota(id_anggota, nama, alamat):
            messagebox.showinfo("Sukses", "Data anggota berhasil diperbarui!")
            self._kosongkan_form()
            self.muat_data_tabel()
        else:
            messagebox.showerror("Error", "Terjadi kesalahan saat memperbarui data.")

    def run(self):
        self.view.mainloop()
        
        