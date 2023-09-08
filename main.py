from concurrent.futures import ThreadPoolExecutor
from queue import Queue

from constants import NUM_CONSUMER_THREADS
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
    # Load URLs from a file
    urls = load_urls_from_file("urls.txt")

    # Create a shared queue for the producer and consumer
    url_queue = Queue()

    # Initialize the producer and consumer
    producer = Producer(url_queue, urls)
    consumer = Consumer(url_queue, "output_links.txt")

    # Start the producer and consumer
    producer.start()
    consumer.start()

    # Wait for the producer and consumer to finish
    producer.join()
    consumer.join()

    print("All URLs processed and links saved!")


if __name__ == "__main__":
    main()
