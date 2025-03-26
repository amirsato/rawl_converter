import re
import argparse
import os

def replace_letters_with_numbers(text):
    
    exceptions = [
        'lh', 'rh', 'minor', 'major', 'lydian', 'mixolydian', 'dorian', 'phrygian',
        'harmonic_minor', 'melodic_minor',
        'ch2', 'ch3', 'ch4', 'ch5', 'ch6', 'ch7', 'ch8', 'ch9', 'ch10', 'ch11', 
        'ch12', 'ch13', 'ch14', 'ch15', 'phrases', 'sections'
    ]
    
    word_replacements = {
        word: f"__SPECIAL_WORD_{i}__" for i, word in enumerate(exceptions)
    }
    
    letters_to_numbers = {
        'a': '1',
        's': '2',
        'd': '3',
        'f': '4',
        'g': '5',
        'h': '6',
        'j': '7'
    }
    
    numbers_to_letters = {
        '0': 'a',
        '1': 's',
        '2': 'd',
        '3': 'f',
        '4': 'g',
        '5': 'h',
        '6': 'j',
        '7': 'j',
        '8': 'q',
        '9': 'w'
    }
    
    # Compile a regular expression to find exceptions
    # Sort words by length (from long to short) to avoid partial matches
    sorted_exceptions = sorted(exceptions, key=len, reverse=True)
    pattern = r'\b(' + '|'.join(re.escape(word) for word in sorted_exceptions) + r')\b'
    exception_regex = re.compile(pattern)
    
    # A regular expression to find strings where you want to replace numbers with letters
    # Format: number, space, letter i, space, content
    num_to_letter_pattern = r'^(\d+\s+i\s+)(.+)$'
    
    # Split the text into lines
    lines = text.split('\n')
    result_lines = []
    
    for line in lines:
        # Check if we need to replace numbers with letters in this line
        num_to_letter_match = re.match(num_to_letter_pattern, line)
        
        if num_to_letter_match:
            # Split the string into prefix (number + i + space) and content
            prefix = num_to_letter_match.group(1)
            content = num_to_letter_match.group(2)
            
            # Replacing numbers with letters in the content
            content = re.sub(r'[0-9]', lambda x: numbers_to_letters[x.group()], content)
            
            # Process the prefix as usual (replace letters with numbers)
            prefix = exception_regex.sub(lambda m: word_replacements.get(m.group(), m.group()), prefix)
            prefix = re.sub(r'[asdfghj]', lambda x: letters_to_numbers[x.group()], prefix)
            
            # Restore prefix exceptions
            for word, placeholder in word_replacements.items():
                prefix = prefix.replace(placeholder, word)
            
            # Putting the string back together
            processed_line = prefix + content
            
        else:
            # Temporarily replacing the exception words
            processed_line = exception_regex.sub(lambda m: word_replacements.get(m.group(), m.group()), line)
            
            # Replacing letters with numbers
            processed_line = re.sub(r'[asdfghj]', lambda x: letters_to_numbers[x.group()], processed_line)
            
            # Recovering exception words
            for word, placeholder in word_replacements.items():
                processed_line = processed_line.replace(placeholder, word)
        
        result_lines.append(processed_line)
    
    return '\n'.join(result_lines)

def process_file(input_file, output_file=None):
    """Processes the input file and writes the result to the output file."""
    
    if output_file is None:
        base_name, ext = os.path.splitext(input_file)
        output_file = f"{base_name}_converted{ext}"
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            input_text = f.read()
        
        output_text = replace_letters_with_numbers(input_text)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(output_text)
        
        print(f"The conversion is complete. The result is saved in {output_file}")
        
    except FileNotFoundError:
        print(f"Error: File {input_file} not found.")
    except Exception as e:
        print(f"An error occurred while processing a file: {str(e)}")

def main():
    """A function for processing command line arguments."""
    parser = argparse.ArgumentParser(description='Converter for rawl.rocks')
    parser.add_argument('input_file', help='Path to the input text file')
    parser.add_argument('-o', '--output', help='Output file path (optional)')
    
    args = parser.parse_args()
    
    process_file(args.input_file, args.output)

if __name__ == "__main__":
    main()