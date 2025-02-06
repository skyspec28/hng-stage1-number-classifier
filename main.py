from fastapi import FastAPI
import httpx
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"]
)

def is_prime(n: int) -> bool:
    """Check if a number n is prime."""
    if n <= 1:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

def is_perfect(n: int) -> bool:
    """Check if a number is perfect """
    total = 0 
    for i in range(1, n):
        if n % i == 0:
            total += i
    return total == n

def is_armstrong(n: int) -> bool:
    """Check if a number is an Armstrong number."""
    if n < 0:
        return False
    digits = [int(d) for d in str(abs(n))]
    power = len(digits)
    return sum(d ** power for d in digits) == abs(n)

def digit_sum(n: int) -> int:
    
    return sum(int(digit) for digit in str(abs(n)))

async def get_fun_facts(n: int) -> str:
    """Fetch a fun fact about the number from the Numbers API asynchronously."""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"http://numbersapi.com/{n}")
        if response.status_code == 200:
            return response.text
        else:
            return "No fun fact Available"

@app.get("/api/classify-number")
async def classify_number(number: str):
    """
    Classify the provided number by calculating its mathematical properties and fetching a fun fact.
    Returns a JSON response with the classification or an error if input is invalid.
    """
    try:
        num = int(number)
    except ValueError:
        return JSONResponse(
            status_code=400,
            content={
                "number": number,
                "error": True
            }
        )

    properties = []


    if is_armstrong(num):
        properties.append("armstrong")
    
   
    if num % 2 == 0:
        properties.append("even")
    else:
        properties.append("odd")

    
    fun_fact = await get_fun_facts(num)
    
    return {
        "number": num,
        "is_prime": is_prime(num),
        "is_perfect": is_perfect(num),
        "properties": properties,
        "digit_sum": digit_sum(num),
        "fun_fact": fun_fact
    }
