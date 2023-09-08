import threading
from bs4 import BeautifulSoup
from urllib.parse import urljoin

class Consumer(threading.Thread):
    def __init__(self, url_queue, output_file):
        super().__init__()
        self.url_queue = url_queue
        self.output_file = output_file

    def run(self):
        while True:
            item = self.url_queue.get()

            # Check for sentinel value
            if item is None:
                break

            url, content = item
            links = self.extract_links(content, url)
            self.save_links(url, links)

    def extract_links(self, content, base_url):
        soup = BeautifulSoup(content, 'html.parser')
        links = {a['href'] for a in soup.find_all('a', href=True) if
                 not a['href'].startswith('#')}
        # Joining base URL with relative paths
        full_links = {urljoin(base_url, link) for link in links}
        return full_links

    def save_links(self, url, links):
        try:
            with open(self.output_file, 'a') as f:
                f.write(f"Links for {url}:\n")
                for link in links:
                    f.write(f"{link}\n")
                f.write("\n")
        except Exception as e:
            print(f"Error writing links for {url} to file: {e}")


if __name__ == "__main__":
    # Example usage for testing
    from queue import Queue
    q = Queue()
    # Simulated content for the test
    q.put(("https://qmplus.qmul.ac.uk", "<html><body><a href='https://www.link1.com'>Link1</a></body></html>"))

    consumer = Consumer(q, "output_links.txt")
    consumer.start()
    consumer.join()

    print("Links extracted and saved!")
