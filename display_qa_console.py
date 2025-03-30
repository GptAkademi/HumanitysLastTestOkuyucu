import pandas as pd
import base64
import io
from PIL import Image
import os
import tempfile
import webbrowser
import sys
import textwrap

def is_base64_image(s):
    if not isinstance(s, str):
        return False
    
    # Check if it looks like a base64 string
    if not s.startswith('data:image') and not s.startswith('/9j/') and not s.startswith('iVBOR'):
        return False
        
    try:
        # Try to extract base64 data
        if s.startswith('data:image'):
            # Extract the base64 part (after comma)
            s = s.split(',', 1)[1]
        
        # Try to decode and see if it forms a valid image
        img_data = base64.b64decode(s)
        Image.open(io.BytesIO(img_data))
        return True
    except:
        return False

def decode_and_save_image(base64_str, temp_dir, filename):
    try:
        # For data URLs, extract the base64 part
        if base64_str.startswith('data:image'):
            base64_str = base64_str.split(',', 1)[1]
            
        # Decode base64 string
        img_data = base64.b64decode(base64_str)
        img = Image.open(io.BytesIO(img_data))
        
        # Save to temporary file
        file_path = os.path.join(temp_dir, filename)
        img.save(file_path)
        return file_path
    except Exception as e:
        print(f"Error decoding image: {e}")
        return None

def print_header(text):
    """Print a formatted header with the given text"""
    width = os.get_terminal_size().columns - 4  # -4 for the '## ' prefix and space at end
    print("\n" + "=" * width)
    print(f"## {text}")
    print("=" * width)

def print_subheader(text):
    """Print a formatted subheader with the given text"""
    width = os.get_terminal_size().columns - 4  # -4 for the '-- ' prefix and space at end
    print("\n" + "-" * width)
    print(f"-- {text}")
    print("-" * width)

def print_wrapped_text(text, initial_indent='', subsequent_indent='  '):
    """Print text with proper wrapping to fit the terminal width"""
    width = os.get_terminal_size().columns
    wrapper = textwrap.TextWrapper(
        width=width, 
        initial_indent=initial_indent,
        subsequent_indent=subsequent_indent,
        break_long_words=False,
        break_on_hyphens=False
    )
    print(wrapper.fill(text))

def display_qa_console():
    # Load the parquet file
    file_path = 'test-00000-of-00001.parquet'
    try:
        df = pd.read_parquet(file_path)
        print(f"Loaded {len(df)} questions from {file_path}")
        
        # Create temporary directory for images
        with tempfile.TemporaryDirectory() as temp_dir:
            current_index = 0
            total_qa = len(df)
            
            while True:
                os.system('cls' if os.name == 'nt' else 'clear')
                print_header(f"Soru/Cevap {current_index + 1}/{total_qa}")
                
                row = df.iloc[current_index]
                
                # Display question
                question = row.get('question', '')
                if isinstance(question, str):
                    if is_base64_image(question):
                        img_path = decode_and_save_image(question, temp_dir, f"question_{current_index}.png")
                        print_subheader("SORU (Görüntü)")
                        print(f"[Görüntü dosyası: {img_path}]")
                        
                        # Open image in default viewer
                        if img_path:
                            webbrowser.open(f"file://{os.path.abspath(img_path)}")
                    else:
                        print_subheader("SORU")
                        print_wrapped_text(question)
                
                # Display additional image if exists
                image = row.get('image', '')
                if isinstance(image, str) and image:
                    if is_base64_image(image):
                        img_path = decode_and_save_image(image, temp_dir, f"additional_image_{current_index}.png")
                        print_subheader("İLAVE GÖRSEL")
                        print(f"[Görüntü dosyası: {img_path}]")
                        
                        # Open image in default viewer
                        if img_path:
                            webbrowser.open(f"file://{os.path.abspath(img_path)}")
                
                # Display answer
                answer = row.get('answer', '')
                if isinstance(answer, str):
                    if is_base64_image(answer):
                        img_path = decode_and_save_image(answer, temp_dir, f"answer_{current_index}.png")
                        print_subheader("CEVAP (Görüntü)")
                        print(f"[Görüntü dosyası: {img_path}]")
                        
                        # Open image in default viewer
                        if img_path:
                            webbrowser.open(f"file://{os.path.abspath(img_path)}")
                    else:
                        print_subheader("CEVAP")
                        print_wrapped_text(answer)
                
                # Display rationale if exists
                rationale = row.get('rationale', '')
                if isinstance(rationale, str) and rationale:
                    print_subheader("AÇIKLAMA (RATIONALE)")
                    print_wrapped_text(rationale)
                
                # Display rationale image if exists
                rationale_image = row.get('rationale_image', '')
                if isinstance(rationale_image, str) and rationale_image:
                    if is_base64_image(rationale_image):
                        img_path = decode_and_save_image(rationale_image, temp_dir, f"rationale_image_{current_index}.png")
                        print_subheader("AÇIKLAMA GÖRSELİ")
                        print(f"[Görüntü dosyası: {img_path}]")
                        
                        # Open image in default viewer
                        if img_path:
                            webbrowser.open(f"file://{os.path.abspath(img_path)}")
                
                # Navigation options
                print("\n" + "=" * (os.get_terminal_size().columns - 1))
                print("Önceki: 'p', Sonraki: 'n', Çıkış: 'q'")
                
                # Get user input
                choice = input("Seçim: ").strip().lower()
                
                if choice == 'q':
                    break
                elif choice == 'p' and current_index > 0:
                    current_index -= 1
                elif choice == 'n' and current_index < total_qa - 1:
                    current_index += 1
    
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    display_qa_console() 