#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket, threading, select, signal, sys, time
from os import system
system("clear")

# --- Bağlantı Ayarları ---
IP = '0.0.0.0' # Dinlenecek IP adresi (0.0.0.0 = tüm arayüzler)
try:
    # Port numarasını komut satırı argümanı olarak almayı dene.
    PORT = int(sys.argv[1])
except:
    # Argüman yoksa, varsayılan olarak 8080 portunu kullan.
    PORT = 8080

PASS = '' # Proxy için parola (boş bırakılırsa parolasız çalışır)
BUFLEN = 8196 * 8 # Veri arabelleği boyutu
TIMEOUT = 60 # Zaman aşımı süresi (saniye)
MSG = '🐉ㅤCyux VPS Yöneticisiㅤ🐉' # HTTP yanıtında gösterilecek mesaj
DEFAULT_HOST = '0.0.0.0:1194' # Hedef host belirtilmezse varsayılan olarak yönlendirilecek adres (Genellikle OpenVPN portu)
RESPONSE = "HTTP/1.1 200 " + str(MSG) + "\r\n\r\n" # İstemciye gönderilecek standart HTTP 200 OK yanıtı

class Server(threading.Thread):
    """
    Sunucu sınıfı, gelen bağlantıları dinler ve her biri için yeni bir thread oluşturur.
    """
    def __init__(self, host, port):
        threading.Thread.__init__(self)
        self.running = False
        self.host = host
        self.port = port
        self.threads = []
        self.threadsLock = threading.Lock()
        self.logLock = threading.Lock()

    def run(self):
        """
        Sunucunun ana döngüsü. Sürekli olarak yeni bağlantıları kabul eder.
        """
        self.soc = socket.socket(socket.AF_INET)
        self.soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.soc.settimeout(2)
        self.soc.bind((self.host, self.port))
        self.soc.listen(0)
        self.running = True

        try:
            while self.running:
                try:
                    c, addr = self.soc.accept()
                    c.setblocking(1)
                except socket.timeout:
                    continue
                
                conn = ConnectionHandler(c, self, addr)
                conn.start()
                self.addConn(conn)
        finally:
            self.running = False
            self.soc.close()
            
    def printLog(self, log):
        """
        Log mesajlarını ekrana güvenli bir şekilde yazdırır.
        """
        self.logLock.acquire()
        print(log)
        self.logLock.release()
    
    def addConn(self, conn):
        # Yeni bağlantı thread'ini listeye ekler.
        try:
            self.threadsLock.acquire()
            if self.running:
                self.threads.append(conn)
        finally:
            self.threadsLock.release()
                    
    def removeConn(self, conn):
        # Kapanan bağlantı thread'ini listeden çıkarır.
        try:
            self.threadsLock.acquire()
            self.threads.remove(conn)
        finally:
            self.threadsLock.release()
            
    def close(self):
        # Sunucuyu ve tüm aktif bağlantıları kapatır.
        try:
            self.running = False
            self.threadsLock.acquire()
            threads = list(self.threads)
            for c in threads:
                c.close()
        finally:
            self.threadsLock.release()

class ConnectionHandler(threading.Thread):
    """
    Her bir istemci bağlantısını ayrı bir thread'de yöneten sınıf.
    """
    def __init__(self, socClient, server, addr):
        threading.Thread.__init__(self)
        self.clientClosed = False
        self.targetClosed = True
        self.client = socClient
        self.client_buffer = ''
        self.server = server
        self.log = 'Bağlantı: ' + str(addr)

    def close(self):
        """
        İstemci ve hedef sunucu bağlantılarını güvenli bir şekilde kapatır.
        """
        try:
            if not self.clientClosed:
                self.client.shutdown(socket.SHUT_RDWR)
                self.client.close()
        except:
            pass
        finally:
            self.clientClosed = True
            
        try:
            if not self.targetClosed:
                self.target.shutdown(socket.SHUT_RDWR)
                self.target.close()
        except:
            pass
        finally:
            self.targetClosed = True

    def run(self):
        """
        Bağlantının ana mantığını çalıştırır.
        """
        try:
            self.client_buffer = self.client.recv(BUFLEN)
        
            # Gelen istekten 'X-Real-Host' başlığını bularak hedef sunucuyu belirle.
            hostPort = self.findHeader(self.client_buffer, 'X-Real-Host')
            
            # Eğer başlık yoksa, varsayılan host'u kullan.
            if hostPort == '':
                hostPort = DEFAULT_HOST

            # 'X-Split' başlığını kontrol et (isteğe bağlı, bazı enjektör uygulamaları kullanır).
            split = self.findHeader(self.client_buffer, 'X-Split')
            if split != '':
                self.client.recv(BUFLEN)
            
            # Hedef host'a bağlanmayı dene.
            if hostPort != '':
                self.method_CONNECT(hostPort)
            else:
                print('- X-Real-Host başlığı bulunamadı!')
                self.client.send(b'HTTP/1.1 400 NoXRealHost!\r\n\r\n')

        except Exception as e:
            self.log += ' - hata: ' + repr(e)
            self.server.printLog(self.log)
        finally:
            self.close()
            self.server.removeConn(self)

    def findHeader(self, head, header):
        """
        Gelen istek başlıkları içinden belirli bir değeri bulur.
        """
        aux = head.find((header + ': ').encode())
    
        if aux == -1:
            return ''

        aux = head.find(b':', aux)
        head = head[aux+2:]
        aux = head.find(b'\r\n')

        if aux == -1:
            return ''

        return head[:aux].decode();

    def connect_target(self, host):
        """
        Hedef sunucuya yeni bir soket bağlantısı başlatır.
        """
        i = host.find(':')
        if i != -1:
            port = int(host[i+1:])
            host = host[:i]
        else:
            port = 22 # Varsayılan olarak SSH portu

        (soc_family, _, _, _, address) = socket.getaddrinfo(host, port)[0]
        self.target = socket.socket(soc_family)
        self.targetClosed = False
        self.target.connect(address)

    def method_CONNECT(self, path):
        """
        HTTP CONNECT metodunu işler, tüneli kurar ve veri akışını başlatır.
        """
        self.log += ' - CONNECT ' + path
        
        self.connect_target(path)
        self.client.sendall(RESPONSE.encode())
        self.client_buffer = ''
        
        self.server.printLog(self.log)
        self.doCONNECT()
                        
    def doCONNECT(self):
        """
        İstemci ve hedef arasında çift yönlü veri aktarımını sağlar.
        """
        socs = [self.client, self.target]
        count = 0
        error = False
        while True:
            count += 1
            (recv, _, err) = select.select(socs, [], socs, 3)
            if err:
                error = True
            if recv:
                for in_ in recv:
                    try:
                        data = in_.recv(BUFLEN)
                        if data:
                            if in_ is self.target:
                                self.client.send(data)
                            else:
                                self.target.send(data)
                            count = 0
                        else:
                            break
                    except:
                        error = True
                        break
            if count == TIMEOUT:
                error = True
            if error:
                break

def main(host=IP, port=PORT):
    """
    Ana fonksiyon, sunucuyu başlatır ve klavye kesintisini (CTRL+C) dinler.
    """
    print("\033[0;34m━"*8, "\033[1;32m PROXY SOCKS BAŞLATILIYOR ", "\033[0;34m━"*8, "\n")
    print("\033[1;33mIP:\033[1;32m " + IP)
    print("\033[1;33mPORT:\033[1;32m " + str(PORT) + "\n")
    print("\033[0;34m━"*10, "\033[1;32m 🐉ㅤCyux VPS Yöneticisiㅤ🐉", "\033[0;34m━\033[1;37m"*11, "\n")
    
    server = Server(host, port)
    server.start()
    
    while True:
        try:
            time.sleep(2)
        except KeyboardInterrupt:
            print('\nDurduruluyor...')
            server.close()
            break

if __name__ == '__main__':
    main()