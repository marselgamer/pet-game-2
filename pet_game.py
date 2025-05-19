import tkinter as tk
from tkinter import messagebox
import json
import os
import random
import string

class PetGame:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Pet Game")
        self.window.geometry("400x600")
        
        self.pet = {
            "name": "Buddy",  # Default pet name
            "happiness": 100,
            "hunger": 0,
            "energy": 100
        }
        
        self.setup_ui()
        
    def setup_ui(self):
        # Pet name label
        self.name_label = tk.Label(self.window, text=f"Pet Name: {self.pet['name']}", font=("Arial", 14))
        self.name_label.pack(pady=10)
        
        # Stats labels
        self.stats_frame = tk.Frame(self.window)
        self.stats_frame.pack(pady=10)
        
        self.happiness_label = tk.Label(self.stats_frame, text="Happiness: 100")
        self.happiness_label.grid(row=0, column=0, padx=5)
        
        self.hunger_label = tk.Label(self.stats_frame, text="Hunger: 0")
        self.hunger_label.grid(row=0, column=1, padx=5)
        
        self.energy_label = tk.Label(self.stats_frame, text="Energy: 100")
        self.energy_label.grid(row=0, column=2, padx=5)
        
        # Buttons frame
        self.button_frame = tk.Frame(self.window)
        self.button_frame.pack(pady=20)
        
        # Action buttons
        tk.Button(self.button_frame, text="Play", command=self.play).grid(row=0, column=0, padx=5)
        tk.Button(self.button_frame, text="Feed", command=self.feed).grid(row=0, column=1, padx=5)
        tk.Button(self.button_frame, text="Sleep", command=self.sleep).grid(row=0, column=2, padx=5)
        
        # Save/Load frame
        self.save_frame = tk.Frame(self.window)
        self.save_frame.pack(pady=10)
        
        # Save code display
        self.save_code_label = tk.Label(self.save_frame, text="Save Code: None", font=("Arial", 12))
        self.save_code_label.pack(pady=5)
        
        # Save button
        tk.Button(self.save_frame, text="Generate Save Code", command=self.save_game).pack(pady=5)
        
        # Load frame
        self.load_frame = tk.Frame(self.window)
        self.load_frame.pack(pady=10)
        
        # Load code entry
        self.load_label = tk.Label(self.load_frame, text="Enter Save Code:", font=("Arial", 10))
        self.load_label.pack(pady=2)
        
        self.code_entry = tk.Entry(self.load_frame, width=10, font=("Arial", 12))
        self.code_entry.pack(pady=2)
        
        # Load button
        tk.Button(self.load_frame, text="Load Game", command=self.load_game).pack(pady=5)
        
        # Reset Game button
        tk.Button(self.window, text="Reset Game", command=self.reset_game).pack(pady=5)
        
    def update_labels(self):
        self.name_label.config(text=f"Pet Name: {self.pet['name']}")
        self.happiness_label.config(text=f"Happiness: {self.pet['happiness']}")
        self.hunger_label.config(text=f"Hunger: {self.pet['hunger']}")
        self.energy_label.config(text=f"Energy: {self.pet['energy']}")
        
    def generate_save_code(self):
        # Generate a random 6-character code using letters and numbers
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
        
        # Save to a file with the code as the filename
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
                    self.code_entry.delete(0, tk.END)  # Clear the entry field
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
        self.code_entry.delete(0, tk.END)  # Clear the entry field
        self.update_labels()
        messagebox.showinfo("Success", "Game reset successfully!")
            
    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    game = PetGame()
    game.run()