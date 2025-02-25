import easyocr
import groq
from groq import Groq

def analyse_image(img):
    # Initialize the reader
    reader = easyocr.Reader(['en', 'fr', 'de'])  # You can add other languages as well

    # Perform OCR on an image
    result = reader.readtext(img)

    # Initialize an empty string to hold the reconstructed text
    full_text = ""

    # Loop through the results and reconstruct the text
    previous_bottom = 0
    for detection in result:
        text = detection[1]
        top_left = detection[0][0]
        bottom_left = detection[0][3]

        # If the current text is at a lower y-coordinate, add a newline
        if bottom_left[1] > previous_bottom:
            full_text += "\n"

        # Add the recognized text with spaces (if it's not the first word)
        full_text += text + " "

        # Update the previous bottom for newline detection
        previous_bottom = bottom_left[1]

    return full_text



def generate_llm_response(full_text,user_query,api_key):

    # Replace with your actual API key
    api_key = api_key
    model_id = 'qwen-2.5-32b'  # Ensure this is the correct model ID
    client = Groq(api_key=api_key)

    response = client.chat.completions.create(
        model=model_id,
        messages=[
                {
                    "role": "system",
                    "content": """You are an expert at answering questions from the given text. 
                                Please give a concise and clear answer. Dont answer anything that is 
                                outside the given context.In such cases reply with following response-
                                I cant answer anything thats not included in the pdf """
                },   
        
            {
                "role": "user",
                "content": f"""{user_query}
                            {full_text}."""
            }
        ],
        temperature=0.3,
        max_completion_tokens=150
    )

    return response.choices[0].message.content