import csv
import time
import tkinter as tk
from tkinter import ttk, messagebox
from tqdm import tqdm 

# ---------- Sorting Algorithms ----------
def bubble_sort(data, key):
    start_time = time.time()
    n = len(data)
    for i in tqdm(range(n), desc="Bubble Sort Progress"):
        swapped = False
        for j in range(0, n - i - 1):
            if data[j][key] > data[j+1][key]:
                data[j], data[j+1] = data[j+1], data[j]
                swapped = True
        if not swapped:
            break
    return data, time.time() - start_time

def insertion_sort(data, key):
    start_time = time.time()
    for i in tqdm(range(1, len(data)), desc="Insertion Sort Progress"):
        current = data[i]
        j = i - 1
        while j >= 0 and data[j][key] > current[key]:
            data[j+1] = data[j]
            j -= 1
        data[j+1] = current
    return data, time.time() - start_time

def merge_sort(data, key):
    start_time = time.time()

    def _merge_sort(arr):
        if len(arr) <= 1:
            return arr
        mid = len(arr) // 2
        left = _merge_sort(arr[:mid])
        right = _merge_sort(arr[mid:])
        return merge(left, right)

    def merge(left, right):
        result = []
        i = j = 0
        while i < len(left) and j < len(right):
            if left[i][key] <= right[j][key]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        result.extend(left[i:])
        result.extend(right[j:])
        return result

    sorted_data = _merge_sort(data)
    return sorted_data, time.time() - start_time

# ---------- File Reading ----------
def read_csv(filename):
    start_time = time.time()
    with open(filename, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        data = []
        for row in reader:
            data.append({
                "ID": int(row["ID"]),
                "FirstName": row["FirstName"],
                "LastName": row["LastName"]
            })
    load_time = time.time() - start_time
    return data, load_time

# ---------- Console Mode ----------
def console_mode(data, load_time):
    while True:
        print("\nMENU OPTIONS")
        print("1. Bubble Sort")
        print("2. Insertion Sort")
        print("3. Merge Sort")
        print("4. Exit")

        choice = input("Enter your choice: ")

        if choice == '4':
            print("Exiting...")
            break

        if choice in ['1', '2', '3']:
            column = input("Choose column to sort by (ID / FirstName / LastName): ")
            if column not in ["ID", "FirstName", "LastName"]:
                print("Invalid column choice.")
                continue

            try:
                N = int(input("Enter number of rows to sort: "))
            except ValueError:
                print("Invalid number.")
                continue

            arr_to_sort = data[:N]

            if choice in ['1', '2'] and N > 10000:
                print("Warning: Sorting with O(n^2) may take a very long time!")

            if choice == '1':
                sorted_arr, sort_time = bubble_sort(arr_to_sort, column)
                method_name = "Bubble Sort"
            elif choice == '2':
                sorted_arr, sort_time = insertion_sort(arr_to_sort, column)
                method_name = "Insertion Sort"
            else:
                sorted_arr, sort_time = merge_sort(arr_to_sort, column)
                method_name = "Merge Sort"

            print(f"\n{method_name} Results (sorted by {column}):")
            for row in sorted_arr[:10]:
                print(row)
            print(f"Sort time: {sort_time:.6f} seconds")
            print(f"Total execution time (load + sort): {load_time + sort_time:.6f} seconds")

        else:
            print("Invalid choice. Please select 1, 2, 3 or 4.")

# ---------- GUI Mode ----------
def gui_mode(data, load_time):
    def run_sort():
        algo = algo_var.get()
        column = column_var.get()
        try:
            N = int(rows_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Rows must be an integer")
            return

        arr_to_sort = data[:N]

        if algo in ["Bubble", "Insertion"] and N > 10000:
            messagebox.showwarning("Warning", "O(n^2) sort may take a long time!")

        if algo == "Bubble":
            sorted_arr, sort_time = bubble_sort(arr_to_sort, column)
        elif algo == "Insertion":
            sorted_arr, sort_time = insertion_sort(arr_to_sort, column)
        else:
            sorted_arr, sort_time = merge_sort(arr_to_sort, column)

        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, f"{algo} Sort Results (by {column}):\n")
        for row in sorted_arr[:10]:
            output_text.insert(tk.END, f"{row}\n")
        output_text.insert(tk.END, f"\nSort time: {sort_time:.6f} seconds\n")
        output_text.insert(tk.END, f"Total execution time: {load_time + sort_time:.6f} seconds\n")

    root = tk.Tk()
    root.title("Sorting Benchmark Tool")

    algo_var = tk.StringVar(value="Merge")
    column_var = tk.StringVar(value="ID")

    ttk.Label(root, text="Algorithm:").grid(row=0, column=0)
    ttk.OptionMenu(root, algo_var, "Merge", "Bubble", "Insertion", "Merge").grid(row=0, column=1)

    ttk.Label(root, text="Column:").grid(row=1, column=0)
    ttk.OptionMenu(root, column_var, "ID", "ID", "FirstName", "LastName").grid(row=1, column=1)

    ttk.Label(root, text="Rows to sort:").grid(row=2, column=0)
    rows_entry = ttk.Entry(root)
    rows_entry.grid(row=2, column=1)

    ttk.Button(root, text="Run Sort", command=run_sort).grid(row=3, column=0, columnspan=2)

    output_text = tk.Text(root, width=60, height=20)
    output_text.grid(row=4, column=0, columnspan=2)

    root.mainloop()

# ---------- Entry Point ----------
if __name__ == "__main__":
    filename = "generated_data.csv"
    try:
        data, load_time = read_csv(filename)
        print(f"File loaded in {load_time:.6f} seconds. Total rows: {len(data)}")

        mode = input("Choose mode: 1) Console 2) GUI: ")
        if mode == '1':
            console_mode(data, load_time)
        else:
            gui_mode(data, load_time)

    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
    except ValueError as e:
        print(f"Error: {e}")

