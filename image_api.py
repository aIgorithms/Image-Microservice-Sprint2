from flask import Flask, request, jsonify

app = Flask(__name__)

# Temp database to test the endpoint
MOCK_DB = {
    "architecture": {
        "url": "https://example.com/images/architecture.jpg", 
        "alt": "A tall modern building"
    },
    "golf": {
        "url": "https://example.com/images/golf.jpg", 
        "alt": "A person swinging a golf club on a green course"
    }
}

# Fallback image for when a word is not found
PLACEHOLDER = {
    "url": "https://example.com/images/placeholder.jpg",
    "alt": "Image not found placeholder"
}

@app.route('/image', methods=['GET'])
def get_image():
    # Get the keyword from the URL
    keyword = request.args.get('keyword')
    
    # Get the size from the URL, or use "medium" as a backup
    size = request.args.get('size', 'medium') 

    # Check if the keyword is missing
    if not keyword:
        # Create an error message
        error_message = {"error": "Keyword parameter is required"}
        return jsonify(error_message), 400

    # Create a list of allowed sizes
    valid_sizes = ["small", "medium", "large"]
    
    # Check if the requested size is valid
    if size not in valid_sizes:
        # Change it to medium if it is invalid
        size = "medium"

    # Convert keyword to string and lowercase it
    search_word = str(keyword)
    search_word = search_word.lower()
    
    # Check if the word exists in our database
    if search_word in MOCK_DB:
        
        # Get the image data
        image_data = MOCK_DB[search_word]
        
        # Build the success response
        response = {
            "keyword_searched": search_word,
            "image_url": image_data["url"],
            "alt_text": image_data["alt"],
            "is_placeholder": False
        }
        
        # Send the response back
        return jsonify(response), 200
        
    else:
        # Build the fallback response
        response = {
            "keyword_searched": search_word,
            "image_url": PLACEHOLDER["url"],
            "alt_text": PLACEHOLDER["alt"],
            "is_placeholder": True
        }
        
        # Send the fallback response back
        return jsonify(response), 200

if __name__ == '__main__':
    app.run(port=5004, debug=True)