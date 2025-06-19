import psycopg2
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy







app = Flask(__name__)

# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname="Dbase",
    user="postgres",
    host="localhost",
    password= "password",
    port ="5432"
    )

# Create a cursor object
cur = conn.cursor()

# Create a cursor object










@app.route('/')
def index():
    return render_template('index2.html')

@app.route('/submits', methods=['POST' ])
def add_record():
    types = request.form['type']
    area = request.form['area']
    Yield = request.form['yield']
    date_planted = request.form['date_planted']
    location = request.form['location']
    

    cur.execute("""
        INSERT INTO fodder
                 (type, area, yield, date_planted,location)
        VALUES (%s, %s, %s, %s, %s)
    """, (types, area,Yield, date_planted,location))
    conn.commit()

    return redirect('/')


# Function for binary search (requires sorted records)
def binary_search(records, search_field_index, search_term):
    
    left = 0
    right = len(records) - 1
    found_records = []

    while left <= right:
        mid = (left + right) // 2
        mid_value = str(records[mid][search_field_index]).lower()  # Convert to lower case for case-insensitive comparison
        if search_term.lower() == mid_value:
            found_records.append(records[mid])
            # Check for other occurrences on the left side
            left_pointer = mid - 1
            while left_pointer >= left and str(records[left_pointer][search_field_index]).lower() == search_term.lower():
                found_records.append(records[left_pointer])
                left_pointer -= 1
            # Check for other occurrences on the right side
            right_pointer = mid + 1
            while right_pointer <= right and str(records[right_pointer][search_field_index]).lower() == search_term.lower():
                found_records.append(records[right_pointer])
                right_pointer += 1
            return found_records
        elif search_term.lower() < mid_value:
            right = mid - 1
        else:
            left = mid + 1

    return found_records


# Function for linear search
def linear_search(records, search_term):
    found_records = []
    for record in records:
        if search_term.lower() in [str(item).lower() for item in record]:
            found_records.append(record)
    return found_records


    

   



# Sorting algorithms
def bubble_sort(records, sorting_field_index, sorting_order):
    n = len(records)
    for i in range(n - 1):
        for j in range(n - i - 1):
            if sorting_order == "ASC":
                if records[j][sorting_field_index] > records[j + 1][sorting_field_index]:
                    records[j], records[j + 1] = records[j + 1], records[j]
            elif sorting_order == "DESC":
                if records[j][sorting_field_index] < records[j + 1][sorting_field_index]:
                    records[j], records[j + 1] = records[j + 1], records[j]

    return records


def insertion_sort(records, sorting_field_index, sorting_order):
    for i in range(1, len(records)):
        key = records[i]
        j = i - 1
        if sorting_order == "ASC":
            while j >= 0 and records[j][sorting_field_index] > key[sorting_field_index]:
                records[j + 1] = records[j]
                j -= 1
        elif sorting_order == "DESC":
            while j >= 0 and records[j][sorting_field_index] < key[sorting_field_index]:
                records[j + 1] = records[j]
                j -= 1
        records[j + 1] = key

    return records

def selection_sort(records, sorting_field_index, sorting_order):
    n = len(records)
    for i in range(n):
        min_index = i
        for j in range(i+1, n):
            if sorting_order == "ASC":
                if records[j][sorting_field_index] < records[min_index][sorting_field_index]:
                    min_index = j
            elif sorting_order == "DESC":
                if records[j][sorting_field_index] > records[min_index][sorting_field_index]:
                    min_index = j
        records[i], records[min_index] = records[min_index], records[i]
    return records

def merge_sort(records, sorting_field_index, sorting_order):
    if len(records) > 1:
        mid = len(records) // 2
        left_half = records[:mid]
        right_half = records[mid:]

        merge_sort(left_half, sorting_field_index, sorting_order)
        merge_sort(right_half, sorting_field_index, sorting_order)

        i = j = k = 0

        while i < len(left_half) and j < len(right_half):
            if (sorting_order == "ASC" and left_half[i][sorting_field_index] <= right_half[j][sorting_field_index]) or \
               (sorting_order == "DESC" and left_half[i][sorting_field_index] >= right_half[j][sorting_field_index]):
                records[k] = left_half[i]
                i += 1
            else:
                records[k] = right_half[j]
                j += 1
            k += 1

        while i < len(left_half):
            records[k] = left_half[i]
            i += 1
            k += 1

        while j < len(right_half):
            records[k] = right_half[j]
            j += 1
            k += 1

    return records


def quick_sort(records, sorting_field_index, sorting_order):
    def partition(low, high):
        pivot = records[high]
        i = low - 1

        for j in range(low, high):
            if (sorting_order == "ASC" and records[j][sorting_field_index] <= pivot[sorting_field_index]) or \
               (sorting_order == "DESC" and records[j][sorting_field_index] >= pivot[sorting_field_index]):
                i += 1
                records[i], records[j] = records[j], records[i]

        records[i + 1], records[high] = records[high], records[i + 1]
        return i + 1

    def quick_sort_recursive(low, high):
        if low < high:
            pi = partition(low, high)

            quick_sort_recursive(low, pi - 1)
            quick_sort_recursive(pi + 1, high)

    quick_sort_recursive(0, len(records) - 1)
    return records



# Function to get the index of the sorting field
def get_field_index(field_name):
    field_names = ["type", "area", "yield", "date_planted", "location"]
    try:
        return field_names.index(field_name)
    except ValueError:
        # Handle the case when the field name is not found
        print(f"Error: Sorting field '{field_name}' not found.")
        # Return a default value or raise an exception depending on your needs
        return -1  # Return -1 as a default index value
        



@app.route('/sort_records', methods=['POST'])
def sort_records():

    sorting_field = request.form['sort_by']
    sorting_algorithm = request.form['sort_algorithm']
    sorting_order = request.form['order']

    # Fetch records from the database
    query = f"SELECT * FROM Fodder"
    cur.execute(query)
    records = cur.fetchall()

    # Get the index of the sorting field
    field_index = get_field_index(sorting_field)
    if field_index == -1:  # Check if the sorting field is valid
        print("Invalid sorting field.")
        

    # Sort the records based on the selected sorting algorithm and field
    if sorting_algorithm == "bubble_sort":
        sorted_records = bubble_sort(records, field_index, sorting_order)
    elif sorting_algorithm == "insertion_sort":
        sorted_records = insertion_sort(records, field_index, sorting_order)
    elif sorting_algorithm == "selection_sort":
        sorted_records = selection_sort(records, field_index, sorting_order)   
    elif sorting_algorithm == "merge_sort":
        sorted_records = merge_sort(records, field_index, sorting_order)  
    elif sorting_algorithm == "quick_sort":
        sorted_records = quick_sort(records, field_index, sorting_order)         
    else:
        sorted_records = records

    return render_template('records2.html' ,records=sorted_records)  # Return sorted records template


           
    

@app.route('/search_records', methods=['POST'])
def search_records():
    search_algorithm = request.form['search_algorithm']
    search_term = request.form['search_term']

    if not search_term:
        print("Please enter a search term.")
        return redirect('/')

    # Fetch records from the database
    query = "SELECT * FROM Fodder"
    cur.execute(query)
    records = cur.fetchall()

    if search_algorithm == "linear_search":
        # Perform linear search on unsorted records
        search_results = linear_search(records, search_term)
    elif search_algorithm == "binary_search":
        # Perform binary search
        search_results = linear_search(records, search_term)
    else:
        print("Invalid search algorithm selected.")
        return redirect('/')
    
    return render_template('records2.html', records=search_results)

if __name__ == '__main__':
    app.run(debug=True)
