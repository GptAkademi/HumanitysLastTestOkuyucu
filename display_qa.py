import pandas as pd
import base64
import io
import matplotlib.pyplot as plt
from PIL import Image
import tkinter as tk
from tkinter import ttk, Button, Label, Text, END, DISABLED, NORMAL, font, StringVar
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os

class QADisplayApp:
    def __init__(self, root, df):
        self.root = root
        self.df = df
        self.filtered_df = df  # Initially, filtered_df is the same as df
        self.current_index = 0
        self.total_qa = len(self.filtered_df)
        
        self.root.title("Soru-Cevap Gösterici")
        self.root.geometry("1200x900")
        
        # Define font sizes
        self.title_font = ('Arial', 16, 'bold')
        self.text_font = ('Arial', 16)
        self.button_font = ('Arial', 16)
        
        # Main frame
        main_frame = ttk.Frame(root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Filter frame
        filter_frame = ttk.Frame(main_frame, padding="5")
        filter_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Category filter
        ttk.Label(filter_frame, text="Kategori:", font=self.text_font).pack(side=tk.LEFT, padx=5)
        
        # Get unique categories
        categories = self.get_unique_categories()
        
        # Create combobox
        self.category_var = StringVar()
        self.category_combobox = ttk.Combobox(filter_frame, textvariable=self.category_var, 
                                              values=["Hepsi"] + categories, 
                                              font=self.text_font, state="readonly")
        self.category_combobox.pack(side=tk.LEFT, padx=5)
        self.category_combobox.current(0)  # Set default to "Hepsi"
        
        # Bind category selection to filter function
        self.category_combobox.bind("<<ComboboxSelected>>", self.filter_by_category)
        
        # Create notebook (tabbed interface)
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Question-Answer tab
        qa_frame = ttk.Frame(notebook, padding="10")
        notebook.add(qa_frame, text="Soru-Cevap")
        
        # Rationale tab
        rationale_frame = ttk.Frame(notebook, padding="10")
        notebook.add(rationale_frame, text="Açıklama (Rationale)")
        
        # Question section
        question_frame = ttk.LabelFrame(qa_frame, text="Soru", padding="10")
        question_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.question_text = Text(question_frame, wrap=tk.WORD, height=8, font=self.text_font)
        self.question_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.question_text.config(state=DISABLED)
        
        self.question_image_label = Label(question_frame)
        self.question_image_label.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Separate image field display
        self.image_frame = ttk.LabelFrame(qa_frame, text="İlave Görsel", padding="10")
        self.image_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.image_label = Label(self.image_frame)
        self.image_label.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Answer section
        answer_frame = ttk.LabelFrame(qa_frame, text="Cevap", padding="10")
        answer_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.answer_text = Text(answer_frame, wrap=tk.WORD, height=7, font=self.text_font)
        self.answer_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.answer_text.config(state=DISABLED)
        
        self.answer_image_label = Label(answer_frame)
        self.answer_image_label.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Rationale section
        rationale_text_frame = ttk.LabelFrame(rationale_frame, text="Açıklama", padding="10")
        rationale_text_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.rationale_text = Text(rationale_text_frame, wrap=tk.WORD, height=12, font=self.text_font)
        self.rationale_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.rationale_text.config(state=DISABLED)
        
        # Rationale image section
        rationale_img_frame = ttk.LabelFrame(rationale_frame, text="Açıklama Görseli", padding="10")
        rationale_img_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.rationale_image_label = Label(rationale_img_frame)
        self.rationale_image_label.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Navigation buttons
        nav_frame = ttk.Frame(main_frame)
        nav_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.prev_button = Button(nav_frame, text="Önceki", command=self.show_previous, font=self.button_font)
        self.prev_button.pack(side=tk.LEFT, padx=5)
        
        self.index_label = Label(nav_frame, text=f"{self.current_index + 1}/{self.total_qa}", font=self.button_font)
        self.index_label.pack(side=tk.LEFT, padx=5)
        
        self.next_button = Button(nav_frame, text="Sonraki", command=self.show_next, font=self.button_font)
        self.next_button.pack(side=tk.LEFT, padx=5)
        
        # Apply custom style to LabelFrames
        style = ttk.Style()
        style.configure('TLabelframe.Label', font=self.title_font)
        
        # Display first Q&A
        self.display_current_qa()
    
    def get_unique_categories(self):
        """Extract unique category values from dataframe"""
        if 'category' in self.df.columns:
            categories = sorted(self.df['category'].dropna().unique().tolist())
            return categories
        return []
    
    def filter_by_category(self, event=None):
        """Filter questions by selected category"""
        selected_category = self.category_var.get()
        
        if selected_category == "Hepsi":
            self.filtered_df = self.df
        else:
            self.filtered_df = self.df[self.df['category'] == selected_category]
        
        self.total_qa = len(self.filtered_df)
        if self.total_qa > 0:
            self.current_index = 0
            self.display_current_qa()
        else:
            # No questions in this category
            self.clear_widgets()
            self.index_label.config(text="0/0")
            self.prev_button.config(state=DISABLED)
            self.next_button.config(state=DISABLED)
    
    def is_base64_image(self, s):
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
    
    def decode_base64_image(self, base64_str):
        try:
            # For data URLs, extract the base64 part
            if base64_str.startswith('data:image'):
                base64_str = base64_str.split(',', 1)[1]
                
            # Decode base64 string
            img_data = base64.b64decode(base64_str)
            img = Image.open(io.BytesIO(img_data))
            return img
        except Exception as e:
            print(f"Error decoding image: {e}")
            return None
    
    def resize_image(self, img, max_width=800, max_height=400):
        # Calculate the resize ratio to fit within max dimensions
        width, height = img.size
        ratio = min(max_width/width, max_height/height)
        new_size = (int(width * ratio), int(height * ratio))
        return img.resize(new_size, Image.LANCZOS)
    
    def clear_widgets(self):
        # Clear text widgets
        self.question_text.config(state=NORMAL)
        self.question_text.delete(1.0, END)
        self.question_text.config(state=DISABLED)
        
        self.answer_text.config(state=NORMAL)
        self.answer_text.delete(1.0, END)
        self.answer_text.config(state=DISABLED)
        
        self.rationale_text.config(state=NORMAL)
        self.rationale_text.delete(1.0, END)
        self.rationale_text.config(state=DISABLED)
        
        # Clear image labels
        self.question_image_label.config(image="")
        self.answer_image_label.config(image="")
        self.image_label.config(image="")
        self.rationale_image_label.config(image="")
    
    def display_current_qa(self):
        self.clear_widgets()
        
        if self.total_qa == 0:
            return
            
        row = self.filtered_df.iloc[self.current_index]
        
        # Update question
        question = row.get('question', '')
        if isinstance(question, str):
            # Check if question is a base64 image
            if self.is_base64_image(question):
                img = self.decode_base64_image(question)
                if img:
                    img = self.resize_image(img)
                    photo = tk.PhotoImage(data=base64.b64encode(get_img_bytes(img)))
                    self.question_image_label.config(image=photo)
                    self.question_image_label.image = photo  # Keep a reference
            else:
                # Regular text question
                self.question_text.config(state=NORMAL)
                self.question_text.insert(END, question)
                self.question_text.config(state=DISABLED)
        
        # Update additional image if exists
        image = row.get('image', '')
        if isinstance(image, str) and image:
            if self.is_base64_image(image):
                img = self.decode_base64_image(image)
                if img:
                    img = self.resize_image(img)
                    photo = tk.PhotoImage(data=base64.b64encode(get_img_bytes(img)))
                    self.image_label.config(image=photo)
                    self.image_label.image = photo  # Keep a reference
        
        # Update answer
        answer = row.get('answer', '')
        if isinstance(answer, str):
            # Check if answer is a base64 image
            if self.is_base64_image(answer):
                img = self.decode_base64_image(answer)
                if img:
                    img = self.resize_image(img)
                    photo = tk.PhotoImage(data=base64.b64encode(get_img_bytes(img)))
                    self.answer_image_label.config(image=photo)
                    self.answer_image_label.image = photo  # Keep a reference
            else:
                # Regular text answer
                self.answer_text.config(state=NORMAL)
                self.answer_text.insert(END, answer)
                self.answer_text.config(state=DISABLED)
        
        # Update rationale
        rationale = row.get('rationale', '')
        if isinstance(rationale, str) and rationale:
            self.rationale_text.config(state=NORMAL)
            self.rationale_text.insert(END, rationale)
            self.rationale_text.config(state=DISABLED)
        
        # Update rationale image
        rationale_image = row.get('rationale_image', '')
        if isinstance(rationale_image, str) and rationale_image:
            if self.is_base64_image(rationale_image):
                img = self.decode_base64_image(rationale_image)
                if img:
                    img = self.resize_image(img)
                    photo = tk.PhotoImage(data=base64.b64encode(get_img_bytes(img)))
                    self.rationale_image_label.config(image=photo)
                    self.rationale_image_label.image = photo  # Keep a reference
        
        # Update index label
        self.index_label.config(text=f"{self.current_index + 1}/{self.total_qa}")
        
        # Update button states
        self.prev_button.config(state=NORMAL if self.current_index > 0 else DISABLED)
        self.next_button.config(state=NORMAL if self.current_index < self.total_qa - 1 else DISABLED)
    
    def show_next(self):
        if self.current_index < self.total_qa - 1:
            self.current_index += 1
            self.display_current_qa()
    
    def show_previous(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.display_current_qa()

def get_img_bytes(img):
    """Convert PIL Image to PNG bytes for tkinter"""
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    return img_byte_arr.getvalue()

def main():
    # Load the parquet file
    file_path = 'test-00000-of-00001.parquet'
    try:
        df = pd.read_parquet(file_path)
        print(f"Loaded {len(df)} questions from {file_path}")
        
        # Initialize tkinter app
        root = tk.Tk()
        app = QADisplayApp(root, df)
        root.mainloop()
    except Exception as e:
        print(f"Error loading parquet file: {e}")

if __name__ == "__main__":
    main() 