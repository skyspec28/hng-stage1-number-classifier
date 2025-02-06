# Number Classification API

A RESTful API that provides mathematical properties and fun facts about numbers.

## Features

- Determines if a number is prime
- Determines if a number is perfect
- Identifies Armstrong numbers
- Calculates digit sum
- Provides odd/even classification
- Fetches interesting math facts from Numbers API

## API Specification

### Endpoint

```
GET /api/classify-number?number={number}
```

### Success Response (200 OK)

```json
{
    "number": 371,
    "is_prime": false,
    "is_perfect": false,
    "properties": ["armstrong", "odd"],
    "digit_sum": 11,
    "fun_fact": "371 is an Armstrong number because 3^3 + 7^3 + 1^3 = 371"
}
```

### Error Response (400 Bad Request)

```json
{
    "number": "alphabet",
    "error": true
}
```

## Installation and Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/skyspec28/hng-stage1-number-classifier.git
   ```

2. Install dependencies:
   ```bash
   pip install fastapi uvicorn httpx
   ```

3. Run the application:
   ```bash
   uvicorn main:app --reload
   ```


## Technologies Used

- Python 3.8+
- FastAPI
- HTTPX for async HTTP requests
- Numbers API for mathematical facts

## Development

To run the application in development mode:

```bash
uvicorn main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`

## Testing

You can test the API using curl:

```bash
curl "http://localhost:8000/api/classify-number?number=371"
```

