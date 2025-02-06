# main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import httpx
import math
from typing import List, Dict, Union

app = FastAPI(title="Number Classification API")


@app.get("/")
@app.head("/")
@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "Server is running"}

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"], 
)


async def get_number_fact(number: int) -> str:
    """Fetch a math fact"""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"http://numbersapi.com/{number}/math")
            response.raise_for_status()  # Raise HTTPError for bad responses
            return response.text
        except httpx.HTTPError as exc:
            return f"Error fetching fact: {exc}"  # Simplified error message
        except Exception as e:
            return f"An unexpected error occurred: {e}"
        

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
async def classify_number(number: Union[int, str]) -> JSONResponse:
    """Classify a number (edge case handling)."""

    if number is None or number == "":  # Check for None or empty string
        return JSONResponse(status_code=400, content={"number": number, "error": True})

    try:
        num = int(number)

        if isinstance(number, str) and not number.isdigit():
            return JSONResponse(status_code=400, content={"number": number, "error": True})

        if num < 0:
            return JSONResponse(status_code=400, content={"number": number, "error": True})

    except (ValueError, TypeError):
        return JSONResponse(status_code=400, content={"number": number, "error": True})

    properties = get_number_properties(num)
    fun_fact = await get_number_fact(num)

    return JSONResponse(content={
        "number": num,
        "is_prime": is_prime(num),
        "is_perfect": is_perfect(num),
        "properties": properties,
        "digit_sum": get_digit_sum(num),
        "fun_fact": fun_fact
    })

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)