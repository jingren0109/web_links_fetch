import time

import requests
import threading


class Producer(threading.Thread):
    def __init__(self, url_queue, urls):
        super().__init__()
        self.url_queue = url_queue
        self.urls = urls
        self.max_retries = 3

    def run(self):
        for url in self.urls:
            retries = 0
            while retries < self.max_retries:
                try:
                    content = self.fetch_content(url)
                    self.url_queue.put((url, content))
                    break  # Content fetched successfully, break out of the retry loop
                except Exception as e:
                    retries += 1
                    print(f"Error fetching content from {url} (Attempt {retries}): {e}")
                    time.sleep(2 ** retries)  # Exponential backoff
            else:
                print(f"Failed to fetch content from {url} after {self.max_retries} attempts.")

        self.url_queue.put(None)


    def fetch_content(self, url):
        response = requests.get(url)
        response.raise_for_status()  # will raise an HTTPError if the HTTP request returned an unsuccessful status code
        return response.text


if __name__ == "__main__":
    # Example usage for testing
    from queue import Queue
    urls = ["https://qmplus.qmul.ac.uk", "https://www.greatfrontend.com/front-end-interview-guidebook"]
    q = Queue()
    producer = Producer(q, urls)
    producer.start()
    producer.join()

    # Printing the contents from the queue for testing
    while not q.empty():
        url, content = q.get()
        print(f"Content from {url} fetched!")
