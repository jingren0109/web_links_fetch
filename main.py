from queue import Queue
from producer import Producer
from consumer import Consumer


def load_urls_from_file(filename):
    try:
        with open(filename, 'r') as f:
            return [line.strip() for line in f.readlines() if line.strip()]
    except Exception as e:
        print(f"Error reading URLs from {filename}: {e}")
        return []


def main():
    urls = load_urls_from_file("urls.txt")
    url_queue = Queue()

    producer = Producer(url_queue, urls)
    consumer = Consumer(url_queue, "output_links.txt")

    producer.start()
    consumer.start()

    producer.join()
    consumer.join()

    print("All URLs processed and links saved!")


if __name__ == "__main__":
    main()
