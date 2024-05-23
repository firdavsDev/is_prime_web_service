# Prime Number Calculator Web Service

A simple asynchronous web service built with aiohttp to calculate the number of prime numbers in a given interval.

## Features

- Asynchronous handling of HTTP requests with aiohttp
- Calculation of prime numbers using a sieve algorithm
- Supports PUT and GET methods for submitting calculation tasks and retrieving results
- Ability to specify a timeout for GET requests
- Caching of calculation results for improved performance

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/your_username/prime-number-calculator.git
    ```

2. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Start the web service:

    ```bash
    python app.py 5000
    ```
    or
    
    ```bash
    docker-compose up --build --remove-orphans
    
    ```

2. Submit a calculation task using PUT method:

    ```bash
    curl -X PUT "http://localhost:5000/number?v=100"
    ```

3. Retrieve the result using GET method:

    ```bash
    curl http://localhost:5000/number
    ```

    You can also specify a timeout for the GET request:

    ```bash
    curl http://localhost:5000/number?timeout=5
    ```

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any improvements or bug fixes.

## Acknowledgements
* [aiohttp](https://docs.aiohttp.org/en/stable/index.html)
* [Community](https://github.com/firdavsDev/Task_Award)
* [Article](https://pythonist.ru/aiohttp-in-python/)
* [Article](https://awstip.com/how-to-handle-a-million-requests-in-a-day-using-django-25eefaee8aad)