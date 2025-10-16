# 🐧 Cyux VPS Yöneticisi

[![Lisans: MIT](https://img.shields.io/badge/Lisans-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Katkıda Bulun](https://img.shields.io/badge/Katk%C4%B1da%20Bulun-A%C3%A7%C4%B1k-brightgreen.svg)](https://github.com/selmandemir/vps-manager-t-rk-e/graphs/contributors)

**Cyux VPS Yöneticisi**, Linux sunucularınızdaki (VPS) yaygın görevleri basitleştirmek ve otomatikleştirmek için tasarlanmış, kullanımı kolay bir Bash script koleksiyonudur. Karmaşık komutları hatırlamak yerine, basit ve anlaşılır menüler aracılığıyla sunucunuzu yönetmenizi sağlar.

Bu proje, [januda-ui/DRAGON-VPS-MANAGER](https://github.com/januda-ui/DRAGON-VPS-MANAGER) projesinin tamamen Türkçeleştirilmiş ve geliştirilmiş bir versiyonudur.

## ✨ Öne Çıkan Özellikler

-   **Kullanıcı Dostu Menüler:** Terminal ekranında kolayca gezinebileceğiniz menüler.
-   **Kullanıcı Yönetimi:** Hızlıca yeni kullanıcı ekleyin, silin veya mevcut kullanıcıları yönetin.
-   **Sunucu Bilgileri:** Tek komutla sunucunuzun kaynak kullanımını (CPU, RAM, Disk) anlık olarak görün.
-   **Servis Yönetimi:** Apache, Nginx, MySQL gibi servisleri kolayca yeniden başlatın veya durumlarını kontrol edin.
-   **Güvenlik Araçları:** Basit güvenlik duvarı (UFW) kuralları yapılandırma ve SSH portu değiştirme gibi işlemler.
-   **Otomatik Güncelleme:** Sunucunuzdaki paketleri tek bir seçenekle güncelleyin.
-   **Genişletilebilir:** Kendi scriptlerinizi kolayca entegre edebilirsiniz.

## 🚀 Kurulum ve Kullanım

Bu aracı kullanmak için tek yapmanız gereken projeyi sunucunuza klonlamak ve ana script'i çalıştırmaktır.

1.  **Projeyi Klonlayın:**
    ```bash
    git clone [https://github.com/selmandemir/vps-manager-t-rk-e.git](https://github.com/selmandemir/vps-manager-t-rk-e.git)
    ```

2.  **Klasöre Gidin:**
    ```bash
    cd vps-manager-t-rk-e
    ```

3.  **Script'i Çalıştırın:**
    Script'e çalışma izni verin ve çalıştırın.
    ```bash
    chmod +x dragon.sh
    ./dragon.sh
    ```
    *Not: Ana script dosyasının adını daha sonra `cyux.sh` olarak değiştirebiliriz.*

## 🤝 Katkıda Bulunma

Bu proje topluluk katkılarına açıktır. Çevirilerde bir hata bulursanız, yeni bir özellik eklemek isterseniz veya mevcut bir hatayı düzeltmek isterseniz lütfen çekinmeyin!

1.  Bu projeyi **fork'layın**.
2.  Kendi özelliğiniz için yeni bir dal (`git checkout -b yeni-ozellik`) oluşturun.
3.  Değişikliklerinizi yapın ve **commit'leyin** (`git commit -m 'Yeni bir özellik eklendi'`).
4.  Dalınızı itin (`git push origin yeni-ozellik`).
5.  Bir **Pull Request** (PR) oluşturun.

## 📄 Lisans

Bu proje, MIT Lisansı altında lisanslanmıştır. Daha fazla bilgi için `LICENSE` dosyasına göz atın.

---