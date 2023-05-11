import socket
import os

HOST = '127.0.0.1' #Loopback IP digunakan untuk mengakses localhost atau server lokal pada komputer
PORT = 5055 #Nomor port server yang digunakan
BASE_DIR = os.path.dirname(os.path.abspath(__file__)) #Base Directory


#Fungsi di bawah untuk mnengklasifikasikan tipe konten yang diminta oleh client
def get_content_type(filename):
    if filename.endswith('.html'):
        return 'text/html'
    elif filename.endswith('.jpg'):
        return 'image/jpg'
    elif filename.endswith('.png'):
        return 'image/png'
    elif filename.endswith('.gif'):
        return 'image/gif'
    else:
        return 'application/octet-stream' 

#Fungsi di bawah untuk membaca file menggunakan read binary
def get_file_content(filename):
    with open(filename, 'rb') as f:
        content = f.read()
    return content

#Fungsi di bawah digunakan untuk menerima permintaan dari klien dan mengembalikan respon http
def generate_http_response(request):
    response = ''
    try:
        filename = request.split()[1][1:] #Menggunakan metode split untuk mengambil filename dari path file
        if filename == '': #String kosong
            filename = 'index.html' #return index.html
        filepath = os.path.join(BASE_DIR, filename) #menggabungkan file path dan file direktori menggunakan metode join
        if os.path.isfile(filepath): #Pengkondisian ketika file yang diminta oleh klien ditemukan
            content_type = get_content_type(filepath) #Klasifikasi tipe konten
            content = get_file_content(filepath)
            response_header = 'HTTP/1.1 200 OK\r\nContent-Type: {}\r\nContent-Length: {}\r\n\r\n'.format(
                content_type, len(content))
            response = response_header.encode('utf-8') + content
        else: #Apabila file tidak ditemukan
            response = b'HTTP/1.1 404 Not Found\r\n\r\n<h1>404 Not Found</h1>'
    except Exception as e:
        print(str(e))
    return response

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT)) #Menghubungkan antara HOST dan PORT
    s.listen() #Mendengarkan request dari client
    print(f"Server berjalan di {HOST}:{PORT}") #Server berjalan

    while True:
        conn, addr = s.accept() #Menerima koneksi server
        with conn:
            print('Terhubung dengan', addr) #Koneksi diterima
            data = conn.recv(1024) #Menerima request dari client
            request = data.decode()
            response = generate_http_response(request) #Mengembalikan respon ke client
            method, path, protocol = request.split('\n')[0].split()
            print('Method:', method)
            print('Path:', path)
            print('Protocol:', protocol)

            conn.sendall(response)
            conn.close()










