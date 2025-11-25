import inquirer
from tabulate import tabulate
import os
import csv
import time
import sys

class Warna:
    BIRU = '\033[94m'      # Warna Biru Terang
    KUNING = '\033[93m'    # Warna Kuning
    HIJAU = '\033[92m'     # Warna Hijau
    MERAH = '\033[91m'     # Warna Merah
    RESET = '\033[0m'      # Reset warna kembali normal

basedir = os.path.dirname(os.path.abspath(__file__))
PASIEN_CSV = os.path.join(basedir, "data", "pasien.csv")
PERMOHONAN_CSV = os.path.join(basedir, "data", "permohonan_kunjungan.csv")

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def header():
    width = 70 
    print("=" * width)
    judul = "SISTEM INFORMASI PIP HOSPITAL - MENU USER"
    print(judul.center(width))
    print("=" * width)

def input_enter():
    """Input Enter dengan warna Kuning"""
    input(f"\n{Warna.KUNING}Tekan Enter untuk kembali ke menu...{Warna.RESET}")

def loading_animasi(teks="Memuat data"):
    """Efek loading sederhana"""
    sys.stdout.write(f"\n{teks}")
    for _ in range(3):
        time.sleep(0.3)
        sys.stdout.write(".")
        sys.stdout.flush()
    print("\n")

#READ DATA PASIEN
def read_data_pasien():
    clear_screen()
    width = 54
    print("=" * width)
    judul = "READ DATA PASIEN PIP HOSPITAL"
    print(judul.center(width))
    print("=" * width)

    if not os.path.exists(PASIEN_CSV):
        print(f"{Warna.MERAH}[ERROR] File tidak ditemukan: {PASIEN_CSV}{Warna.RESET}")
        input_enter()
        return

    data_tabel = []
    headers = [
        f"{Warna.BIRU}No{Warna.RESET}", 
        f"{Warna.BIRU}Nama Pasien{Warna.RESET}", 
        f"{Warna.BIRU}Ruangan{Warna.RESET}", 
        f"{Warna.BIRU}Status{Warna.RESET}"
    ]

    try:
        with open(PASIEN_CSV, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            count = 0
            for row in reader:
                count += 1
                row = {k.strip(): v.strip() for k, v in row.items()}
                
                #Hanya mengambil data umum
                data_tabel.append([
                    count,
                    row.get("nama", "-"),
                    row.get("ruangan", "-"),
                    row.get("status_kunjungan", "-")
                ])
        
        if data_tabel:
            print(tabulate(data_tabel, headers=headers, tablefmt="rounded_grid", stralign="left", numalign="center"))
        else:
            print("Belum ada data pasien.")

    except Exception as e:
        print(f"{Warna.MERAH}[ERROR] Gagal membaca CSV: {e}{Warna.RESET}")
    
    input_enter()

#PERMOHONAN KUNJUNGAN
def form_permohonan():
    clear_screen()
    width = 65 
    print("=" * width)
    judul = "PERMOHONAN KUNJUNGAN PIP HOSPITAL"
    print(judul.center(width))
    print("=" * width)

    pertanyaan = [
        inquirer.Text('nama', message="Nama Penjenguk", validate=lambda _, x: len(x) > 0),
        inquirer.Text('pasien', message="Nama Pasien yang dijenguk", validate=lambda _, x: len(x) > 0),
        inquirer.Text('jam', message="Rencana Jam Besuk (cth: 10.00)", validate=lambda _, x: len(x) > 0),
    ]
    
    jawaban = inquirer.prompt(pertanyaan)
    
    if not jawaban: return 

    try:
        loading_animasi("Mengirim permohonan")
        
        file_exists = os.path.exists(PERMOHONAN_CSV)
        
        with open(PERMOHONAN_CSV, mode='a', newline='', encoding='utf-8') as file:
            fieldnames = ['nama_penjenguk', 'nama_pasien', 'jam_besuk', 'status']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            
            if not file_exists:
                writer.writeheader()
            
            writer.writerow({
                'nama_penjenguk': jawaban['nama'],
                'nama_pasien': jawaban['pasien'],
                'jam_besuk': jawaban['jam'],
                'status': 'Pending' 
            })
            
        print(f"{Warna.HIJAU} SUKSES! Permohonan Anda telah dikirim dengan status 'Menunggu'.{Warna.RESET}")
        print("   Silakan cek status secara berkala.")
        
    except Exception as e:
        print(f"{Warna.MERAH}[ERROR] Gagal menyimpan data: {e}{Warna.RESET}")

    input_enter()

#CEK STATUS KUNJUNGAN
def cek_status():
    clear_screen()
    width = 57
    print("=" * width)
    judul = "CEK STATUS KUNJNGAN PIP HOSPITAL"
    print(judul.center(width))
    print("=" * width)

    cari = inquirer.prompt([inquirer.Text('nama', message="Masukkan Nama Penjenguk")])
    if not cari: return
    nama_dicari = cari['nama'].lower()

    if not os.path.exists(PERMOHONAN_CSV):
        print(f"\n{Warna.KUNING}[INFO] Belum ada data permohonan sama sekali.{Warna.RESET}")
        input_enter()
        return

    loading_animasi("Mencari data")
    
    data_tabel = []
    #Header Tabel Hasil Pencarian
    headers = [
        f"{Warna.BIRU}Nama Penjenguk{Warna.RESET}", 
        f"{Warna.BIRU}Pasien{Warna.RESET}", 
        f"{Warna.BIRU}Jam{Warna.RESET}", 
        f"{Warna.BIRU}Status{Warna.RESET}"
    ]

    try:
        with open(PERMOHONAN_CSV, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                row = {k.strip(): v.strip() for k, v in row.items()}
                
                if nama_dicari in row['nama_penjenguk'].lower():
                    status_raw = row['status']
                    if "Disetujui" in status_raw:
                        status_fmt = f"{Warna.HIJAU}{status_raw}{Warna.RESET}"
                    elif "Pending" in status_raw:
                        status_fmt = f"{Warna.KUNING}{status_raw}{Warna.RESET}"
                    else:
                        status_fmt = f"{Warna.MERAH}{status_raw}{Warna.RESET}"

                    data_tabel.append([
                        row['nama_penjenguk'],
                        row['nama_pasien'],
                        row['jam_besuk'],
                        status_fmt
                    ])
        
        if data_tabel:
            print(tabulate(data_tabel, headers=headers, tablefmt="rounded_grid", stralign="left"))
        else:
            print(f"{Warna.MERAH} Data atas nama '{cari['nama']}' tidak ditemukan.{Warna.RESET}")

    except Exception as e:
        print(f"{Warna.MERAH}[ERROR] Terjadi kesalahan: {e}{Warna.RESET}")

    input_enter()

#MENU UTAMA
def main_menu():
    while True:
        clear_screen()
        width = 45
        print("=" * width)
        judul = "MENU USER"
        print(judul.center(width))
        print("=" * width)
        
        pertanyaan = [
            inquirer.List('menu',
                message="Silakan pilih menu (Gunakan panah ⬆⬇)",
                choices=[
                    '1. Lihat Data Pasien Rawat Inap',
                    '2. Ajukan Permohonan Kunjungan',
                    '3. Cek Status Kunjungan',
                    '4. Logout / Keluar',
                ],
                carousel=True 
            ),
        ]
        
        jawaban = inquirer.prompt(pertanyaan)
        
        if not jawaban: break 

        pilihan = jawaban['menu']

        if '1.' in pilihan:
            read_data_pasien()
        elif '2.' in pilihan:
            form_permohonan()
        elif '3.' in pilihan:
            cek_status()
        elif '4.' in pilihan:
            konfirmasi = inquirer.confirm("Yakin ingin keluar?", default=True)
            if konfirmasi:
                print(f"\n{Warna.BIRU}Terima kasih telah menggunakan layanan PIP Hospital.{Warna.RESET}")
                break

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print(f"\n{Warna.KUNING}Program dihentikan.{Warna.RESET}")