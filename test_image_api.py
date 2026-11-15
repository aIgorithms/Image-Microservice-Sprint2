import requests

URL = "http://localhost:5004/image"


def test_image(keyword, size="medium"):
    print(f"\nSearching for: {keyword!r}, size: {size}")
    try:
        response = requests.get(
            URL, params={"keyword": keyword, "size": size}, timeout=15
        )
        print("HTTP status:", response.status_code)
        print("Response:", response.json())
    except requests.RequestException as error:
        print("Request failed:", error)


test_image("golf", "large")
test_image("architecture", "small")

test_image("zzzxxyyqqnotarealimage12345")

test_image("")
