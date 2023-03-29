import tkinter as tk
from tkinter import ttk


class ScrollableFrame(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        # Create a canvas and a vertical scrollbar for scrolling
        self.canvas = tk.Canvas(self, borderwidth=0, highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(
            self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas)

        # Link the scrollbar and the canvas
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.bind("<Configure>", lambda e: self.canvas.configure(
            scrollregion=self.canvas.bbox("all")))

        # Add the scrollable frame to the canvas
        self.canvas.create_window(
            (0, 0), window=self.scrollable_frame, anchor="nw")

        # Pack the scrollbar and the canvas
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        # Allow the scrollable frame to expand and shrink with its parent
        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(
            scrollregion=self.canvas.bbox("all")))


# Create the main window
root = tk.Tk()
root.title("Sort Student Scores")

# Create the scrollable frame
scrollable_frame = ScrollableFrame(root)
scrollable_frame.pack(side="left", fill="both", expand=True)

# Create the input fields
num_students_label = tk.Label(
    scrollable_frame.scrollable_frame, text="Number of students:")
num_students_label.pack(side=tk.TOP)

num_students_entry = tk.Entry(scrollable_frame.scrollable_frame)
num_students_entry.pack(side=tk.TOP)

student_entries = []
for i in range(25):
    student_frame = tk.Frame(scrollable_frame.scrollable_frame)
    student_frame.pack(side=tk.TOP, fill="x", padx=5, pady=5)

    student_name_label = tk.Label(
        student_frame, text="Name of student {}: ".format(i+1))
    student_name_label.pack(side=tk.LEFT)

    student_name_entry = tk.Entry(student_frame)
    student_name_entry.pack(side=tk.LEFT, padx=5)

    student_score_label = tk.Label(
        student_frame, text="Score of student {}: ".format(i+1))
    student_score_label.pack(side=tk.LEFT)

    student_score_entry = tk.Entry(student_frame)
    student_score_entry.pack(side=tk.LEFT, padx=5)

    student_entries.append((student_name_entry, student_score_entry))

# Create the sort button
sort_button = tk.Button(root, text="Sort")


def sort_scores():
    # Get the input values
    num_students = int(num_students_entry.get())
    student_scores = {}
    for i in range(num_students):
        name = student_entries[i][0].get()
        score = int(student_entries[i][1].get())
        student_scores[name] = score

    # Sort the dictionary by values (scores)
    sorted_scores = sorted(student_scores.items(),
                           key=lambda x: x[1], reverse=True)

    # Display the sorted results
    result_text.delete(1.0, tk.END)
    position = 1
    for i, (student, score) in enumerate(sorted_scores):
        if i > 0 and score < sorted_scores[i-1][1]:
            position = i+1
        result_text.insert(
            tk.END, "{}. {} - {} (position {})\n".format(position, student, score, i+1))


sort_button.config(command=sort_scores)
sort_button.pack(side=tk.TOP, pady=10)

# Create the output area
result_label = tk.Label(root, text="Results:")
result_label.pack(side=tk.TOP, pady=10)

result_frame = tk.Frame(root)
result_frame.pack(side=tk.TOP, fill="both", expand=True)

result_text = tk.Text(result_frame, wrap="word")
result_text.pack(side=tk.LEFT, fill="both", expand=True)

result_scrollbar = ttk.Scrollbar(
    result_frame, orient="vertical", command=result_text.yview)
result_scrollbar.pack(side=tk.RIGHT, fill="y")

result_text.configure(yscrollcommand=result_scrollbar.set)

root.mainloop()
