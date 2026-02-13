import requests
from bs4 import BeautifulSoup
import os
import time

URLS_TO_CRAWL = [
    'https://habr.com/ru/articles/995558/',
    'https://habr.com/ru/articles/996022/',
    'https://habr.com/ru/articles/995592/',
    'https://habr.com/ru/articles/995542/',
    'https://habr.com/ru/articles/995582/',
    'https://habr.com/ru/articles/996108/',
    'https://habr.com/ru/articles/996006/',
    'https://habr.com/ru/articles/996056/',
    'https://habr.com/ru/articles/995914/',
    'https://habr.com/ru/articles/995604/',
    'https://habr.com/ru/articles/995518/',
    'https://habr.com/ru/articles/995982/',
    'https://habr.com/ru/articles/996014/',
    'https://habr.com/ru/articles/995826/',
    'https://habr.com/ru/articles/996106/',
    'https://habr.com/ru/articles/996028/',
    'https://habr.com/ru/articles/995602/',
    'https://habr.com/ru/articles/995560/',
    'https://habr.com/ru/articles/995548/',
    'https://habr.com/ru/articles/996064/',
    'https://habr.com/ru/articles/995632/',
    'https://habr.com/ru/articles/995890/',
    'https://habr.com/ru/articles/995712/',
    'https://habr.com/ru/articles/996044/',
    'https://habr.com/ru/articles/995882/',
    'https://habr.com/ru/articles/996074/',
    'https://habr.com/ru/articles/995838/',
    'https://habr.com/ru/articles/995884/',
    'https://habr.com/ru/articles/995988/',
    'https://habr.com/ru/articles/995506/',
    'https://habr.com/ru/articles/996144/',
    'https://habr.com/ru/articles/995502/',
    'https://habr.com/ru/articles/995678/',
    'https://habr.com/ru/articles/995906/',
    'https://habr.com/ru/articles/995626/',
    'https://habr.com/ru/articles/996080/',
    'https://habr.com/ru/articles/996000/',
    'https://habr.com/ru/articles/995964/',
    'https://habr.com/ru/articles/995804/',
    'https://habr.com/ru/articles/996086/',
    'https://habr.com/ru/articles/995554/',
    'https://habr.com/ru/articles/977490/',
    'https://habr.com/ru/articles/995538/',
    'https://habr.com/ru/articles/995596/',
    'https://habr.com/ru/articles/995944/',
    'https://habr.com/ru/articles/995706/',
    'https://habr.com/ru/articles/995868/',
    'https://habr.com/ru/articles/995676/',
    'https://habr.com/ru/articles/995574/',
    'https://habr.com/ru/articles/995794/',
    'https://habr.com/ru/articles/995762/',
    'https://habr.com/ru/articles/995422/',
    'https://habr.com/ru/articles/995608/',
    'https://habr.com/ru/articles/996136/',
    'https://habr.com/ru/articles/996098/',
    'https://habr.com/ru/articles/996052/',
    'https://habr.com/ru/articles/995646/',
    'https://habr.com/ru/articles/995482/',
    'https://habr.com/ru/articles/995078/',
    'https://habr.com/ru/articles/995722/',
    'https://habr.com/ru/articles/995900/',
    'https://habr.com/ru/articles/995818/',
    'https://habr.com/ru/articles/995082/',
    'https://habr.com/ru/articles/995724/',
    'https://habr.com/ru/articles/995594/',
    'https://habr.com/ru/articles/996026/',
    'https://habr.com/ru/articles/995546/',
    'https://habr.com/ru/articles/995960/',
    'https://habr.com/ru/articles/995690/',
    'https://habr.com/ru/articles/995504/',
    'https://habr.com/ru/articles/995674/',
    'https://habr.com/ru/articles/995846/',
    'https://habr.com/ru/articles/995056/',
    'https://habr.com/ru/articles/995962/',
    'https://habr.com/ru/articles/995634/',
    'https://habr.com/ru/articles/982434/',
    'https://habr.com/ru/articles/995640/',
    'https://habr.com/ru/articles/995038/',
    'https://habr.com/ru/articles/995544/',
    'https://habr.com/ru/articles/995600/',
    'https://habr.com/ru/articles/995664/',
    'https://habr.com/ru/articles/995854/',
    'https://habr.com/ru/articles/995624/',
    'https://habr.com/ru/articles/994928/',
    'https://habr.com/ru/articles/996036/',
    'https://habr.com/ru/articles/996068/',
    'https://habr.com/ru/articles/995984/',
    'https://habr.com/ru/articles/995772/',
    'https://habr.com/ru/articles/995496/',
    'https://habr.com/ru/articles/995822/',
    'https://habr.com/ru/articles/995450/',
    'https://habr.com/ru/articles/995528/',
    'https://habr.com/ru/articles/995348/',
    'https://habr.com/ru/articles/995622/',
    'https://habr.com/ru/articles/996060/',
    'https://habr.com/ru/articles/995860/',
    'https://habr.com/ru/articles/995902/',
    'https://habr.com/ru/articles/995976/',
    'https://habr.com/ru/articles/995532/',
    'https://habr.com/ru/articles/995694/',
    'https://habr.com/ru/articles/995736/',
    'https://habr.com/ru/articles/995536/',
    'https://habr.com/ru/articles/995718/',
    'https://habr.com/ru/articles/994986/',
    'https://habr.com/ru/articles/996128/',
    'https://habr.com/ru/articles/993788/',
    'https://habr.com/ru/articles/995728/',
    'https://habr.com/ru/articles/995484/',
    'https://habr.com/ru/articles/996120/',
    'https://habr.com/ru/articles/995556/',
]

OUTPUT_DIR = "downloaded_pages"

INDEX_FILE = "index.txt"
REQUEST_DELAY = 1

def create_directories():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

def save_page(url, content, file_index):
    filename = os.path.join(OUTPUT_DIR, f"page_{file_index:04d}.txt")
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    return filename

def create_index_entry(file_index, url):
    return f"{file_index}: {url}\n"

def is_valid_page(response):
    if response.status_code != 200:
        print(f"  [!] Неуспешный статус: {response.status_code}")
        return False

    content_type = response.headers.get('Content-Type', '').lower()
    if 'text/html' not in content_type:
        print(f"  [!] Не HTML контент: {content_type}")
        return False
    soup = BeautifulSoup(response.content, 'html.parser')
    text = soup.get_text(strip=True)
    if not text or len(text) < 50: 
        print("  [!] Контент страницы слишком короткий или пустой.")
        return False
    if soup.find('script') and not soup.find('body'):
        print("  [!] Подозрение на страницу, загружаемую через JS.")
        return False

    print("  [*] Страница валидна.")
    return True

def crawl_pages(urls):
    create_directories()
    index_content = ""
    file_counter = 1

    for url in urls:
        print(f"\n[*] Скачивание: {url}")
        try:
            response = requests.get(url, timeout=10)
            if is_valid_page(response):
                filename = save_page(url, response.text, file_counter)
                index_content += create_index_entry(file_counter, url)
                print(f"  [+] Сохранено в: {filename}")
                file_counter += 1
            else:
                print("  [!] Страница пропущена.")

        except requests.exceptions.RequestException as e:
            print(f"  [!] Ошибка при запросе {url}: {e}")
        except Exception as e:
            print(f"  [!] Неизвестная ошибка при обработке {url}: {e}")

        time.sleep(REQUEST_DELAY)
        if file_counter > 100:
            print(f"\n[*] Собрано минимально необходимое количество страниц ({file_counter - 1}). Завершение работы.")
            break

    with open(INDEX_FILE, "w", encoding="utf-8") as f:
        f.write(index_content)
    print(f"\n[*] Файл {INDEX_FILE} создан.")

if __name__ == "__main__":
    if len(URLS_TO_CRAWL) < 100:
        print("Предупреждение: Список URL содержит менее 100 адресов. Краулер попытается собрать 100 страниц, но может не достигнуть цели, если список исчерпается.")

    crawl_pages(URLS_TO_CRAWL)
    print("\n[*] Задание выполнено.")
