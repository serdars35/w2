import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

# Sahibinden'de filtrelenmiş URL
url = 'https://www.sahibinden.com/arazi-suv-pickup-renault-kadjar/manuel/ikinci-el?a277_max=2019&a277_min=2017&a116446=1263360'
sent_file = 'sent_ads.txt'  # Daha önce gönderilen ilanların kaydedileceği dosya

# Sahibinden'i kontrol eden fonksiyon
def check_new_cars():
    response = requests.get(url)

    if response.status_code != 200:
        print("Sayfaya erişilemedi.")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    cars = soup.find_all('tr', {'class': 'searchResultsItem'})

    # Daha önce gönderilen ilanları oku
    sent_ads = read_sent_ads()

    # İlanları tarayıp e-posta göndermek için
    for car in cars:
        title = car.find('td', {'class': 'searchResultsTitleValue'}).text.strip()
        price = car.find('td', {'class': 'searchResultsPriceValue'}).text.strip()
        location = car.find('td', {'class': 'searchResultsLocationValue'}).text.strip()
        link = car.find('a')['href']  
        full_link = f"https://www.sahibinden.com{link}"

        # Eğer ilan daha önce gönderilmediyse
        if title not in sent_ads:
            print(f"Yeni ilan bulundu: {title} - {price} - {location}")
            send_email(title, price, location, full_link)
            save_sent_ad(title)  # İlanı kaydet

# Daha önce gönderilen ilanları okuma fonksiyonu
def read_sent_ads():
    if os.path.exists(sent_file):
        with open(sent_file, 'r') as file:
            return file.read().splitlines()  # Dosyadaki her satırı bir liste elemanı yap
    return []

# Yeni ilanı kaydetme fonksiyonu
def save_sent_ad(title):
    with open(sent_file, 'a') as file:
        file.write(title + '\n')  # Yeni ilanı dosyaya ekle

# E-posta gönderme fonksiyonu
def send_email(title, price, location, full_link):
    sender_email = "cann09x@gmail.com"
    receiver_email = "serdarcan100@gmail.com"
    password = "nitjzqpmquwcebth"  # Google Uygulama Şifren

    subject = f"Yeni Araç İlanı: {title}"
    body = f"Başlık: {title}\nFiyat: {price}\nLokasyon: {location}\nLink: {full_link}"

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, password)
        text = msg.as_string()
        server.sendmail(sender_email, receiver_email, text)
        server.quit()
        print(f"E-posta gönderildi: {title}")
    except Exception as e:
        print(f"E-posta gönderme başarısız: {e}")

# Sahibinden'i kontrol etme fonksiyonunu çağır
if __name__ == "__main__":
    check_new_cars()
