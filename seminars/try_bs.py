import requests

def main():
        response = requests.get('https://orenday.ru/news/', headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
    })
    step_time = random.randrange(4,10)
    time.sleep(step_time)

        print(response.status_code)
        print(response.text)