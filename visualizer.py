import tkinter as tk
import random

# ----------- Sorting Algorithms as Generators -----------

def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(n - 1 - i):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
            yield arr

def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
            yield arr
        arr[j + 1] = key
        yield arr

def selection_sort(arr):
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
            yield arr
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
        yield arr

def merge_sort(arr, l=0, r=None):
    if r is None:
        r = len(arr) - 1

    if l >= r:
        return

    mid = (l + r) // 2
    yield from merge_sort(arr, l, mid)
    yield from merge_sort(arr, mid + 1, r)

    # Merge step
    left = arr[l:mid + 1]
    right = arr[mid + 1:r + 1]
    i = j = 0
    k = l

    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            arr[k] = left[i]
            i += 1
        else:
            arr[k] = right[j]
            j += 1
        k += 1
        yield arr

    while i < len(left):
        arr[k] = left[i]
        i += 1
        k += 1
        yield arr

    while j < len(right):
        arr[k] = right[j]
        j += 1
        k += 1
        yield arr

def quick_sort(arr, l=0, r=None):
    if r is None:
        r = len(arr) - 1

    def partition(low, high):
        pivot = arr[high]
        i = low
        for j in range(low, high):
            if arr[j] < pivot:
                arr[i], arr[j] = arr[j], arr[i]
                yield arr
                i += 1
        arr[i], arr[high] = arr[high], arr[i]
        yield arr
        return i

    if l < r:
        p = yield from partition(l, r)
        yield from quick_sort(arr, l, p - 1)
        yield from quick_sort(arr, p + 1, r)

# ----------- Main Visualizer Class -----------

class SortingVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Sorting Algorithm Visualizer")
        self.root.config(bg="#1e1e2f")

        # Canvas
        self.canvas = tk.Canvas(root, width=800, height=400, bg="#1e1e2f", highlightthickness=0)
        self.canvas.pack(pady=20)

        # Controls
        control_frame = tk.Frame(root, bg="#1e1e2f")
        control_frame.pack()

        tk.Label(control_frame, text="Algorithm:", fg="white", bg="#1e1e2f").grid(row=0, column=0, padx=5)
        self.algo_choice = tk.StringVar(value="Bubble Sort")
        tk.OptionMenu(control_frame, self.algo_choice,
                      "Bubble Sort", "Insertion Sort", "Selection Sort",
                      "Merge Sort", "Quick Sort").grid(row=0, column=1, padx=5)

        tk.Button(control_frame, text="Generate Array", command=self.generate_array, bg="#4cafef", fg="white").grid(row=0, column=2, padx=5)
        tk.Button(control_frame, text="Start Sorting", command=self.start_sorting, bg="#4caf50", fg="white").grid(row=0, column=3, padx=5)

        # Variables
        self.array = []
        self.generator = None

        self.generate_array()

    def generate_array(self):
        self.array = [random.randint(10, 390) for _ in range(50)]
        self.draw_array(self.array)

    def draw_array(self, arr, color="cyan"):
        self.canvas.delete("all")
        bar_width = 800 / len(arr)
        for i, val in enumerate(arr):
            x0 = i * bar_width
            y0 = 400 - val
            x1 = (i + 1) * bar_width
            y1 = 400
            self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="")
        self.root.update_idletasks()

    def start_sorting(self):
        algo = self.algo_choice.get()
        if algo == "Bubble Sort":
            self.generator = bubble_sort(self.array)
        elif algo == "Insertion Sort":
            self.generator = insertion_sort(self.array)
        elif algo == "Selection Sort":
            self.generator = selection_sort(self.array)
        elif algo == "Merge Sort":
            self.generator = merge_sort(self.array)
        elif algo == "Quick Sort":
            self.generator = quick_sort(self.array)
        self.animate()

    def animate(self):
        try:
            arr = next(self.generator)
            self.draw_array(arr, color="orange")
            self.root.after(50, self.animate)  # Adjust speed here
        except StopIteration:
            self.draw_array(self.array, color="lime")  # Sorted array in green

# ----------- Run Program -----------

if __name__ == "__main__":
    root = tk.Tk()
    app = SortingVisualizer(root)
    root.mainloop()
