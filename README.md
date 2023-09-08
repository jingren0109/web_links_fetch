# Web Link Extractor

Web Link Extractor is a simple producer/consumer system designed to extract hyperlinks from given URLs. The producer fetches the content of specified URLs, and the consumer parses this content to extract and save hyperlinks.

## Features

- Concurrently fetches and processes URLs.
- Isolation in error handling: One failed fetch or parse doesn't halt the entire process.
- Saves hyperlinks for each URL in a structured manner.

## Setup

1. **Clone the repository:**

```bash
git clone [Your Repository URL]
```

2. **Navigate to the project directory:**

```bash
cd web_link_extractor
```

3. **Install dependencies:**

```bash
pip install -r requirements.txt
```

## Usage

1. Add your URLs to the `urls.txt` file, one URL per line.

2. Run the program:

```bash
python main.py
```

3. Check the `output_links.txt` for the extracted hyperlinks.

## Testing

To run unit tests:

```bash
python -m unittest discover
```