from flask import Flask, request, jsonify, render_template, redirect, url_for
import pandas as pd

app = Flask(__name__)

def load_feedback_data():
    try:
        # Load the CSV data into a DataFrame
        df = pd.read_csv('employee_feedback.csv')
        return df
    except FileNotFoundError:
        print("CSV file not found.")
        return pd.DataFrame(columns=['subject', 'level', 'job_title', 'function_code', 'question1', 'question2', 'question3', 'question4'])

df = load_feedback_data()

@app.route('/')
def index():
    
    return render_template('index.html')

@app.route('/employees', methods=['GET'])
def get_employees():
    feedbacks = load_feedback_data()
    employees = feedbacks['subject'].unique().tolist()
    return jsonify({'employees': employees})

@app.route('/employee_details/<employee_name>', methods=['GET'])
def get_employee_details(employee_name):
    feedbacks = load_feedback_data()
    employee_details = feedbacks[feedbacks['subject'] == employee_name].iloc[0]  # Get first occurrence of employee
    details = {
        'name': employee_details['subject'],
        'level': employee_details['level'],
        'function_code': employee_details['function_code'],
        'job_title': employee_details['job_title']
    }
    return jsonify(details)

@app.route('/feedback/<employee_name>', methods=['GET'])
def get_feedback(employee_name):
    # feedbacks = load_feedback_data()
    employee_feedbacks = df[df['subject'] == employee_name].to_dict(orient='records')
    return jsonify({'feedbacks': employee_feedbacks})


@app.route('/add_feedback', methods=['POST'])
def add_feedback():
    global df

    new_feedback = {
        'subject': request.form['employee_name'],
        'level': request.form['level'],
        'job_title': request.form['job_title'],
        'function_code': request.form['function_code'],
        'question1': request.form['question1'],
        'question2': request.form['question2'],
        'question3': request.form['question3'],
        'question4': request.form['question4']
    }
    new_feedback_df = pd.DataFrame([new_feedback])
    df = pd.concat([df, new_feedback_df], ignore_index=True)

    df.to_csv('employee_feedback.csv', index=False)
    load_feedback_data()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)