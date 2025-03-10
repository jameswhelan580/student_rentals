from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = 'mysecretkey'  # Set a secret key for session management

# Updated mock data for property listings with images (assume images are in static/images/)
properties = [
    {
        "id": 1,
        "title": "Modern Studio Apartment in Galway City Centre",
        "description": "A cozy, modern studio for students, close to campus.",
        "price": "€700/month",
        "image": "property1.jpg"  # Ensure this matches an actual file
    },
    {
        "id": 2,
        "title": "Spacious Two-Bedroom Apartment in Salthill",
        "description": "A beautiful apartment with sea views.",
        "price": "€1,200/month",
        "image": "property2.jpg"
    },
    {
        "id": 3,
        "title": "Cozy Shared House in Residential Galway",
        "description": "A great shared home for students.",
        "price": "€450 per person/month",
        "image": "property3.jpg"
    }
]

@app.route('/')
def home():
    return render_template('index.html')

# NEW: Route for entering the university email
@app.route('/enter-email', methods=['GET', 'POST'])
def enter_email():
    if request.method == 'POST':
        email = request.form.get('email')
        if email:
            session['email'] = email  # Save the email in the session
            return redirect(url_for('list_properties'))
        else:
            error = "Please enter a valid university email."
            return render_template('enter_email.html', error=error)
    return render_template('enter_email.html')

# UPDATED: Properties route now requires university email verification
@app.route('/properties')
def list_properties():
    if 'email' not in session:
        return redirect(url_for('enter_email'))
    search_query = request.args.get('search', '').lower()
    if search_query:
        filtered_properties = [prop for prop in properties if search_query in prop["title"].lower()]
    else:
        filtered_properties = properties
    return render_template('properties.html', properties=filtered_properties)

# UPDATED: Property detail route now requires university email verification
@app.route('/property/<int:property_id>')
def property_detail(property_id):
    if 'email' not in session:
        return redirect(url_for('enter_email'))
    property_item = next((prop for prop in properties if prop["id"] == property_id), None)
    if property_item:
        return render_template('property_detail.html', property=property_item)
    return "Property not found", 404

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        # Retrieve data from the form
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        # Here you could process the data, e.g., send an email or save it.
        # For now, we'll simply return a success message.
        return render_template('contact.html', success=True, name=name)
    return render_template('contact.html', success=False)

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000, use_reloader=False)