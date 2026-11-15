from flask import Flask, request, jsonify
import requests
import re
from html import unescape

app = Flask(__name__)

Wikimedia = "https://commons.wikimedia.org/w/api.php"

Imagesizes = {"small": 320, "medium": 640, "large": 1024}

PLACEHOLDER_URL = "https://placehold.co/640x400.png?text=Image+Unavailable"


def find_image(keyword, size):
    searchsettings = {
        "action": "query",
        "format": "json",
        "generator": "search",
        "gsrsearch": keyword,
        "gsrnamespace": 6, 
        "gsrlimit": 10,
        "prop": "imageinfo",
        "iiprop": "url|mime|extmetadata",
        "iiurlwidth": Imagesizes[size],
        "iiextmetadatafilter": "ImageDescription",
    }

    try:
        response = requests.get(
            Wikimedia,
            params=searchsettings,
            headers={"User-Agent": "CS361ImageMicroservice/1.0 (student project)"},
            timeout=10,
        )
        response.raise_for_status()
        data = response.json()
    except (requests.RequestException, ValueError):
        return None

    searchresults = data.get("query", {}).get("pages", {})
    for resultspage in searchresults.values():
        images = resultspage.get("imageinfo", [])
        if not images:
            continue

        image = images[0]
        if not image.get("mime", "").startswith("image/"):
            continue

        image_url = image.get("thumburl") or image.get("url")
        if not image_url:
            continue

        details = image.get("extmetadata", {})
        description = details.get("ImageDescription", {}).get("value", "")
        description = re.sub(r"<[^>]+>", " ", description)
        description = unescape(description)
        description = " ".join(description.split())

        if not description:
            description = resultspage.get("title", "").replace("File:", "")
            description = description.rsplit(".", 1)[0].replace("_", " ")

        if not description:
            description = "Image related to " + keyword

        return {"url": image_url, "alt": description[:500]}

    return None


@app.route("/image", methods=["GET"])
def get_image():
    keyword = request.args.get("keyword", "").strip().lower()
    size = request.args.get("size", "medium").lower()

    if not keyword:
        return jsonify({"error": "Keyword parameter is required"}), 400

    if size not in Imagesizes:
        size = "medium"

    image = find_image(keyword, size)

    is_placeholder = False
    if image is None:
        is_placeholder = True
        image = {
            "url": PLACEHOLDER_URL,
            "alt": "Image unavailable placeholder",
        }

    result = {
        "keyword_searched": keyword,
        "image_url": image["url"],
        "alt_text": image["alt"],
        "is_placeholder": is_placeholder,
    }
    return jsonify(result), 200


if __name__ == "__main__":
    app.run(port=5004, debug=True)
