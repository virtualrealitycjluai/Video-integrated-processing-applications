# task2.py
import requests

def task():
    try:
        response = requests.get("https://api.github.com")
        with open("task2.log", "w") as f:
            f.write(f"Task 2 (requests from env2) Status Code: {response.status_code}\n")
    except Exception as e:
        with open("task2.log", "w") as f:
            f.write(f"Task 2 encountered an error: {e}\n")

if __name__ == "__main__":
    task()
