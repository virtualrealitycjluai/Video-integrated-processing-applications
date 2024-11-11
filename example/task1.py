# task1.py
import requests

def task():
    try:
        response = requests.get("https://api.github.com")
        with open("task1.log", "w") as f:
            f.write(f"Task 1 (requests from env1) Status Code: {response.status_code}\n")
    except Exception as e:
        with open("task1.log", "w") as f:
            f.write(f"Task 1 encountered an error: {e}\n")

if __name__ == "__main__":
    task()
