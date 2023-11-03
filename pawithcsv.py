from prettytable import PrettyTable
import csv
import os
from pwinput import pwinput

DATA_PRODUK = "data_produk.csv"
USER = "user.csv"
ADMIN_FILE = "admin.csv"
# Inisialisasi data produk
products = []
# Definisikan dictionary database pengguna

# Fungsi untuk login Customer
def load_users(file_name):
    users = []
    if os.path.exists(file_name):
        with open(file_name, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                users.append(row)
    return users

def sign_in_user(username, password, users):
    for user in users:
        if user['username'] == username and user['password'] == password:
            return True
    return False

def login_as_admin():
    while True:
        admins = load_users(ADMIN_FILE)
        username = input("Enter admin username: ")
        password = pwinput("Enter admin password: ")
        if sign_in_user(username, password, admins):
            print("Admin login successful!")
            return menu_admin()
        else:
            print("Admin login failed. Please try again.")


def login_as_customer():
    while True:
        global username
        customers = load_users(USER)
        username = input("Enter customer username: ")
        password = pwinput("Enter customer password: ")
        if sign_in_user(username, password, customers):
            print("Customer login successful!")
            return menu_user()
        else:
            print("Customer login failed. Please try again.")

def register_as_admin():
    username = input("Masukan Username: ")

    if len(username) > 20:
        print("Username tidak boleh lebih dari 20")
    else:
        username_available = True
        with open(ADMIN_FILE, mode='r') as file:
            reader = csv.DictReader(file)
            for data in reader:
                if username == data['username']:
                    print("Username tidak tersedia")
                    username_available = False
                    break

        if username_available:
            password = pwinput("Masukan Password: ")
            with open(ADMIN_FILE, mode='a', newline='') as file:
                fieldnames = ["username", "password"]
                writer = csv.DictWriter(file, fieldnames=fieldnames)

                if file.tell() == 0:
                    writer.writeheader()

                writer.writerow({"username": username, "password": password})
                print("Sign Up berhasil")

        menu_awal_admin


def register_as_customer():
    saldo = 0
    username = input("Enter new customer username: ")
    if len(username) > 20:
        print("Username tidak boleh lebih dari 20")
    else:
        username_available = True
        with open(USER, mode='r') as file:
            reader = csv.DictReader(file)
            for data in reader:
                if username == data['username']:
                    print("Username tidak tersedia")
                    username_available = False
                    break
        if username_available:
            password = pwinput("Enter new customer password: ")
            with open(USER, mode='a', newline='') as file:
                fieldnames = ["username", "password", "saldo"]
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                if file.tell() == 0:
                    writer.writeheader()
                writer.writerow({"username": username, "password": password, "saldo": saldo})
        
        menu_awal_user

def load_products_from_file():
    if os.path.exists(DATA_PRODUK):
        with open(DATA_PRODUK, mode='r') as file:
            reader = csv.DictReader(file)
            products.extend(reader)

def save_products_to_file():
    fieldnames = ["Code", "jenis kendaraan", "merek kendaraan", "harga rental"]
    with open(DATA_PRODUK, mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        if file.tell() == 0:
            writer.writeheader()
        writer.writerows(products)

# ... (rest of your code remains the same) ...

def tambah_product():
    code_products = input("Nama code: ")
    jeniskendaraan_products = input("Nama Jenis Kendaraan:")
    merekkendaraan_products = input("Nama Merek Kendaraan:")
    hargarental_products = float(input("Harga Rental Produk: "))

    product = {
        "Code": code_products,
        "jenis kendaraan": jeniskendaraan_products,
        "merek kendaraan": merekkendaraan_products,
        "harga rental": hargarental_products
    }

    products.append(product)
    save_products_to_file()

# Fungsi untuk menampilkan produk menggunakan PrettyTable
def table_products():
    with open(DATA_PRODUK, mode='r') as file:
        reader = csv.DictReader(file)
        table = PrettyTable()
        table.field_names = ["Code", "jenis kendaraan", "merek kendaraan", "harga rental"]
        for row in reader:
            table.add_row([row["Code"], row["jenis kendaraan"], row["merek kendaraan"], row["harga rental"]])
        print(table)

# Fungsi untuk membaca dan menampilkan semua produk
def melihat_products():
    table_products()
    if not products:
        print("Tidak ada produk yang tersedia.")
        return

# Fungsi untuk memperbarui produk berdasarkan nama
def perbarui_product():
    table_products()
    code = input("Kode Produk yang akan diperbarui: ")

    updated_products = []
    product_found = False

    with open(DATA_PRODUK, mode='r') as file:
        reader = csv.DictReader(file)
        fieldnames = ["Code", "jenis kendaraan", "merek kendaraan", "harga rental"]

        for product in reader:
            if product['Code'] == code:
                product_found = True
                nama_baru = input("Nama Jenis Kendaraan: ")
                merk_baru = input("Merk baru: ")
                harga_baru = float(input("Harga Baru: "))
                product['jenis kendaraan'] = nama_baru
                product['merek kendaraan'] = merk_baru
                product['harga rental'] = harga_baru

            updated_products.append(product)

    if not product_found:
        print("Produk tidak ditemukan.")
        return

    with open(DATA_PRODUK, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(updated_products)

    print("Produk diperbarui.")

# Fungsi untuk menghapus produk berdasarkan nama
def hapus_product():
    table_products()
    code = input("Kode Produk yang akan dihapus: ")

    updated_products = []
    product_found = False

    with open(DATA_PRODUK, mode='r') as file:
        reader = csv.DictReader(file)
        fieldnames = ["Code", "jenis kendaraan", "merek kendaraan", "harga rental"]

        for product in reader:
            if product['Code'] == code:
                product_found = True
                continue

            updated_products.append(product)

    if not product_found:
        print("Produk tidak ditemukan.")
        return

    with open(DATA_PRODUK, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(updated_products)

    print("Produk dihapus.")

# Menghitung biaya rental
def hitung_biaya_rental(data, kendaraan, hari_sewa):
    for row in data:
        if row[0] == kendaraan:
            harga_rental = float(row[1])
            biaya_total = harga_rental * hari_sewa
            return biaya_total
    return None

# Fungsi untuk menampilkan saldo E-Money
def display_balance():
    with open(USER, mode='r') as file:
        reader = csv.DictReader(file)
        for data in reader:
            if data["username"] == username:
                print(f"Saldo E-Money Anda: Rp. {data['saldo']} ")

# Fungsi untuk menambahkan saldo E-Money
def top_up_balance():
    display_balance()
    choice = input("Apakah Anda ingin top up saldo E-Money? (ya/tidak): ")
    if choice.lower() == "ya":
        amount = float(input("Masukkan jumlah yang ingin Anda top up: Rp. "))
        updated = False
        with open(USER, mode='r') as file:
            users = list(csv.DictReader(file))
            for user in users:
                if user["username"] == username:
                    user["saldo"] = str(float(user["saldo"]) + amount)  # Convert 'saldo' to float
                    updated = True

        if updated:
            with open(USER, mode='w', newline='') as file:
                fieldnames = ["username", "password", "saldo"]
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(users)
            print("Top up berhasil")
        else:
            print("Gagal menambahkan saldo. Pengguna tidak ditemukan.")

def transaksi():
    keranjang = []
    total_harga = 0

    while True:
        print("======================================================\n")
        table_products()
        kode = input("Masukkan Code produk yang ingin dirental (ketik 0 untuk selesai): ")

        if kode == '0':
            break

        found_product = False
        with open(DATA_PRODUK, mode='r') as file:
            reader = csv.DictReader(file)
            for item in reader:
                if item['Code'] == kode:
                    harga = float(item['harga rental'])
                    total_harga += harga
                    found_product = True
                    break

        if not found_product:
            print("Produk tidak ditemukan.")
            continue

        display_balance()  # Menampilkan saldo awal

        if total_harga > 0:
            with open(USER, mode='r') as file:
                users = list(csv.DictReader(file))
                for user in users:
                    if user["username"] == username:
                        if float(user["saldo"]) >= total_harga:
                            user["saldo"] = str(float(user["saldo"]) - total_harga)

                            with open(USER, mode='w', newline='') as file:
                                fieldnames = ["username", "password", "saldo"]
                                writer = csv.DictWriter(file, fieldnames=fieldnames)
                                writer.writeheader()
                                writer.writerows(users)  # Tulis kembali semua data pengguna
                                print("Transaksi berhasil. Saldo Anda telah dikurangi.")
                        else:
                            print("Saldo tidak mencukupi. Transaksi dibatalkan.")
                            break
            print("Transaksi selesai.")
        else:
            print("Tidak ada transaksi yang dilakukan.")

    print("\n======================================================")
    print(f"Total Harga : Rp {total_harga}")
    print("======================================================")

def menu_admin():
    while True:
        print("\nMenu Admin:")
        print("1. Tambah Produk")
        print("2. Lihat Produk")
        print("3. Perbarui Produk")
        print("4. Hapus Produk")
        print("5. Keluar")
        choice = input("Pilih operasi (1/2/3/4/5): ")

        if choice == "1":
            tambah_product()
        elif choice == "2":
            melihat_products()
        elif choice == "3":
            perbarui_product()
        elif choice == "4":
            hapus_product()
        elif choice == "5":
            print("Terima kasih! Sampai jumpa.")
            break
        else:
            print("Pilihan tidak valid. Silakan coba lagi.")

def menu_awal_admin():
    while True:
        print("\n Admin:")
        print("1. Sign In")
        print("2. Sign Up")
        print("3. Keluar")
        pilihan = input("Pilih operasi (1/2): ")

        if  pilihan == "1":
            login_as_admin()
        elif pilihan == "2":
            register_as_admin()
        elif pilihan == "3":
            break
        else:
            print("Pilihan tidak valid. Silakan coba lagi.")

def menu_awal_user():
    while True:
                print("\n login Customer:")
                print("1. Sign In")
                print("2. sign Up")
                print("3. Keluar")
                pilihan = input("Pilih operasi (1/2/3): ")

                if  pilihan == "1":
                    login_as_customer()
                elif pilihan == "2":
                    register_as_customer()
                elif pilihan == "3":
                    break
                else:
                    print("Pilihan tidak valid. Silakan coba lagi.")

def menu_user():
    while True:
                    print("1. tampilkan saldo")
                    print("2. top up saldo")  
                    print("3. Sewa")  
                    print("4. Keluar")
                    pilihan = input("Pilih operasi (1/2/3/4): ")

                    if pilihan == "1":
                        display_balance()
                    elif pilihan == "2":
                        top_up_balance()
                    elif pilihan == "3":
                        transaksi()
                    elif pilihan == "4":
                        break

if __name__ == "_main_":
    load_products_from_file()


while True:
    try:
        print("="*100)
        print("Selamat datang di toko ")
        print("="*100)
        print("1. Admin")
        print("2. Customer")
        print("3. Keluar")
        peran = input("Pilih peran Anda (Admin/Customer): ")
        print("="*100)

        if peran == "1":
            menu_awal_admin()
                
        elif peran == "2":
            menu_awal_user()

        elif peran == "3":
            print("Terima kasih! Sampai jumpa.")
            break
        else:
            print("Pilihan tidak valid. Silakan coba lagi.")
    except KeyboardInterrupt:
        print("\n\nINVALID\n\n")