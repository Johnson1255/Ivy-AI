import random
import time
from gtts import gTTS
from playsound import playsound
from googletrans import Translator

class BadAppleEasterEgg:
    def __init__(self):
        # Original Bad Apple lyrics with Spanish translations
        self.bad_apple_lyrics = [
            {
                "original": "What color is the deep sea?",
                "spanish": "¿De qué color es el mar profundo?"
            },
            {
                "original": "What color is the heart?",
                "spanish": "¿De qué color es el corazón?"
            },
            {
                "original": "Bad apple",
                "spanish": "Manzana mala"
            },
            {
                "original": "",
                "spanish": ""
            },
            {
                "original": "サイレンがなり響く街",
                "spanish": "Una ciudad donde suena la sirena"
            },
            {
                "original": "今日も君は探している",
                "spanish": "Hoy también estás buscando"
            },
            {
                "original": "君の為に踊る影を",
                "spanish": "La sombra que baila por ti"
            },
            {
                "original": "見えない翼広げて",
                "spanish": "Extendiendo alas invisibles"
            },
            {
                "original": "",
                "spanish": ""
            },
            {
                "original": "落ちていく世界の中で",
                "spanish": "En un mundo que cae"
            },
            {
                "original": "君は何を見つめている?",
                "spanish": "¿Qué estás mirando?"
            },
            {
                "original": "Bad Apple!!",
                "spanish": "¡Manzana Mala!"
            }
        ]
        
        # Activation triggers for text input
        self.text_triggers = [
            "canta bad apple", 
            "reproducir bad apple", 
            "cantar bad apple"
        ]
        
        # Activation triggers for voice input
        self.voice_triggers = [
            "bad apple", 
            "canta bad apple", 
            "play bad apple"
        ]
    
    def check_text_trigger(self, user_input):
        """
        Check if the user input matches any text triggers
        
        Args:
            user_input (str): User's input text
        
        Returns:
            bool: True if a trigger is found, False otherwise
        """
        return any(trigger in user_input.lower() for trigger in self.text_triggers)
    
    def activate_easter_egg(self, output_method='print'):
        """
        Activate the Bad Apple Easter Egg with different output methods
        
        Args:
            output_method (str): Output method ('print', 'speech', or 'return')
        
        Returns:
            str: The generated response
        """
        # Prepare initial response
        response = "¡Oh! Parece que quieres escuchar Bad Apple. ¡Aquí vamos!\n\n"
        
        # Simulate preparation
        for _ in range(3):
            response += "🎵 "
        response += "\n\n"
        
        # Text for voice conversion
        speech_text = ""
        
        # Add lyrics
        for line in self.bad_apple_lyrics:
            # Display both versions
            if line["original"]:
                response += f"Original: {line['original']}\n"
                response += f"Español: {line['spanish']}\n\n"
                
                # Accumulate text for voice conversion
                speech_text += line['spanish'] + ". "
        
        # Final message
        final_message = "¡Espero que hayas disfrutado de Bad Apple!"
        response += f"\n{final_message}"
        speech_text += final_message
        
        # Process output method
        if output_method == 'print':
            print(response)
            return response
        
        elif output_method == 'speech':
            # Convert to Spanish audio
            tts = gTTS(text=speech_text, lang="es")
            filename = "bad_apple_easter_egg.mp3"
            tts.save(filename)
            playsound(filename)
            return response
        
        else:
            return response
    
    def process_input(self, user_input, input_type='text'):
        """
        Process user input to activate the Easter Egg
        
        Args:
            user_input (str): User's input text
            input_type (str): Input type ('text' or 'voice')
        
        Returns:
            str or None: Easter egg response or None if not triggered
        """
        # Check triggers based on input type
        if input_type == 'text':
            if self.check_text_trigger(user_input):
                return self.activate_easter_egg(output_method='return')
        
        elif input_type == 'voice':
            # Logic for voice input recognition
            if any(trigger in user_input.lower() for trigger in self.voice_triggers):
                return self.activate_easter_egg(output_method='speech')
        
        return None

# Example usage
def main():
    bad_apple = BadAppleEasterEgg()
    
    # Text activation example
    print("Text trigger test:")
    result = bad_apple.process_input("Ivy, canta bad apple")
    if result:
        print(result)
    
    # Voice activation example (simulated)
    print("\nVoice trigger test:")
    voice_result = bad_apple.process_input("bad apple", input_type='voice')
    if voice_result:
        print(voice_result)

if __name__ == "__main__":
    main()