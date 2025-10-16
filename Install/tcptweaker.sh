#!/bin/bash
# Başlık metnini mavi arka plan üzerine beyaz ve kalın olarak yazdır.
tput setaf 7 ; tput setab 4 ; tput bold ; printf '%35s%s%-20s\n' "TCP İyileştirici 1.0" ; tput sgr0

# /etc/sysctl.conf dosyasında bizim özel işaretimiz olan "#PH56" var mı diye kontrol et.
# Eğer varsa, ayarlar zaten yapılmış demektir.
if [[ `grep -c "^#PH56" /etc/sysctl.conf` -eq 1 ]]
then
    echo ""
    echo "TCP İyileştirici ağ ayarları sisteme zaten eklenmiş!"
    echo ""
    # Kullanıcıya ayarları kaldırmak isteyip istemediğini sor. Varsayılan cevap 'h' (hayır).
    read -p "TCP İyileştirici ayarlarını kaldırmak istiyor musunuz? [e/h]: " -e -i h cevap0
    
    # Eğer kullanıcı 'e' (evet) derse...
    if [[ "$cevap0" = 'e' ]]; then
        # sysctl.conf dosyasından bizim eklediğimiz tüm satırları sil ve geçici bir dosyaya yaz.
        grep -v "^#PH56
net.ipv4.tcp_window_scaling = 1
net.core.rmem_max = 16777216
net.core.wmem_max = 16777216
net.ipv4.tcp_rmem = 4096 87380 16777216
net.ipv4.tcp_wmem = 4096 16384 16777216
net.ipv4.tcp_low_latency = 1
net.ipv4.tcp_slow_start_after_idle = 0" /etc/sysctl.conf > /tmp/syscl && mv /tmp/syscl /etc/sysctl.conf
        
        # Değiştirilen ayarları sisteme uygula.
        sysctl -p /etc/sysctl.conf > /dev/null
        
        echo ""
        echo "TCP İyileştirici ağ ayarları başarıyla kaldırıldı."
        echo ""
    exit
    else 
        # Eğer kullanıcı 'h' derse, hiçbir şey yapmadan çık.
        echo ""
        exit
    fi
else
    # Eğer ayarlar daha önce eklenmemişse...
    echo ""
    echo "Bu deneysel bir script'tir. Sorumluluk size aittir!"
    echo "Bu script, gecikmeyi azaltmak ve hızı artırmak için"
    echo "bazı ağ ayarlarını değiştirecektir."
    echo ""
    # Kullanıcıya kuruluma devam etmek isteyip istemediğini sor. Varsayılan 'h' (hayır).
    read -p "Kuruluma devam edilsin mi? [e/h]: " -e -i h cevap
    
    # Eğer kullanıcı 'e' (evet) derse...
    if [[ "$cevap" = 'e' ]]; then
        echo ""
        echo "Aşağıdaki ayarlar değiştiriliyor:"
        echo " " >> /etc/sysctl.conf
        # Özel işaretimizi ve ağ ayarlarını /etc/sysctl.conf dosyasının sonuna ekle.
        echo "#PH56" >> /etc/sysctl.conf
        echo "net.ipv4.tcp_window_scaling = 1
net.core.rmem_max = 16777216
net.core.wmem_max = 16777216
net.ipv4.tcp_rmem = 4096 87380 16777216
net.ipv4.tcp_wmem = 4096 16384 16777216
net.ipv4.tcp_low_latency = 1
net.ipv4.tcp_slow_start_after_idle = 0" >> /etc/sysctl.conf
        echo ""
        # Eklenen yeni ayarları sisteme uygula ve ekranda göster.
        sysctl -p /etc/sysctl.conf
        echo ""
        echo "TCP İyileştirici ağ ayarları başarıyla eklendi."
        echo ""
    else
        # Eğer kullanıcı 'h' derse, işlemi iptal et.
        echo ""
        echo "Kurulum kullanıcı tarafından iptal edildi!"
        echo ""
    fi
fi
exit