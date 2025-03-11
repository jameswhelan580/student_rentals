from flask import Flask, render_template, request, session, redirect, url_for
import random

app = Flask(__name__)
app.secret_key = 'mysecretkey'  # Set a secret key for session management

# Company Details
COMPANY_NAME = "Sonas"
SLOGAN = "CREDIBLE HOMES, CONFIDENT FUTURE"
CONTACT_EMAIL = "Sonas@info.ie"

# Updated mock data for property listings with seller and testimonial details
properties = [
    {
        "id": 1,
        "title": "Modern Studio Apartment in Galway City Centre",
        "description": (
            "A cozy, modern studio for students, close to campus. "
            "This bright and airy apartment features floor-to-ceiling windows, "
            "high-speed internet, and on-site laundry facilities. "
            "Located in the heart of Galway, you'll be just steps away from cafés, shops, and nightlife."
        ),
        "bedrooms": 1,
        "bathrooms": 1,
        "area": 30,  # in square meters
        "furnished": "Fully furnished",
        "heating": "Electric",
        "parking": "On-street parking available",
        "pets": "No pets allowed",
        "smoking": "No smoking allowed",
        "lease": "12 months minimum",
        "deposit": "One month's rent",
        "utilities": "Electricity and internet included",
        "amenities": ["High-speed internet", "Laundry facilities", "Close to public transport"],
        "price": "€700/month",
        "image": "property1.jpg",
        "seller": "Galway Homes Realty",
        "seller_contact": "+353 1 234 5678",
        "testimonial": "I absolutely love my studio apartment. The service was amazing!",
        "testimonial_author": "Alice O'Connor"
    },
    {
        "id": 2,
        "title": "Spacious Two-Bedroom Apartment in Salthill",
        "description": (
            "A beautiful apartment with sweeping sea views. "
            "This two-bedroom gem boasts a large living room, two bathrooms, and a fully equipped kitchen. "
            "Enjoy morning walks on the promenade and easy access to local restaurants and pubs. "
            "Perfect for families or professionals seeking a tranquil coastal lifestyle."
        ),
        "bedrooms": 2,
        "bathrooms": 2,
        "area": 80,  # in square meters
        "furnished": "Partly furnished",
        "heating": "Gas",
        "parking": "Private parking available",
        "pets": "Pets allowed",
        "smoking": "No smoking allowed",
        "lease": "Flexible lease options",
        "deposit": "Two month's rent",
        "utilities": "Not included",
        "amenities": ["Sea views", "Fully equipped kitchen", "Private parking"],
        "price": "€1,200/month",
        "image": "property2.jpg",
        "seller": "Salthill Property Group",
        "seller_contact": "+353 1 345 6789",
        "testimonial": "The apartment's sea views are breathtaking, and the process was seamless.",
        "testimonial_author": "Brian Murphy"
    },
    {
        "id": 3,
        "title": "Cozy Shared House in Residential Galway",
        "description": (
            "A great shared home for students or young professionals. "
            "Featuring four bedrooms, a spacious common area, and a large backyard, "
            "this house offers a balance of privacy and community living. "
            "Conveniently located near bus routes, local shops, and parks, it's perfect for those looking for an affordable yet comfortable space."
        ),
        "bedrooms": 4,
        "bathrooms": 2,
        "area": 120,  # in square meters
        "furnished": "Partly furnished",
        "heating": "Oil",
        "parking": "Driveway parking available",
        "pets": "No pets allowed",
        "smoking": "No smoking allowed",
        "lease": "6 months minimum",
        "deposit": "One month's rent",
        "utilities": "Shared utilities",
        "amenities": ["Large backyard", "Close to public transport", "Nearby shops and parks"],
        "price": "€450 per person/month",
        "image": "property3.jpg",
        "seller": "Galway Shared Homes",
        "seller_contact": "+353 1 456 7890",
        "testimonial": "Our shared house exceeded expectations; it's both comfortable and affordable.",
        "testimonial_author": "Clara Doyle"
    }
]

# New blog posts data – 7 successful stories
blog_posts = [
    {
        "id": 1,
        "title": "From Renter to Homeowner: A Success Story",
        "content": "After years of renting, Sarah finally found her dream home with Sonas. The process was smooth and supportive every step of the way.",
        "author": "Sarah P.",
        "date": "2025-01-15"
    },
    {
        "id": 2,
        "title": "A Family's Journey to a New Beginning",
        "content": "The Jones family moved into a spacious home that perfectly suits their needs. Their new life in a friendly neighborhood has been transformative.",
        "author": "The Jones Family",
        "date": "2025-02-10"
    },
    {
        "id": 3,
        "title": "Investing in Dreams: A Young Professional’s Story",
        "content": "John, a young professional, invested in a modern apartment through Sonas. It was the best decision he ever made for his future.",
        "author": "John D.",
        "date": "2025-03-05"
    },
    {
        "id": 4,
        "title": "Finding the Perfect Rental: A Student Success Story",
        "content": "Emily, a university student, found an affordable yet modern studio apartment that suits her busy lifestyle perfectly.",
        "author": "Emily R.",
        "date": "2025-02-28"
    },
    {
        "id": 5,
        "title": "From Small Space to Grand Living",
        "content": "Michael expanded his living space with a two-bedroom apartment that offers both comfort and style, setting him up for success.",
        "author": "Michael S.",
        "date": "2025-01-22"
    },
    {
        "id": 6,
        "title": "Creating a Cozy Home in the City",
        "content": "Lisa transformed a modest apartment into a cozy retreat in the heart of the city, thanks to the dedicated team at Sonas.",
        "author": "Lisa K.",
        "date": "2025-03-12"
    },
    {
        "id": 7,
        "title": "Building a Future, One Brick at a Time",
        "content": "After years of hard work, David and his partner found a home that symbolized their journey and dreams. They are now thriving in their new space.",
        "author": "David & Partner",
        "date": "2025-02-05"
    }
]

@app.route('/')
def home():
    return render_template('index.html', company_name=COMPANY_NAME, slogan=SLOGAN)

@app.route('/enter-email', methods=['GET', 'POST'])
def enter_email():
    error = None
    if request.method == 'POST':
        email = request.form.get('email')
        if email:
            session['email'] = email
            session['verified'] = True  # Mark user as verified
            return redirect(url_for('list_properties'))
        else:
            error = "Please enter a valid university email."
    return render_template('enter_email.html', error=error, company_name=COMPANY_NAME)

@app.route('/properties')
def list_properties():
    if not session.get('verified'):
        return redirect(url_for('enter_email'))
    search_query = request.args.get('search', '').lower()
    if search_query:
        filtered_properties = [prop for prop in properties if search_query in prop["title"].lower()]
    else:
        filtered_properties = properties
    return render_template('properties.html', properties=filtered_properties, company_name=COMPANY_NAME)

@app.route('/property/<int:property_id>')
def property_detail(property_id):
    if not session.get('verified'):
        return redirect(url_for('enter_email'))
    property_item = next((prop for prop in properties if prop["id"] == property_id), None)
    if property_item:
        return render_template('property_detail.html', property=property_item, company_name=COMPANY_NAME)
    return "Property not found", 404

@app.route('/about')
def about():
    return render_template('about.html', company_name=COMPANY_NAME, slogan=SLOGAN)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        return render_template('contact.html', success=True, name=name, company_name=COMPANY_NAME, contact_email=CONTACT_EMAIL)
    return render_template('contact.html', success=False, company_name=COMPANY_NAME, contact_email=CONTACT_EMAIL)

# New Blog Route
@app.route('/blog')
def blog():
    return render_template('blog.html', company_name=COMPANY_NAME, blog_posts=blog_posts)

@app.route('/submit_request', methods=['POST'])
def submit_request():
    # Here you can handle the form data
    full_name = request.form['name']
    age = request.form['age']
    university_email = request.form['email']
    phone_number = request.form['phone']
    current_address = request.form['address']
    past_rental_reference = request.form['reference']
    cover_letter = request.form['cover_letter']

    # For example, print the submitted data (or save it to a database)
    print(f"Request submitted: {full_name}, {university_email}")

    # Redirect to a thank you page or the property details page
    return redirect(url_for('property_detail', property_id=request.args.get('property_id')))

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000, use_reloader=False)
