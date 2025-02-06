# main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import httpx
import math
from typing import List, Dict, Union

app = FastAPI(title="Number Classification API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

async def get_number_fact(number: int) -> str:
    """Fetch a math fact about the number from the Numbers API."""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"http://numbersapi.com/{number}/math")
        return response.text

def is_prime(n: int) -> bool:
    """Check if a number is prime."""
    if n < 2:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def is_perfect(n: int) -> bool:
    """Check if a number is perfect (sum of proper divisors equals the number)."""
    if n <= 1:
        return False
    divisors_sum = sum(i for i in range(1, n) if n % i == 0)
    return divisors_sum == n

def is_armstrong(n: int) -> bool:
    """Check if a number is an Armstrong number."""
    num_str = str(n)
    power = len(num_str)
    return n == sum(int(digit) ** power for digit in num_str)

def get_digit_sum(n: int) -> int:
    """Calculate the sum of digits in a number."""
    return sum(int(digit) for digit in str(n))

def get_number_properties(n: int) -> List[str]:
    """Get a list of properties for a number."""
    properties = []
    
    # Check if number is Armstrong
    if is_armstrong(n):
        properties.append("armstrong")
    
    # Check if odd or even
    properties.append("odd" if n % 2 else "even")
    
    return properties

@app.get("/api/classify-number")
async def classify_number(number: Union[int, str]) -> Dict:
    """
    Classify a number and return its properties.
    """
    try:
        num = int(number)
    except (ValueError, TypeError):
        return {
            "number": number,
            "error": True
        }

    properties = get_number_properties(num)
    fun_fact = await get_number_fact(num)
    
    return {
        "number": num,
        "is_prime": is_prime(num),
        "is_perfect": is_perfect(num),
        "properties": properties,
        "digit_sum": get_digit_sum(num),
        "fun_fact": fun_fact
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)