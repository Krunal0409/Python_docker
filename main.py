from flask import Flask, jsonify, request, render_template_string
import MySQLdb
from MySQLdb import cursors

app = Flask(__name__)

# MySQL configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'K1R2N@!kolhe'
app.config['MYSQL_DB'] = 'krunal'

@app.route('/')
def hello():
    return "Successfully made Docker image! :-) We can do anything now hurray!!!!!"

@app.route('/health')
def health():
    return {"status": "healthy"}, 200

# Display form and list users
@app.route('/users', methods=['GET', 'POST'])
def users():
    if request.method == 'POST':
        # Get form data
        name = request.form.get('name')
        email = request.form.get('email')
        
        try:
            conn = MySQLdb.connect(
                host=app.config['MYSQL_HOST'],
                user=app.config['MYSQL_USER'],
                passwd=app.config['MYSQL_PASSWORD'],
                db=app.config['MYSQL_DB']
            )
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (name, email) VALUES (%s, %s)", (name, email))
            conn.commit()
            cursor.close()
            conn.close()
            message = f"✓ User '{name}' added successfully!"
        except Exception as e:
            message = f"✗ Error: {str(e)}"
    else:
        message = ""
    
    # Fetch all users
    try:
        conn = MySQLdb.connect(
            host=app.config['MYSQL_HOST'],
            user=app.config['MYSQL_USER'],
            passwd=app.config['MYSQL_PASSWORD'],
            db=app.config['MYSQL_DB']
        )
        cursor = conn.cursor(cursors.DictCursor)
        cursor.execute("SELECT * FROM users")
        users_list = cursor.fetchall()
        cursor.close()
        conn.close()
    except Exception as e:
        users_list = []
        message = f"Error fetching users: {str(e)}"
    
    # HTML form
    html = f"""
    <style>
        body {{ font-family: Arial; margin: 20px; }}
        form {{ margin: 20px 0; padding: 20px; background: #f0f0f0; border-radius: 5px; }}
        input {{ padding: 8px; margin: 5px 0; width: 300px; }}
        button {{ padding: 10px 20px; background: #4CAF50; color: white; border: none; cursor: pointer; }}
        button:hover {{ background: #45a049; }}
        table {{ border-collapse: collapse; margin-top: 20px; }}
        th, td {{ border: 1px solid #ddd; padding: 10px; text-align: left; }}
        th {{ background-color: #4CAF50; color: white; }}
        .message {{ padding: 10px; margin: 10px 0; background: #e8f5e9; border-left: 4px solid #4CAF50; }}
    </style>
    
    <h1>User Management</h1>
    
    {f'<div class="message">{message}</div>' if message else ''}
    
    <form method="POST">
        <h2>Add New User</h2>
        <label>Name:</label><br>
        <input type="text" name="name" required><br>
        <label>Email:</label><br>
        <input type="email" name="email" required><br>
        <button type="submit">Add User</button>
    </form>
    
    <h2>All Users</h2>
    <table>
        <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Email</th>
        </tr>
    """
    
    for user in users_list:
        html += f"<tr><td>{user.get('id', 'N/A')}</td><td>{user.get('name', 'N/A')}</td><td>{user.get('email', 'N/A')}</td></tr>"
    
    html += "</table>"
    
    return render_template_string(html)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)