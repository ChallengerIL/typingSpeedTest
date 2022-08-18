from tkinter import *
import re
from random import shuffle


# Remove all non-alphabetic characters
def clean_sources():
    with open('source.txt', 'r', encoding="utf8") as file:
        string = file.read()

    # Get rid of everything except for lower and upper case letters, lowercase what's left and filter it by word length
    words_list = [word.lower() for word in re.sub("[^a-zA-z]", " ", string).split() if len(word) > 1]

    # Convert the list to a set and back to get rid of duplicates (plus a benefit of randomization)
    return [*set(words_list)]


class App(Tk):
    BG_COLOR = "#162026"
    FG_COLOR = "#fff"
    PANEL_FONT = ("Arial", 15)
    TEXT_FONT = ("Arial", 30)

    def __init__(self, seconds: int = 60):
        super().__init__()
        self.word = str()
        self.text = clean_sources()
        self.time_value = seconds
        self.total_time = seconds
        self.score = 0
        self.passed = 0

        # Specify window's title
        self.title("Typing Speed Test")

        # Assign weight to center everything inside the window
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # Change background color
        self.configure(background=self.BG_COLOR)

        # Get user's screen size and scale it down
        self.screen_width = self.winfo_screenwidth() // 2
        self.screen_height = self.winfo_screenheight() // 2

        # Create fixed initial geometry of the window
        self.geometry(f'{self.screen_width}x{self.screen_height}')
        self.resizable(False, False)

        # Create a frame in which all the subsequent widgets will be stored
        self.frame = Frame(self, width=self.screen_width, height=self.screen_height, background=self.BG_COLOR)
        # Place the frame on the grid
        self.frame.grid()

        self.info_panel = PanedWindow(self.frame, background=self.BG_COLOR)
        self.info_panel.grid(column=0, row=0)

        self.wpm_label = Label(self.info_panel, text="WPM:", background=self.BG_COLOR, foreground=self.FG_COLOR,
                               font=self.PANEL_FONT)
        self.info_panel.add(self.wpm_label)

        self.wpm_score = Label(self.info_panel, text=self.score, background=self.BG_COLOR, foreground=self.FG_COLOR,
                               font=self.PANEL_FONT, width=2)
        self.info_panel.add(self.wpm_score)

        self.time_label = Label(self.info_panel, text="Time left:", background=self.BG_COLOR, foreground=self.FG_COLOR,
                                font=self.PANEL_FONT)
        self.info_panel.add(self.time_label)

        self.time_left = Label(self.info_panel, background=self.BG_COLOR, foreground=self.FG_COLOR,
                               font=self.PANEL_FONT, width=2)
        self.info_panel.add(self.time_left)

        self.text_label = Label(self.frame, background=self.BG_COLOR, foreground=self.FG_COLOR, font=self.TEXT_FONT)
        self.text_label.grid(column=0, row=1, pady=(30, 30))

        self.entry_field = Entry(self.frame, width=30)
        self.entry_field.grid(column=0, row=2)
        # Activate the entry field on launch
        self.entry_field.focus()

        self.hint = Label(self.frame, text="Press 'Space bar' to continue", background=self.BG_COLOR,
                          foreground=self.FG_COLOR)
        self.hint.grid(column=0, row=3, pady=20)

        self.restart_button = Button(self.frame, text="Restart", command=self.restart)

        # If there is time left
        if self.time_value > 0:
            self.get_next_word()
            self.bind("<space>", self.compare_words)

        self.countdown()

    def countdown(self):
        # Subtract from time left
        self.time_value -= 1
        # Update data on the screen
        self.time_left.configure(text=self.time_value)

        # If there is still time left
        if self.time_value > 0:
            # Call countdown again after 1000ms (1s)
            self.after(1000, self.countdown)
        else:
            self.entry_field.configure(state=DISABLED)
            self.restart_button.grid(column=0, row=4, pady=30)

    def get_next_word(self):
        # Get the first word from the list
        self.word = self.text[0]
        # Remove that word from the list
        self.text.remove(self.word)

        # Display the word to user
        self.text_label.configure(text=self.word)

    def compare_words(self, event):
        if self.word == self.entry_field.get().strip():
            self.passed += 1
            # Calculate Words Per Minute
            self.score = int((self.passed / (self.total_time - self.time_value)) * 60)
            # Display current score
            self.wpm_score.configure(text=self.score)

        # Clear entry field
        self.entry_field.delete(0, END)
        # Update the word label
        self.get_next_word()

    def restart(self):
        self.score = 0
        self.passed = 0
        shuffle(self.text)
        self.time_value = self.total_time

        self.entry_field.configure(state=NORMAL)
        self.get_next_word()
        self.wpm_score.configure(text=self.score)
        self.time_left.configure(text=self.time_value)

        self.restart_button.grid_forget()
        self.countdown()


if __name__ == "__main__":
    app = App()
    app.mainloop()
