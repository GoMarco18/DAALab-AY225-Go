import time

def bubble_sort_descending(arr):
    """
    Sorts an array using the bubble sort algorithm in descending order.

    Args:
        arr: List of comparable elements to sort

    Returns:
        Tuple of (sorted list, time taken in seconds)
    """
    start_time = time.time()
    n = len(arr)

    for i in range(n):
        swapped = False

        for j in range(0, n - i - 1):
            # Change comparison for descending order
            if arr[j] < arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True

        if not swapped:
            break

    end_time = time.time()
    time_taken = end_time - start_time

    return arr, time_taken


def insertion_sort_descending(arr):
    """
    Sorts an array using the insertion sort algorithm in descending order.
    """
    start_time = time.time()
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and key > arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    end_time = time.time()
    return arr, end_time - start_time


def merge_sort_descending(arr):
    """
    Sorts an array using the merge sort algorithm in descending order.
    """
    start_time = time.time()
    
    def _merge_sort(a):
        if len(a) > 1:
            mid = len(a) // 2
            L = a[:mid]
            R = a[mid:]

            _merge_sort(L)
            _merge_sort(R)

            i = j = k = 0

            while i < len(L) and j < len(R):
                if L[i] > R[j]:
                    a[k] = L[i]
                    i += 1
                else:
                    a[k] = R[j]
                    j += 1
                k += 1

            while i < len(L):
                a[k] = L[i]
                i += 1
                k += 1

            while j < len(R):
                a[k] = R[j]
                j += 1
                k += 1
        return a

    _merge_sort(arr)
    end_time = time.time()
    return arr, end_time - start_time


def read_numbers_from_txt(filename):
    """
    Reads numbers from a text file and returns them as a list.
    """
    with open(filename, "r") as file:
        data = file.read().split()
        return [int(num) for num in data]


# Example usage
if __name__ == "__main__":
    # TXT file input
    filename = "dataset.txt"

    try:
        data = read_numbers_from_txt(filename)
        
        while True:
            print("\nMENU DRIVEN OPTIONS FOR...")
            print("1. BUBBLE SORT")
            print("2. INSERTION SORT")
            print("3. MERGE SORT")
            print("4. EXIT")
            
            choice = input("\nEnter your choice: ")
            
            if choice == '4':
                print("Exiting...")
                break
            
            if choice in ['1', '2', '3']:
                # Sort a copy of the data
                arr_to_sort = data.copy()
                
                # print(f"Sorting {len(arr_to_sort)} items...") 
                
                if choice == '1':
                    sorted_arr, time_taken = bubble_sort_descending(arr_to_sort)
                    method_name = "Bubble Sort"
                elif choice == '2':
                    sorted_arr, time_taken = insertion_sort_descending(arr_to_sort)
                    method_name = "Insertion Sort"
                elif choice == '3':
                    sorted_arr, time_taken = merge_sort_descending(arr_to_sort)
                    method_name = "Merge Sort"
                
                print(f"\n{method_name} Results:")
                print(f"Sorted Data (Descending Order): {sorted_arr}")
                print(f"Time spent: {time_taken:.6f} seconds")
            else:
                print("Invalid choice. Please select 1, 2, 3 or 4.")

    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
    except ValueError:
        print("Error: The text file must contain only numbers.")
