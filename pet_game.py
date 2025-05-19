import tkinter as tk
from tkinter import messagebox
import json
import os
import random
import string
from tkinter import ttk

class PetGame:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Pet Game")
        
        # Get screen dimensions
        self.screen_width = self.window.winfo_screenwidth()
        self.screen_height = self.window.winfo_screenheight()
        
        # Set window to fullscreen
        self.window.state('zoomed')  # This makes the window maximized
        
        # Set up the gradient background
        self.canvas = tk.Canvas(self.window, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        
        # Create gradient background
        self.update_background()
        
        # Bind window resize event
        self.window.bind('<Configure>', self.on_window_resize)
        
        # Create main frame with transparent background
        self.main_frame = tk.Frame(self.window)
        self.main_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        self.pet = {
            "name": "Buddy",
            "happiness": 100,
            "hunger": 0,
            "energy": 100
        }
        
        self.setup_ui()
        
    def on_window_resize(self, event):
        # Update background when window is resized
        self.update_background()
        
    def update_background(self):
        # Clear existing background
        self.canvas.delete("all")
        
        # Get current window size
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        
        # Create gradient background
        for i in range(height):
            # Calculate color values for gradient
            r = 0
            g = int(100 + (i/height) * 155)
            b = int(200 + (i/height) * 55)
            color = f'#{r:02x}{g:02x}{b:02x}'
            self.canvas.create_line(0, i, width, i, fill=color)
        
    def create_styled_button(self, parent, text, command):
        style = ttk.Style()
        style.configure('Custom.TButton', 
                       font=('Arial', 12, 'bold'),
                       padding=10)
        return ttk.Button(parent, text=text, command=command, style='Custom.TButton')
        
    def setup_ui(self):
        # Pet name label
        self.name_label = tk.Label(self.main_frame, 
                                 text=f"Pet Name: {self.pet['name']}", 
                                 font=("Arial", 16, "bold"),
                                 fg='black')
        self.name_label.pack(pady=15)
        
        # Stats labels
        self.stats_frame = tk.Frame(self.main_frame)
        self.stats_frame.pack(pady=15)
        
        self.happiness_label = tk.Label(self.stats_frame, 
                                      text="Happiness: 100",
                                      font=("Arial", 12),
                                      fg='black')
        self.happiness_label.grid(row=0, column=0, padx=10)
        
        self.hunger_label = tk.Label(self.stats_frame, 
                                   text="Hunger: 0",
                                   font=("Arial", 12),
                                   fg='black')
        self.hunger_label.grid(row=0, column=1, padx=10)
        
        self.energy_label = tk.Label(self.stats_frame, 
                                   text="Energy: 100",
                                   font=("Arial", 12),
                                   fg='black')
        self.energy_label.grid(row=0, column=2, padx=10)
        
        # Buttons frame
        self.button_frame = tk.Frame(self.main_frame)
        self.button_frame.pack(pady=20)
        
        # Action buttons
        self.create_styled_button(self.button_frame, "Play", self.play).grid(row=0, column=0, padx=10)
        self.create_styled_button(self.button_frame, "Feed", self.feed).grid(row=0, column=1, padx=10)
        self.create_styled_button(self.button_frame, "Sleep", self.sleep).grid(row=0, column=2, padx=10)
        
        # Save/Load frame
        self.save_frame = tk.Frame(self.main_frame)
        self.save_frame.pack(pady=15)
        
        # Save code display
        self.save_code_label = tk.Label(self.save_frame, 
                                      text="Save Code: None", 
                                      font=("Arial", 14, "bold"),
                                      fg='black')
        self.save_code_label.pack(pady=10)
        
        # Save button
        self.create_styled_button(self.save_frame, "Generate Save Code", self.save_game).pack(pady=10)
        
        # Load frame
        self.load_frame = tk.Frame(self.main_frame)
        self.load_frame.pack(pady=15)
        
        # Load code entry
        self.load_label = tk.Label(self.load_frame, 
                                 text="Enter Save Code:", 
                                 font=("Arial", 12),
                                 fg='black')
        self.load_label.pack(pady=5)
        
        self.code_entry = tk.Entry(self.load_frame, 
                                 width=15, 
                                 font=("Arial", 14),
                                 justify='center')
        self.code_entry.pack(pady=5)
        
        # Load button
        self.create_styled_button(self.load_frame, "Load Game", self.load_game).pack(pady=10)
        
        # Reset Game button
        self.create_styled_button(self.main_frame, "Reset Game", self.reset_game).pack(pady=15)
        
    def update_labels(self):
        self.name_label.config(text=f"Pet Name: {self.pet['name']}")
        self.happiness_label.config(text=f"Happiness: {self.pet['happiness']}")
        self.hunger_label.config(text=f"Hunger: {self.pet['hunger']}")
        self.energy_label.config(text=f"Energy: {self.pet['energy']}")
        
    def generate_save_code(self):
        characters = string.ascii_lowercase + string.digits
        return ''.join(random.choice(characters) for _ in range(6))
        
    def play(self):
        self.pet['happiness'] = min(100, self.pet['happiness'] + 10)
        self.pet['energy'] = max(0, self.pet['energy'] - 10)
        self.pet['hunger'] = min(100, self.pet['hunger'] + 5)
        self.update_labels()
        
    def feed(self):
        self.pet['hunger'] = max(0, self.pet['hunger'] - 20)
        self.pet['energy'] = min(100, self.pet['energy'] + 5)
        self.update_labels()
        
    def sleep(self):
        self.pet['energy'] = 100
        self.pet['hunger'] = min(100, self.pet['hunger'] + 10)
        self.update_labels()
        
    def save_game(self):
        save_code = self.generate_save_code()
        save_data = {
            'code': save_code,
            'pet': self.pet
        }
        
        with open(f'save_{save_code}.json', 'w') as f:
            json.dump(save_data, f)
            
        self.save_code_label.config(text=f"Save Code: {save_code}")
        messagebox.showinfo("Success", f"Game saved successfully!\nYour save code is: {save_code}")
        
    def load_game(self):
        save_code = self.code_entry.get().strip()
        if not save_code:
            messagebox.showerror("Error", "Please enter a save code!")
            return
            
        try:
            with open(f'save_{save_code}.json', 'r') as f:
                save_data = json.load(f)
                if save_data['code'] == save_code:
                    self.pet = save_data['pet']
                    self.update_labels()
                    self.save_code_label.config(text=f"Save Code: {save_code}")
                    self.code_entry.delete(0, tk.END)
                    messagebox.showinfo("Success", "Game loaded successfully!")
                else:
                    messagebox.showerror("Error", "Invalid save code!")
        except FileNotFoundError:
            messagebox.showerror("Error", "Save code not found!")
            
    def reset_game(self):
        self.pet = {
            "name": "Buddy",
            "happiness": 100,
            "hunger": 0,
            "energy": 100
        }
        self.save_code_label.config(text="Save Code: None")
        self.code_entry.delete(0, tk.END)
        self.update_labels()
        messagebox.showinfo("Success", "Game reset successfully!")
            
    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    game = PetGame()
    game.run()