# Required library imports
import csv          # Module for handling CSV files
import random      # Module for generating random numbers and selections
from gtts import gTTS      # Google Text-to-Speech for converting text to speech
from playsound import playsound  # Module for playing audio files

def load_responses(file_path):
    """
    Loads and processes responses from a CSV file.
    
    Args:
        file_path (str): Path to the CSV file containing the responses
        
    Returns:
        dict: Nested dictionary containing questions, personalities, and their respective responses
    """
    # Initialize dictionary to store all responses
    responses = {}
    
    # Open CSV file in read mode with UTF-8 encoding
    with open(file_path, 'r', encoding='utf-8') as file:
        # Create CSV reader that will interpret the file as a dictionary
        reader = csv.DictReader(file)
        
        # Iterate through each row in the CSV file
        for row in reader:
            # Extract values from each column
            question = row['question']        # Question
            personality = row['personality']  # Personality type
            # Split multiple responses using the '|' separator
            answers = row['answers'].split('|')  
            
            # Create nested structure to store responses
            if question not in responses:
                # If question doesn't exist, create a new dictionary for it
                responses[question] = {}
            # Store responses associated with the personality
            responses[question][personality] = answers
            
    return responses

def get_response(question, responses, personality=None):
    """
    Retrieves a random response for a specific question.
    
    Args:
        question (str): Question to be answered
        responses (dict): Dictionary containing all available responses
        personality (str, optional): Personality type for the response
        
    Returns:
        str: Randomly selected response
        
    Note:
        If personality is not specified or not found, it will select from all available responses
    """
    # Check if the question exists in the responses dictionary
    if question in responses:
        if personality and personality in responses[question]:
            # If personality is specified and exists, select from its responses
            return random.choice(responses[question][personality])
        # If no personality specified or not found, select from all responses
        return random.choice([
            resp for resp_list in responses[question].values() 
            for resp in resp_list
        ])
    # Default message if question is not found
    return "Lo siento, no tengo una respuesta para esa pregunta."

# Main execution block
def main():
    """
    Main function that executes the program flow
    
    This function:
    1. Loads responses from CSV
    2. Gets a response for a test question
    3. Converts the response to speech
    4. Plays the generated audio
    """
    # Load responses from CSV file
    responses = load_responses('ivy_responses.csv')
    
    # Define test question and personality
    question = "¿Quién eres?"
    personality = "Friendly"
    
    # Get a response from the system
    response = get_response(question, responses, personality)
    
    # Create Text-to-Speech object with the response
    # 'es' specifies Spanish language for speech synthesis
    tts = gTTS(text=response, lang="es")
    
    # Define audio file name
    filename = "answer.mp3"
    
    # Save the generated audio
    tts.save(filename)
    
    # Play the generated audio file
    playsound(filename)

# Program entry point
# This ensures the main() function only runs if the script is executed directly
if __name__ == "__main__":
    main()