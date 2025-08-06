import tkinter as tk
import random
from PIL import Image, ImageTk

class MontyHallGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Monty Hall Problem")
        self.master.geometry("500x400")
        self.master.configure(bg='#f0f0f0')

        self.wins = 0
        self.losses = 0
        self.games_played = 0

        # Load images
        self.door_img = ImageTk.PhotoImage(Image.open("assets/door.png"))
        self.car_img = ImageTk.PhotoImage(Image.open("assets/car.png"))
        self.goat_img = ImageTk.PhotoImage(Image.open("assets/goat.png"))

        self.info_label = tk.Label(master, text="Choose a door (1, 2, or 3)", font=('Arial', 16, 'bold'), bg='#f0f0f0')
        self.info_label.pack(pady=20)

        self.door_frame = tk.Frame(master, bg='#f0f0f0')
        self.door_frame.pack(pady=20)

        self.doors = []
        for i in range(3):
            door_button = tk.Button(self.door_frame, image=self.door_img, borderwidth=0,
                                    command=lambda i=i: self.door_clicked(i))
            door_button.grid(row=0, column=i, padx=20)
            self.doors.append(door_button)

        self.stats_label = tk.Label(master, text=self.get_stats_text(), font=('Arial', 12), bg='#f0f0f0')
        self.stats_label.pack(pady=20)

        self.master.bind('<Key>', self.key_press)

        self.reset_game()

    def get_stats_text(self):
        return f"Games: {self.games_played} | Wins: {self.wins} | Losses: {self.losses}"

    def door_clicked(self, choice):
        if self.game_state == "choose":
            self.choose_door(choice)
        elif self.game_state == "switch":
            if self.doors[choice]['state'] != tk.DISABLED:
                self.switch_or_stay(choice)

    def reset_game(self):
        self.car_door = random.randint(0, 2)
        self.player_choice = None
        self.opened_door = None
        self.game_state = "choose"  # choose, switch, reveal

        self.info_label.config(text="Choose a door (1, 2, or 3)")
        for i, door in enumerate(self.doors):
            door.config(image=self.door_img, state=tk.NORMAL, bg='#f0f0f0')
        self.stats_label.config(text=self.get_stats_text())

    def choose_door(self, choice):
        if self.game_state != "choose":
            return

        self.player_choice = choice
        self.doors[self.player_choice].config(bg='yellow')  # highlight

        # host opens a door
        doors_to_open = [i for i in range(3) if i != self.player_choice and i != self.car_door]
        self.opened_door = random.choice(doors_to_open)
        self.doors[self.opened_door].config(image=self.goat_img, state=tk.DISABLED)

        self.game_state = "switch"
        self.info_label.config(text="Switch or stay? Choose a door.")

    def switch_or_stay(self, final_choice):
        if self.game_state != "switch":
            return

        is_win = final_choice == self.car_door
        if is_win:
            self.wins += 1
        else:
            self.losses += 1
        self.games_played += 1

        # reveal
        for i in range(3):
            if i == self.car_door:
                self.doors[i].config(image=self.car_img)
            else:
                # Only reveal the remaining goat if it wasn't the one already opened
                if i != self.opened_door:
                    self.doors[i].config(image=self.goat_img)
            self.doors[i].config(state=tk.DISABLED, bg='#f0f0f0')


        self.game_state = "reveal"
        result_text = "You win!" if is_win else "You lose!"
        self.info_label.config(text=f"{result_text} Press any key to play again.")

    def key_press(self, event):
        if self.game_state == "reveal":
            self.reset_game()
            return

        try:
            choice = int(event.char) - 1
            if choice in range(3):
                self.door_clicked(choice)
        except (ValueError, IndexError):
            pass # ignore other keys

if __name__ == "__main__":
    root = tk.Tk()
    app = MontyHallGUI(root)
    root.mainloop()
