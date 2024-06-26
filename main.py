from typing import List, Optional
from decimal import Decimal
from typing import Literal
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests

app = FastAPI(
    title="Government",
    description="API untuk mengelola data pemerintahan",
    docs_url="/",  # Ubah docs_url menjadi "/"
)

# chema model untuk data pajak objek wisata
class Pajak(BaseModel):
    id_pajak: str
    id_wisata: str
    nama_objek:  str
    status_kepemilikan: Literal['Pemerintah', 'Swasta', 'Campuran']
    jenis_pajak: str
    tarif_pajak: float
    besar_pajak: int

# Data dummy untuk tabel pajak_objek_wisata
data_pajak =[
    {'id_pajak': 'PJ001', 'status_kepemilikan': 'Swasta', 'jenis_pajak': 'Pajak Pertahanan Nilai (PPN)', 'tarif_pajak': Decimal(0.11), 'besar_pajak': 50000000},
    {'id_pajak': 'PJ002', 'status_kepemilikan': 'Swasta', 'jenis_pajak': 'Pajak Pertahanan Nilai (PPN)', 'tarif_pajak': Decimal(0.11), 'besar_pajak': 100000000},
    {'id_pajak': 'PJ003', 'status_kepemilikan': 'Pemerintah', 'jenis_pajak': 'Pajak Pertahanan Nilai (PPN)', 'tarif_pajak': Decimal(0), 'besar_pajak': 0},
    {'id_pajak': 'PJ004', 'status_kepemilikan': 'Pemerintah', 'jenis_pajak': 'Pajak Pertahanan Nilai (PPN)', 'tarif_pajak': Decimal(0.11), 'besar_pajak': 75000000},
    {'id_pajak': 'PJ005', 'status_kepemilikan': 'Campuran', 'jenis_pajak': 'Pajak Pertahanan Nilai (PPN)', 'tarif_pajak': Decimal(0.11), 'besar_pajak': 65000000}
]

# Endpoint untuk mengakses path root "/"
@app.get("/")
async def read_root():
    return {'example': 'Kamu telah berhasil masuk ke API Government', "Data":"Successful"}

# Endpoint untuk menambahkan data pajak objek wisata
@app.post('/pajak')
async def add_pajakwisata(pajak: Pajak):
    data_pajak.append(pajak.dict())
    return {"message": "Data Pajak Objek Wisata Berhasil Ditambahkan."}

#Endpoint untuk mendapatkan data pajak objek wisata
@app.get('/pajak', response_model=List[Pajak])
async def get_pajak():
    return data_pajak

def get_pajak_index(id_pajak):
    for index, pajak in enumerate(data_pajak):
        if pajak['id_wisata'] == id_pajak:
            return index
    return None

# Endpoint untuk mengmabil detail data pajak sesuai dengan input id_pajak
@app.get("/pajak/{id_pajak}", response_model=Optional[Pajak])
def get_pajak_by_id(id_pajak: str):
    for pajak in data_pajak:
        if pajak['id_wisata'] == id_pajak:
            return Pajak(**pajak)
    return None

# Endpoint untuk memperbarui data pajak objek wisata dengan memasukkan id_pajak saja
@app.put("/pajak/{id_pajak}")
def update_pajak_by_id(id_pajak: str, new_pajak: Pajak):
    index = get_pajak_index(id_pajak)
    if index is not None:
        data_pajak[index] = new_pajak.dict()
        return {"message": "Data wisata berhasil diperbarui."}
    else:
        raise HTTPException(status_code=404, detail="Data Pajak Objek Wisata Tidak Ditemukan.")

# Endpoint untuk menghapus data pajak objek wisaya by id_pajak
@app.delete("/pajak/{id_pajak}")
def delete_pajak_by_id(id_pajak: str):
    index = get_pajak_index(id_pajak)
    if index is not None:
        del data_pajak[index]
        return {"message": "Data Pajak Objek Wisata Berhasil Dihapus."}
    else:
        raise HTTPException(status_code=404, detail="Data Pajak Objek Wisata Tidak Berhasil Dihapus.")

#Fungsi untuk mengambil data objek wisata dari website objek wisata
async def get_objek_wisata_from_web():
    url = "https://pajakobjekwisata.onrender.com/wisata" # URL Endpoint API dari Objek Wisata
    response = requests.get(url)
    if response.status.code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail = "Gagal mengambil data Objek Wisata")
    
# Schema Model untuk data Objek Wisata
class ObjekWisata(BaseModel):
    id_wisata: str
    nama_wisata: str

# Endpoint untuk mendapatkan data objek wisata
@app.get('/wisata', response_model=List[ObjekWisata])
async def get_objekwisata():
    data_objek = get_objek_wisata_from_web()
    return data_objek


# untuk penduduk

class Penduduk (BaseModel):
    nik: int
    nama: str
    provinsi: str
    kota: str
    kecamatan: str
    desa: str

# Data Dummy untuk tabel penduduk
data_penduduk =[
    {'nik':106, 'nama':'Ammar', 'provinsi': 'Banten', 'kota': 'Tangeran Selatan', 'kecamatan': 'Serpong', 'desa': 'Rawa Buntu'},
    {'nik':107, 'nama':'Alif', 'provinsi': 'Sumatera Barat', 'kota': 'Padang', 'kecamatan': 'Kuranji', 'desa': 'Ampang'},
    {'nik':108, 'nama':'Malvin', 'provinsi': 'Jawa Barat', 'kota': 'Bogor', 'kecamatan': 'Bogor Selatan', 'desa': 'Cikaret'},
    {'nik':109, 'nama':'Agung', 'provinsi': 'Jawa Timur', 'kota': 'Jember', 'kecamatan': 'Pakusari', 'desa': 'Kertosari'},
    {'nik':110, 'nama':'Fadlan', 'provinsi': 'Banten', 'kota': 'Serang', 'kecamatan': 'Taktakan', 'desa': 'Kalang Anyar'},
   
    {'nik':116, 'nama':'Ali', 'provinsi': 'Banten', 'kota': 'Tangerang Selatan', 'kecamatan': 'Ciputat Timur', 'desa': 'Bintaro Sektor 3A'},
    {'nik':117, 'nama':'Sandra', 'provinsi': 'Jawa Barat', 'kota': 'Bandung', 'kecamatan': 'Sumur Bandung', 'desa': 'Karanganyar'},
    {'nik':118, 'nama':'Joseph', 'provinsi': 'Jawa Tengah', 'kota': 'Magelang', 'kecamatan': 'Magelang Utara', 'desa': 'Wates'},
    {'nik':119, 'nama':'Lisa', 'provinsi': 'DI Yogyakarta', 'kota': 'Yogyakarta', 'kecamatan': 'Kota Gede', 'desa': 'Purbayan'},
    {'nik':120, 'nama':'Bagus', 'provinsi': 'DKI Jakarta', 'kota': 'Jakarta Barat', 'kecamatan': 'Taman Sari', 'desa': 'Maphar'},
]
# untuk post data kita ke kelompok lain
@app.post('/penduduk')
async def post_penduduk(penduduk: Penduduk):
    data_penduduk.append(penduduk.dict())

# untuk menampilkan data kita sendiri
@app.get('/penduduk', response_model=List[Penduduk])
async def post_penduduk():
    return data_penduduk

# untuk get data sendiri (berdasakan index)
def get_penduduk_index(nik):
    for index, penduduk in enumerate(data_penduduk):
        if penduduk['nik'] == nik:
            return index
    return None

# untuk get data sendiri (berdasarkan NIK)
@app.get("/penduduk/{id_data}", response_model=Optional[Penduduk])
def get_penduduk_by_id(nik: int):
    for penduduk in data_penduduk:
        if penduduk['nik'] == nik:
            return Penduduk(**penduduk)
    return None

# untuk update data sendiri 
@app.put("/penduduk/{id_data}")
def update_penduduk_by_id(nik: int, update_penduduk: Penduduk):
    index = get_penduduk_index(nik)
    if index is not None:
        data_penduduk[index] = update_penduduk.dict()
        return {"message": "Data (nama datanya) berhasil diperbarui."}
    else:
        raise HTTPException(status_code=404, detail="Data (nama datanya) Tidak Ditemukan.")
    

# untuk menghapus data
@app.delete("/penduduk/{id_data}")
def delete_penduduk_by_id(nik: int):
    index = get_penduduk_index(nik)
    if index is not None:
        del data_penduduk[index]
        return {"message": "Data (nama datanya) Berhasil Dihapus."}
    else:
        raise HTTPException(status_code=404, detail="Data (nama datanya) Tidak Berhasil Dihapus.")
    
# untuk get data dari kelompok asuransi menggunakan url web hosting
async def get_penduduk_from_web():
    url = "path url"  #endpoint kelompok asuransi
    response = requests.get(url)
    if response.status.code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail = "Gagal mengambil (nama datanya).")

# untuk get data dari kelompok bank menggunakan url web hosting
async def get_asuransi_from_web():
    url = "path url"  #endpoint kelompok bank
    response = requests.get(url)
    if response.status.code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail = "Gagal mengambil (nama datanya).")

# untuk get data dari kelompok bank menggunakan url web hosting (bank)
async def get_bank_from_web():
    url = "path url"  #endpoint kelompok bank
    response = requests.get(url)
    if response.status.code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail = "Gagal mengambil (nama datanya).")
    
class Asuransi(BaseModel):
    nik: int
    nama: str

class Bank(BaseModel):
    nik: int
    nama: str

# untuk mendapatkan hasil dari kelompok lain (asuransi)
@app.get('/penduduk', response_model=List[Asuransi])
async def get_asuransi():
    data_asuransi = get_asuransi_from_web()
    return data_asuransi
# untuk mendapatkan hasil dari kelompok lain (bank)
@app.get('/penduduk', response_model=List[Bank])
async def get_bank():
    data_bank = get_bank_from_web()
    return data_bank