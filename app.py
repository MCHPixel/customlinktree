from flask import Flask, render_template, request, redirect, url_for
import os
import json

app = Flask(__name__)

# Function to load user-specific data
def load_user_data(username):
    user_file_path = f'users/{username}.json'
    if os.path.exists(user_file_path):
        with open(user_file_path) as f:
            return json.load(f)
    else:
        # Return default profile if user doesn't exist
        return {
            "name": username,
            "bio": "This user does not have a custom bio yet.",
            "links": [],
            "bg_color_start": "#ffffff",  # Default white
            "bg_color_end": "#000000"    # Default black
        }

# Function to list all available users by reading from 'users/' directory
def get_all_users():
    user_files = os.listdir('users/')
    return [file.replace('.json', '') for file in user_files if file.endswith('.json')]

@app.route('/')
def home():
    # List all users as clickable links
    users = get_all_users()
    return render_template('users.html', users=users)

@app.route('/<username>')
def user_profile(username):
    # Load user data based on username
    user_data = load_user_data(username)
    return render_template('profile.html',
                           username=user_data['name'],
                           bio=user_data['bio'],
                           links=user_data['links'],
                           bg_color_start=user_data['bg_color_start'],
                           bg_color_end=user_data['bg_color_end'])

# Route to display the profile creation form
@app.route('/create_profile', methods=['GET', 'POST'])
def create_profile():
    if request.method == 'POST':
        # Get form data
        username = request.form['username']
        bio = request.form['bio']
        color1 = request.form['color1']
        color2 = request.form['color2']
        links = json.loads(request.form['links'])

        # Save profile data to JSON
        user_data = {
            'name': username,
            'bio': bio,
            'links': links,
            'bg_color_start': color1,
            'bg_color_end': color2
        }

        # Write user data to a JSON file in 'users/' directory
        user_file_path = f'users/{username}.json'
        with open(user_file_path, 'w') as f:
            json.dump(user_data, f, indent=4)

        return redirect(url_for('user_profile', username=username))

    # Display the profile creation form (GET request)
    return render_template('profile_creator.html')

@app.route('/preview')
def preview():
    # Get the query parameters (default values are provided if missing)
    username = request.args.get('username', 'Default User')
    bio = request.args.get('bio', 'This is a bio preview...')
    bg_color_start = request.args.get('bg_color_start', '#3D3D3D')  # Default to white
    bg_color_end = request.args.get('bg_color_end', '#000000')      # Default to black
    links_json = request.args.get('links', '[]')  # Expecting a JSON string

    # Convert links JSON string into a Python list
    links = json.loads(links_json)

    # Render the template with the dynamic content
    return render_template('profile_preview.html',
                           username=username,
                           bio=bio,
                           bg_color_start=bg_color_start,
                           bg_color_end=bg_color_end,
                           links=links)

@app.route('/gradient_preview')
def gradient_preview():
    # Get the query parameters for background colors, default to black and white
    bg_start = request.args.get('bg_start', '#000000')  # Default start color
    bg_end = request.args.get('bg_end', '#ffffff')      # Default end color
    return render_template('gradient_preview.html', bg_start=bg_start, bg_end=bg_end)

if __name__ == '__main__':
    app.run(debug=True)
