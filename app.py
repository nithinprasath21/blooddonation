from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# MySQL Configuration
db_config = {
    'host':'localhost',
    'user': 'root',
    'password': '',
    'database': 'blooddonation'
}

# Create a MySQL connection
conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()

# Create Blood Donation table if not exists
cursor.execute('''
    CREATE TABLE IF NOT EXISTS donations (
        id INT AUTO_INCREMENT PRIMARY KEY,
        donor_name VARCHAR(255) NOT NULL,
        blood_group VARCHAR(10) NOT NULL,
        contact_number VARCHAR(15) NOT NULL
    )
''')
conn.commit()

# Route to update donation record
@app.route('/update/<int:donation_id>', methods=['GET', 'POST'])
def update(donation_id):
    if request.method == 'GET':
        # Retrieve donation details for the selected ID
        cursor.execute('SELECT * FROM donations WHERE id = %s', (donation_id,))
        donation = cursor.fetchone()
        return render_template('update.html', donation=donation)
    elif request.method == 'POST':
        # Update donation details in the database
        donor_name = request.form['donor_name']
        blood_group = request.form['blood_group']
        contact_number = request.form['contact_number']

        cursor.execute('''
            UPDATE donations
            SET donor_name = %s, blood_group = %s, contact_number = %s
            WHERE id = %s
        ''', (donor_name, blood_group, contact_number, donation_id))
        conn.commit()

        return redirect(url_for('request_blood'))

# Route to delete donation record
@app.route('/delete/<int:donation_id>')
def delete(donation_id):
    # Delete donation record from the database
    cursor.execute('DELETE FROM donations WHERE id = %s', (donation_id,))
    conn.commit()

    return redirect(url_for('request_blood'))


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/donate', methods=['POST'])
def donate():
    donor_name = request.form['donor_name']
    blood_group = request.form['blood_group']
    contact_number = request.form['contact_number']

    # Insert donation details into the database
    cursor.execute('''
        INSERT INTO donations (donor_name, blood_group, contact_number)
        VALUES (%s, %s, %s)
    ''', (donor_name, blood_group, contact_number))
    conn.commit()

    return redirect(url_for('index'))

@app.route('/request')
def request_blood():
    # Retrieve donation details from the database
    cursor.execute('SELECT * FROM donations')
    donations = cursor.fetchall()

    return render_template('request.html', donations=donations)

if __name__ == '__main__':
    app.run(debug=True)
