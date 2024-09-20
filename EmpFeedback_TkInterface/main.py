import tkinter as tk
from tkinter import ttk
import pandas as pd

# Reading data from CSV file
def load_data():
    try:
        # Loading the CSV data into a DataFrame
        df = pd.read_csv('./employee_feedback.csv')
        return df
    except FileNotFoundError:
        print("CSV file not found.")
        return None

# Display feedback for the selected employee
def show_feedback(event):
    selected_employee = employee_listbox.get(employee_listbox.curselection())
    feedback_data = df[df['employee_name'] == selected_employee]
    feedback_text.delete(1.0, tk.END)  # Clearing previous text
    if not feedback_data.empty:
        for index, feedback_details in feedback_data.iterrows():
            feedback_text.insert(tk.END, f"Feedback by: {feedback_details['feedback_given_by']}\n")
            feedback_text.insert(tk.END, f"Feedback: {feedback_details['feedback']}\n")
            feedback_text.insert(tk.END, "-"*70 + "\n")
    else:
        feedback_text.insert(tk.END, "No feedback available.")

# The main application window
def create_ui():
    global employee_listbox, feedback_text, df

    # Loading the data
    df = load_data()
    if df is None:
        return

    # Create the main window
    root = tk.Tk()
    root.title("Employee Feedback Viewer")
    root.geometry('700x500')

    # Create the employee list label
    list_label = ttk.Label(root, text="Select an Employee:")
    list_label.pack(pady=5)

    # Create a Listbox to display employee names
    employee_listbox = tk.Listbox(root, height=10)
    employee_listbox.pack(pady=5, padx=10, fill=tk.BOTH, expand=True)

    # Populate the Listbox with employee names
    for name in df['employee_name'].unique():
        employee_listbox.insert(tk.END, name)

    # Bind the selection event to display feedback
    employee_listbox.bind('<<ListboxSelect>>', show_feedback)

    # Create a Text widget to display feedback details
    feedback_text = tk.Text(root, height=10, wrap=tk.WORD)
    feedback_text.pack(pady=5, padx=10, fill=tk.BOTH, expand=True)

    # Start the main loop
    root.mainloop()

# Entry point of the application
if __name__ == "__main__":
    create_ui()















# from flask import Flask, render_template, request, jsonify, redirect, url_for
# from urllib.parse import unquote
# import pandas as pd

# app = Flask(__name__)

# # Read data from CSV file
# def load_data():
#     try:
#         # Load the CSV data into a DataFrame
#         df = pd.read_csv('employee_feedback.csv')
#         return df
#     except FileNotFoundError:
#         print("CSV file not found.")
#         return pd.DataFrame(columns=['employee_name', 'feedback_given_by', 'feedback'])

# df = load_data()

# @app.route('/')
# def index():
#     if not df.empty:
#         employees = df['employee_name'].unique()
#     else:
#         employees = []
#     return render_template('index.html', employees=employees)

# @app.route('/feedback/<employee>', methods=['GET'])
# def feedback(employee):
#     employee = unquote(employee)
#     feedback_data = df[df['employee_name'] == employee]
#     feedbacks = []
#     if not feedback_data.empty:
#         for index, feedback_details in feedback_data.iterrows():
#             feedbacks.append({
#                 'given_by': feedback_details['feedback_given_by'],
#                 'feedback': feedback_details['feedback']
#             })
#     return jsonify({'feedbacks': feedbacks})

# @app.route('/add_feedback', methods=['POST'])
# def add_feedback():
#     global df
#     employee_name = request.form['employee_name']
#     feedback_given_by = request.form['feedback_given_by']
#     feedback = request.form['feedback']

#     new_feedback = pd.DataFrame({
#         'employee_name': [employee_name],
#         'feedback_given_by': [feedback_given_by],
#         'feedback': [feedback]
#     })

#     df = pd.concat([df, new_feedback], ignore_index=True)

#     df.to_csv('employee_feedback.csv', index=False)

#     return redirect(url_for('index'))

# if __name__ == '__main__':
#     app.run(debug=True)
