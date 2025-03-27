import re
import argparse
import os

def convert_note(note):
    """Convert a note based on old-to-new notation mapping."""
    # Mapping for converting between old and new notation
    old_to_new = {
        # Core note conversions
        'a': '1',
        's': '2',
        'd': '3',
        'f': '4',
        'g': '5',
        'h': '6',
        'j': '7',
        '1': 'a',
        '2': 's',
        '3': 'd',
        '4': 'f',
        '5': 'g',
        '6': 'h',
        '7': 'j',
        '8': 'q',
        '9': 'w',
        '0': 'e'
    }
    
    # If the note is in the mapping, convert it
    if note in old_to_new:
        return old_to_new[note]
    return note

def replace_letters_with_numbers(text):
    """Process the text to convert notes in lines with specific format."""
    exceptions = [
        'lh', 'rh', 'c', 'ac'
    ]
    
    word_replacements = {
        word: f"__SPECIAL_WORD_{i}__" for i, word in enumerate(exceptions)
    }
    
    # Compile a regular expression to find exceptions
    sorted_exceptions = sorted(exceptions, key=len, reverse=True)
    pattern = r'\b(' + '|'.join(re.escape(word) for word in sorted_exceptions) + r')\b'
    exception_regex = re.compile(pattern)
    
    # A regular expression to find strings where we want to replace notes
    # Format: number (with optional 'b' part), spaces, letter i, spaces, content
    note_line_pattern = r'^(\d+(?:b\d+)?\s+i\s+)(.+)$'
    
    # Split the text into lines
    lines = text.split('\n')
    result_lines = []
    
    # Track the current section (lh or rh)
    current_section = None
    
    for line in lines:
        # Check if this line starts with 'lh' or 'rh'
        if line.strip().startswith('lh'):
            current_section = 'lh'
            result_lines.append(line)
            continue
        elif line.strip().startswith('rh'):
            current_section = 'rh'
            result_lines.append(line)
            continue
        
        # Check if we need to replace notes in this line
        note_line_match = re.match(note_line_pattern, line)
        
        if note_line_match:
            # Split the string into prefix (number + i + space) and content
            prefix = note_line_match.group(1)
            content = note_line_match.group(2)
            
            # Protect special words in prefix
            prefix = exception_regex.sub(lambda m: word_replacements.get(m.group(), m.group()), prefix)
            
            # Restore protected words
            for word, placeholder in word_replacements.items():
                prefix = prefix.replace(placeholder, word)
            
            # Find all notes and other characters in content
            note_pattern = r'[asdfghjqwertyuiop1234567890]'
            notes = re.findall(note_pattern, content)
            other_chars = re.split(note_pattern, content)
            
            # Convert each note
            converted_notes = [convert_note(note) for note in notes]
            
            # Reconstruct content
            content = ''
            for i in range(len(converted_notes)):
                content += other_chars[i] + converted_notes[i]
            if len(other_chars) > len(converted_notes):
                content += other_chars[-1]
            
            # Putting the string back together
            processed_line = prefix + content
            
        else:
            # For all other lines, keep them as they are
            processed_line = line
        
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
