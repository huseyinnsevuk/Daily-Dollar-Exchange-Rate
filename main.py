import requests
import xml.etree.ElementTree as ET
from datetime import datetime

# TCMB Günlük Kur Sayfası (XML Formatında)
URL = "https://www.tcmb.gov.tr/kurlar/today.xml"

def get_exchange_rates():
    try:
        # 1. Veriyi internetten çek
        response = requests.get(URL)
        response.raise_for_status() # Hata varsa programı durdur

        # 2. XML verisini ayrıştır (Parsing)
        root = ET.fromstring(response.content)
        
        usd_buy = "0"
        usd_sell = "0"
        eur_buy = "0"
        eur_sell = "0"

        # XML içindeki para birimlerini dolaş
        for currency in root.findall('Currency'):
            code = currency.get('Kod')
            
            if code == "USD":
                usd_buy = currency.find('BanknoteBuying').text
                usd_sell = currency.find('BanknoteSelling').text
            elif code == "EUR":
                eur_buy = currency.find('BanknoteBuying').text
                eur_sell = currency.find('BanknoteSelling').text

        return usd_buy, usd_sell, eur_buy, eur_sell

    except Exception as e:
        print(f"Hata oluştu: {e}")
        return None, None, None, None

def update_files():
    usd_buy, usd_sell, eur_buy, eur_sell = get_exchange_rates()
    
    if usd_buy is None:
        return # Veri çekilemediyse dosyaları bozma

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # --- LOG.md Dosyasına Ekleme (Geçmiş Veriler) ---
    log_entry = f"| {now} | 🇺🇸 USD: {usd_sell} | 🇪🇺 EUR: {eur_sell} |\n"
    
    with open("LOG.md", "a", encoding="utf-8") as file:
        file.write(log_entry)

    # --- README.md Dosyasını Yenileme (Dashboard Görünümü) ---
    readme_content = f"""
# 💰 Günlük Döviz Takip Botu
*Bu proje Python ile TCMB verilerini otomatik çeker ve her gün günceller.*

### 🚀 Son Güncelleme: {now}

| Döviz Tipi | Alış (TL) | Satış (TL) |
| :--- | :---: | :---: |
| **🇺🇸 Dolar (USD)** | {usd_buy} | {usd_sell} |
| **🇪🇺 Euro (EUR)** | {eur_buy} | {eur_sell} |

---
*Veriler [TCMB](https://www.tcmb.gov.tr) üzerinden XML servisi ile anlık alınmıştır.*
    """
    
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(readme_content)

if __name__ == "__main__":
    update_files()