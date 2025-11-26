import os
import csv
import pandas as pd
import inquirer
from tabulate import tabulate
from colorama import Fore, Style, init

init(autoreset=True)

dataDIR = 'data'
dfPasien = f'{dataDIR}/pasien.csv'
dfInfoUmum = f'{dataDIR}/info_umum.csv'
dfInfoDokter = f'{dataDIR}/info_dokter.csv'

def baca_pasien():
    try:
        df = pd.read_csv(dfPasien, dtype=str)
        return df if not df.empty else df
    except FileNotFoundError:
        print(Fore.RED + f"[ERROR] File '{dfPasien}' tidak ditemukan." + Style.RESET_ALL)
        return None

def baca_csv(path_file):
    if not os.path.exists(path_file):
        print(Fore.RED + f"[ERROR] File '{path_file}' tidak ditemukan." + Style.RESET_ALL)
        return []
    with open(path_file, "r", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def clear():
    os.system("cls || clear")

def tampilkan_tabel(data):
    if not data:
        print(Fore.RED + "Tidak ada data untuk ditampilkan." + Style.RESET_ALL)
        return
    headers = list(data[0].keys())
    rows = [list(row.values()) for row in data]
    headers_warna = [Fore.CYAN + h + Style.RESET_ALL for h in headers]
    print(tabulate(rows, headers=headers_warna, tablefmt="rounded_outline"))
    print()

def menu_utama():
    while True:
        clear()
        pilihan = inquirer.list_input(
            "Pilih menu:",
            choices=[
                "1. Lihat Jadwal Besuk",
                "2. Lihat Jadwal Dokter",
                "3. Lihat Data Pasien",
                "Keluar"
                ]
            )
        if pilihan.startswith("1"):
            clear()
            print("\n=== JADWAL BESUK ===")  
            data = baca_csv(dfInfoUmum)
            tampilkan_tabel(data)
            input(Fore.YELLOW + "Tekan ENTER untuk melanjutkan..." + Style.RESET_ALL)
        elif pilihan.startswith("2"):
            clear()
            print("\n=== JADWAL DOKTER ===") 
            data = baca_csv(dfInfoDokter)
            tampilkan_tabel(data)
            input(Fore.YELLOW + "Tekan ENTER untuk melanjutkan..." + Style.RESET_ALL)
        elif pilihan.startswith("3"):
            clear()
            print("\n=== DATA PASIEN ===") 
            df = baca_pasien()
            if df is None or df.empty:
                print(Fore.RED + "Data pasien kosong atau tidak ditemukan." + Style.RESET_ALL)
            else:
                print(tabulate(df, headers="keys", tablefmt="rounded_outline", showindex=False))
            input(Fore.YELLOW + "Tekan ENTER untuk melanjutkan..." + Style.RESET_ALL)
        else:
            print(Fore.GREEN + "Terima kasih!" + Style.RESET_ALL)
            break

if __name__ == "__main__":
    menu_utama()
