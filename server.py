import logging
import os
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import worker  # Import the worker module

# Initialize Flask app and CORS
app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
app.logger.setLevel(logging.ERROR)


# Define the route for the index page
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')  # Render the index.html template


# Define the route for processing messages
@app.route('/process-message', methods=['POST'])
def process_message_route():
    user_message = request.json.get('userMessage', '')  # Extract the user's message from the request
    if not user_message:
        return jsonify({"botResponse": "No message provided"}), 400

    try:
        bot_response = worker.process_prompt(user_message)  # Process the user's message using the worker module
    except Exception as e:
        app.logger.error(f"Error processing message: {e}")
        return jsonify({"botResponse": "An error occurred while processing your message."}), 500

    # Return the bots response as JSON
    return jsonify({"botResponse": bot_response}), 200


# Define the route for processing documents
@app.route('/process-document', methods=['POST'])
def process_document_route():
    # Check if a file was uploaded
    if 'file' not in request.files:
        return jsonify({
                           "botResponse": "It seems like the file was "
                                          "not uploaded correctly, can you try again. "
                                          "If the problem persists, try using a different file"}), 400

    file = request.files['file']  # Extract the uploaded file from the request

    if file.filename == '':
        return jsonify({"botResponse": "No selected file"}), 400

    file_path = os.path.join("uploads", file.filename)  # Define the path where the file will be saved
    os.makedirs(os.path.dirname(file_path), exist_ok=True)  # Create the directory if it does not exist
    file.save(file_path)  # Save the file

    try:
        worker.process_document(file_path)  # Process the document using the worker module
    except Exception as e:
        app.logger.error(f"Error processing document: {e}")
        return jsonify({"botResponse": "An error occurred while processing your document."}), 500

    # Return a success message as JSON
    return jsonify({
                       "botResponse": "Thank you for providing your PDF document. "
                                      "I have analyzed it, so now you can ask me any questions regarding it!"}), 200


# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True, port=8000, host='0.0.0.0')
