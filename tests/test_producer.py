import unittest
from queue import Queue
from unittest.mock import patch
from producer import Producer


class TestProducer(unittest.TestCase):

    def test_fetch_content_failure(self):
        with patch('requests.get') as mock_get:
            mock_get.side_effect = Exception("Mocked exception")
            url_queue = Queue()
            urls = ["https://www.invalid.com"]
            producer = Producer(url_queue, urls)
            with self.assertRaises(Exception):
                producer.fetch_content(urls[0])

    def test_run_with_retry_success(self):
        with patch('requests.get') as mock_get:
            mock_get.side_effect = [Exception("Attempt 1"), Exception("Attempt 2"), "Mocked content"]
            url_queue = Queue()
            urls = ["https://youtube.com"]
            producer = Producer(url_queue, urls)
            producer.start()
            producer.join()
            self.assertFalse(producer.is_alive())

    def test_run_with_retry_failure(self):
        with patch('requests.get') as mock_get:
            mock_get.side_effect = [Exception("Attempt 1"), Exception("Attempt 2"), Exception("Attempt 3")]
            url_queue = Queue()
            urls = ["https://www.youtube.com"]
            producer = Producer(url_queue, urls)
            producer.run()
            self.assertTrue(any("Failed to fetch content" in error for error in producer.errors))

    def test_run_with_success(self):
        with patch('requests.get') as mock_get:
            mock_get.return_value.status_code = 200
            mock_get.return_value.text = 'Mocked content'
            url_queue = Queue()
            urls = ["https://www.youtube.com"]
            producer = Producer(url_queue, urls)
            producer.run()
            item = url_queue.get()
            self.assertIsNotNone(item)
            url, content = item
            self.assertEqual(url, urls[0])
            self.assertEqual(content, 'Mocked content')


if __name__ == "__main__":
    unittest.main()
