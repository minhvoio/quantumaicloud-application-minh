from fastapi import FastAPI
from pydantic import BaseModel
import random

app = FastAPI()

class ListRequest(BaseModel):
    n: int

class SearchRequest(BaseModel):
    k: int
    list_n: list

@app.post("/generate_list")
def generate_random_list(request: ListRequest):
    n = request.n
    list_n = []
    for _ in range(n * 2):
        temp = random.getrandbits(n)
        while temp in list_n:
            temp = random.getrandbits(n)
        list_n.append(temp)
    k = random.getrandbits(n)
    return {"k": k, "list_n": list_n}

@app.post("/search_k")
def search_k(request: SearchRequest):
    k = request.k
    list_n = request.list_n
    list_n.sort()
    if k == list_n[0] or k == list_n[-1]:
        return {"found": True, "n_steps": 1}
    
    left = 0
    right = len(list_n) - 1
    n_steps = 0

    while left <= right:
        n_steps += 1
        mid = (left + right) // 2

        if k == list_n[mid]:
            return {"found": True, "n_steps": n_steps}
        elif k < list_n[mid]:
            right = mid - 1
        else:
            left = mid + 1

    return {"found": False, "n_steps": n_steps}

@app.post("/less_than_k")
def less_than_k(request: SearchRequest):
    k = request.k
    list_n = request.list_n
    list_n.sort()

    k_exist, n_steps = search_k(SearchRequest(k=k, list_n=list_n))

    if not k_exist:
        return {"list_nk": [], "n_steps": 1}

    result = []
    for idx, num in enumerate(list_n):
        n_steps += 1
        if num < k:
            result.append(num)
        else:
            break

    return {"list_nk": result, "n_steps": n_steps}

@app.get("/")
def read_root():
    return {"message": "Welcome to Binary Search API"}