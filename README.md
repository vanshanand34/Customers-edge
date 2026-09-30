# Customers Edge 🛒📊

## Live Demo

**https://customers-edge.onrender.com**

A real-time price comparison web application that searches products across Amazon and Flipkart and presents the results in a single interface.

## Features

- Product search across Amazon and Flipkart
- Real-time price comparison
- Product title, price, rating, image, and product link
- Sorting results by price or rating
- Real-time result streaming using WebSockets
- Recent search history
- Trending searches
- Responsive user interface
- Automatic redirection of invalid URLs to the home page

## Tech Stack

- Django
- Django Channels
- WebSockets
- Playwright
- Chromium
- HTML, CSS, JavaScript
- Docker
- Render

## How It Works

1. Enter a product name.
2. The application searches Amazon and Flipkart.
3. Playwright retrieves the relevant product listings.
4. Results are streamed to the frontend using WebSockets.
5. Results can be sorted by price or rating.
6. Users can open the original product listing directly.

## Run Locally

### Prerequisites

- Docker installed
- Git installed

### Clone the Repository

```bash
git clone https://github.com/vanshanand34/Customers-edge.git
cd Customers-edge
```

### Build the Docker Image

The project uses a lowercase `dockerfile`:

```bash
docker build -f dockerfile -t customers-edge .
```

### Run the Application

```bash
docker run --rm -it \
  -p 8000:8000 \
  -e PORT=8000 \
  -e DEBUG=True \
  -e SECRET_KEY="local-development-secret" \
  -e ALLOWED_HOSTS="localhost,127.0.0.1" \
  customers-edge
```

Open the application at:

**http://localhost:8000**

The application runs Django, WebSockets, Playwright, and Chromium inside the Docker container.

## Live Application

**https://customers-edge.onrender.com**
