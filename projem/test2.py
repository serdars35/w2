import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Sahibinden'de filtrelenmiş URL
url = 'https://www.sahibinden.com/arazi-suv-pickup-renault-kadjar/manuel/ikinci-el?a277_max=2019&a277_min=2017&a116446=1263360'

# Sahibinden'i kontrol eden fonksiyon
def check_new_cars():
    response = requests.get(url)

    # Gelen cevabı kontrol etmek için ekliyoruz:
    print("HTML yanıtını kontrol et:")
    print(response.text)  # HTML yanıtını görmek için
    
    soup = BeautifulSoup(response.text, 'html.parser')

    # Sahibinden'deki ilanları bulma
    cars = soup.find_all('tr', {'class': 'searchResultsItem'})

    # İlanları tarayıp e-posta göndermek için
    for car in cars:
        title = car.find('td', {'class': 'searchResultsTitleValue'}).text.strip()
        price = car.find('td', {'class': 'searchResultsPriceValue'}).text.strip()
        location = car.find('td', {'class': 'searchResultsLocationValue'}).text.strip()
        link = car.find('a')['href']  # İlanın linki (göreceli URL)

        full_link = f"https://www.sahibinden.com{link}"  # Tam URL oluşturma
        
        # Özel filtreleme yapmak istersen burayı genişletebilirsin
        if 'Kadjar' in title:
            print(f"İlan bulundu: {title} - {price} - {location}")  # İlan bilgilerini terminalde göster
            send_email(title, price, location, full_link)

# E-posta gönderme fonksiyonu
def send_email(title, price, location, full_link):
    sender_email = "cann09x@gmail.com"  # Kendi e-posta adresin
    receiver_email = "yilmazcan1000@gmail.com"  # Alıcı e-posta adresi
    password = "nitjzqpmquwcebth"  # Google Uygulama Şifren

    subject = f"Yeni KADJAR ARAC FOR YCAN: {title}"
    body = f"Başlık: {title}\nFiyat: {price}\nLokasyon: {location}\nLink: {full_link}"

    # E-posta yapısı oluşturma
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        # E-posta sunucusuna bağlanma ve e-posta gönderme
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, password)
        text = msg.as_string()
        server.sendmail(sender_email, receiver_email, text)
        server.quit()
        print(f"E-posta gönderildi: {title}")
    except Exception as e:
        print(f"E-posta gönderme başarısız: {e}")

# Test e-posta gönderme (kodun çalışıp çalışmadığını görmek için)
send_email("kadjar arac", "Test Fiyatı", "Test Lokasyonu", "https://www.sahibinden.com/arazi-suv-pickup-renault-kadjar/manuel/ikinci-el?a277_max=2019&a277_min=2017&a116446=1263360")

# Sahibinden'i kontrol etme fonksiyonunu çağır
check_new_cars()
