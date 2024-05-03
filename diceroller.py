import tkinter as tk
from tkinter import ttk, scrolledtext, simpledialog, font as tkFont, messagebox
import random
import re

# Handles the dice selection from the dropdown menu
def handle_dice_selection(event=None):
    selection = dice_combo.get()
    roll_dice(selection)

# Rolls a d20 and chooses the higher roll (advantage mechanic in D&D)
def roll_dice_advantage():
    roll1, roll2 = random.randint(1, 20), random.randint(1, 20)
    result = max(roll1, roll2)
    update_result_and_history(f"{roll1} | {roll2} = {result}", "1d20 with advantage")

# Rolls a d20 and chooses the lower roll (disadvantage mechanic in D&D)
def roll_dice_disadvantage():
    roll1, roll2 = random.randint(1, 20), random.randint(1, 20)
    result = min(roll1, roll2)
    update_result_and_history(f"{roll1} | {roll2} = {result}", "1d20 with disadvantage")

# General function to roll dice based on input string (e.g., "2d6+1")
def roll_dice(dice_input):
    total_roll = 0
    history_entry = ""
    
    # Simplified parsing for dice notations and modifiers using regex
    parts = re.findall(r"([+-]?)(\d*)d(\d+)|([+-]?\d+)", dice_input.replace(" ", ""))
    
    for sign, num, dice, modifier in parts:
        if dice:  # Dice notation found
            num = int(num) if num else 1
            sign = -1 if sign == '-' else 1
            rolls = [random.randint(1, int(dice)) for _ in range(num)]
            roll_sum = sum(rolls) * sign
            total_roll += roll_sum
            history_entry += f"{'-' if sign < 0 else ''}{num}d{dice}: {' + '.join(map(str, rolls))} = {roll_sum}\n"
        elif modifier:  # Numeric modifier found
            modifier = int(modifier)
            total_roll += modifier
            history_entry += f"Modifier: {modifier}\n"
    
    # After processing all parts, add the total result
    history_entry += f"\nFinal Result: {total_roll}\n---\n"  # Include the final result in the history
    
    result_label.config(text=f'Result: {total_roll}')  # Update the result label to show the final result
    history.insert(tk.END, history_entry)  # Insert the detailed history entry including the final result
    history.see(tk.END)  # Scroll the history view to the end


# Updates the result label and history textbox
def update_result_and_history(result, history_entry):
    result_label.config(text=f'Result: {result}')
    history.insert(tk.END, f"{history_entry}\n---\n")
    history.see(tk.END)

# Prompts the user for a custom dice roll command
def prompt_roll():
    dice_command = simpledialog.askstring("Roll Dice", "Enter your roll (e.g., 1d20+2d6+3):", parent=root)
    if dice_command:
        roll_dice(dice_command)

# Clears the roll history
def clear_history():
    history.delete('1.0', tk.END)

# Adds a button for custom dice rolls dynamically
def add_custom_roll():
    expression = simpledialog.askstring("Custom Roll", "Enter custom roll (e.g., 1d8+5):", parent=root)
    if expression:
        button = tk.Button(custom_rolls_frame, text=expression, command=lambda: roll_dice(expression), 
                           bg=theme["button"], fg=theme["button_text"], font=customFont)
        button.pack()
        # Bind the right-click event to remove the button
        button.bind('<Button-3>', lambda event, b=button: remove_custom_roll(event, b))

def remove_custom_roll(event, button):
    # Removes the specified button from the UI
    button.destroy()

# GUI Setup
root = tk.Tk()
root.title("D&D Dice Roller Enhanced")
root.geometry("500x600")  # Adjusted to accommodate custom rolls

# Attempt to use a custom font, falling back to default if not found
try:
    customFont = tkFont.Font(family="MedievalSharp-Regular", size=12)
except tkFont.TclError:
    customFont = tkFont.Font(size=12)

# Themed colors for the UI
theme = {"background": '#F4EFD3', "text": '#3E4149', "button": '#8B4513', "button_text": 'white'}

# Dropdown menu for selecting dice
dice_options = ["1d4", "1d6", "1d8", "1d10", "1d12", "1d20", "1d100"]
dice_combo = ttk.Combobox(root, values=dice_options, state="readonly")
dice_combo.set("Choose dice")
dice_combo.pack(pady=10)
dice_combo.bind("<<ComboboxSelected>>", handle_dice_selection)
style = ttk.Style()
style.theme_use('clam')  # 'clam' is a theme that allows for more customization
style.configure("TCombobox", fieldbackground=theme["background"], background=theme["button"], foreground=theme["text"])
style.map('TCombobox', fieldbackground=[('readonly', theme["background"])])


root.configure(bg=theme["background"])

# UI Components for rolling, displaying results, and history
roll_button = tk.Button(root, text="Roll", command=prompt_roll, bg=theme["button"], fg=theme["button_text"], font=customFont, padx=20, pady=10)
roll_button.pack(pady=10)

adv_button = tk.Button(root, text="Roll with Advantage", command=roll_dice_advantage, bg=theme["button"], fg=theme["button_text"], font=customFont, padx=20, pady=10)
adv_button.pack(pady=5)

disadv_button = tk.Button(root, text="Roll with Disadvantage", command=roll_dice_disadvantage, bg=theme["button"], fg=theme["button_text"], font=customFont, padx=20, pady=10)
disadv_button.pack(pady=5)

result_label = tk.Label(root, text='Result:', font=customFont, bg=theme["background"], fg=theme["text"])
result_label.pack(pady=10)

history = scrolledtext.ScrolledText(root, width=50, height=10, bg="#FFF8DC", fg=theme["text"], font=('Arial', 10))
history.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

clear_history_button = tk.Button(root, text="Clear History", command=clear_history, bg=theme["button"], fg=theme["button_text"], font=customFont)
clear_history_button.pack(pady=5)

# Frame for dynamically added custom roll buttons
custom_rolls_frame = tk.Frame(root, bg=theme["background"])
custom_rolls_frame.pack(pady=10)

add_custom_roll_button = tk.Button(root, text="Add Custom Roll", command=add_custom_roll, bg=theme["button"], fg=theme["button_text"], font=customFont)
add_custom_roll_button.pack(pady=10)


root.mainloop()
