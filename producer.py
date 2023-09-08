import time

import requests
import threading


class Producer(threading.Thread):
    def __init__(self, url_queue, urls):
        super().__init__()
        self.url_queue = url_queue
        self.urls = urls
        self.max_retries = 3
        self.errors = []

    def run(self):
        for url in self.urls:
            retries = 0
            while retries < self.max_retries:
                try:
                    content = self.fetch_content(url)
                    self.url_queue.put((url, content))
                    break
                except Exception as e:
                    retries += 1
                    self.errors.append(f"Error fetching content from {url} (Attempt {retries}): {e}")
                    print(f"Error fetching content from {url} (Attempt {retries}): {e}")
                    time.sleep(2 ** retries)
            else:
                self.errors.append(f"Failed to fetch content from {url} after {self.max_retries} attempts.")
                print(f"Failed to fetch content from {url} after {self.max_retries} attempts.")

        self.url_queue.put(None)


    def fetch_content(self, url):
        response = requests.get(url)
        response.raise_for_status()
        return response.text


if __name__ == "__main__":
    from queue import Queue
    urls = ["https://qmplus.qmul.ac.uk", "https://www.greatfrontend.com/front-end-interview-guidebook"]
    q = Queue()
    producer = Producer(q, urls)
    producer.start()
    producer.join()

    while True:
        item = q.get()
        if item is None:
            break
        url, content = item
        print(f"Content from {url} fetched!")

