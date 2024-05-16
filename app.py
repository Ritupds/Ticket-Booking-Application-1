
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.sqlite3"

db = SQLAlchemy(app)

from datetime import datetime

#creating tables

#user table
class User(db.Model):
    user_id = db.Column(db.Integer, primary_key = True)
    user_name = db.Column(db.String, nullable = False)
    user_email = db.Column(db.String, nullable = False)
    user_password = db.Column(db.String, nullable = False)
    
    def __init__(self,user_name,user_email,user_password):
        self.user_email=user_email
        self.user_name=user_name
        self.user_password=user_password

#admin table

class Admin(db.Model):
    admin_id = db.Column(db.Integer, primary_key = True)
    admin_username = db.Column(db.String, nullable = False)
    admin_password = db.Column(db.String, nullable = False)

    def __init__(self,admin_username,admin_password):
        self.admin_username=admin_username
        self.admin_password=admin_password

#venue table

class Venue(db.Model):
    venue_id = db.Column(db.Integer, primary_key = True)
    venue_name = db.Column(db.String, nullable = False)
    venue_place = db.Column(db.String, nullable = False)
    venue_city = db.Column(db.String, nullable = False)
    venue_capacity = db.Column(db.Integer, nullable = False)
    shows = db.relationship("Show", secondary="association")

    def __init__(self,venue_name,venue_place,venue_city,venue_capacity):
        self.venue_name=venue_name
        self.venue_place=venue_place
        self.venue_city=venue_city
        self.venue_capacity=venue_capacity

#show table
    
class Show(db.Model):
    show_id = db.Column(db.Integer, primary_key = True)
    show_name = db.Column(db.String, nullable = False)
   
    show_genre = db.Column(db.String, nullable = False)
    show_rating = db.Column(db.Integer, nullable = False)
    show_price = db.Column(db.Integer, nullable = False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey('venue.venue_id'), nullable=False)
    available_seats = db.Column(db.Integer, default=0, nullable=False)

    
    def __init__(self,show_name,show_genre,show_rating,show_price,venue_id,start_time,end_time,available_seats):
       
        self.show_name=show_name
        self.venue_id=venue_id
        self.start_time=start_time
        self.end_time=end_time
        self.show_genre=show_genre
        self.show_rating=show_rating
        self.show_price=show_price
        self.available_seats=available_seats

#association table

class Association(db.Model):
    venue_id = db.Column(db.Integer, db.ForeignKey("venue.venue_id"), primary_key=True)
    show_id = db.Column(db.Integer, db.ForeignKey("show.show_id"), primary_key=True)

    def __init__(self,venue_id,show_id):
        self.venue_id=venue_id
        self.show_id=show_id

#booking table

class Booking(db.Model):
    booking_id = db.Column(db.Integer, primary_key = True)
    venue_id = db.Column(db.Integer, db.ForeignKey("venue.venue_id"), nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"), nullable = False)
    show_id = db.Column(db.Integer, db.ForeignKey("show.show_id"), nullable = False)
    date = db.Column(db.Date, nullable = False)
    number_of_seats = db.Column(db.Integer, nullable=False)
        
    def __init__(self,date,number_of_seats,user_id,show_id,venue_id):
        self.user_id=user_id
        self.date = date
        self.number_of_seats=number_of_seats
        self.show_id=show_id
        self.venue_id=venue_id

#rating table

class Rating(db.Model):
    rating_id = db.Column(db.Integer, primary_key = True)
    venue_id = db.Column(db.Integer, db.ForeignKey("venue.venue_id"), nullable = False)
    show_id = db.Column(db.Integer, db.ForeignKey("show.show_id"), nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"), nullable = False)
    rating = db.Column(db.Integer)


    def __init__(self,venue_id,show_id,user_id,rating):
        self.venue_id=venue_id
        self.user_id=user_id
        self.show_id=show_id
        self.rating=rating
       

  
app.secret_key = 'adminsecretkey'
app.app_context().push()
db.create_all()


#creating admin login credential

def add_admin_if_not_existed():
    if db.session.query(Admin).count() == 0:
        admin=Admin(admin_username="ritu.parna", admin_password="ritu1098")
        db.session.add(admin)
        db.session.commit()

add_admin_if_not_existed()

#adding user
def add_user_if_not_existed():
    if db.session.query(User).count() == 0:
        u1=User(user_name="Radhika R",user_email="12345678@gmail.com",user_password=123456)
        u2=User(user_name="Pritam D",user_email="prtm@gmail.com",user_password=1209876)
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()

add_user_if_not_existed()


#landing page is admin login page....

@app.route('/')
def landing_page(): 
    return render_template('landing_page.html')

@app.route('/admin_dashboard')
def admin_dashboard():
    admin = Admin.query.all()
    all = Venue.query.all()
    return render_template('admin_dashboard.html',admin=admin, all=all)


@app.route('/admin/login', methods = ['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        admin_username = request.form['admin_username']
        admin_password = request.form['admin_password']
        if admin_username == 'ritu.parna' and admin_password == 'ritu1098':

            return redirect('/admin_dashboard')
        else:
            error = "INVALID USERNAME OR PASSWORD"

       
    return render_template('admin_login.html')


@app.route('/add_venues', methods = ['GET', 'POST']) 
def add_venues():
    if request.method == 'POST':
        venue_name = request.form['venue_name']
        venue_place = request.form['venue_place']
        venue_city = request.form['venue_city']
        venue_capacity = request.form['venue_capacity']

        new_venue = Venue(venue_name=venue_name, venue_place=venue_place, venue_city=venue_city, venue_capacity=venue_capacity)
        db.session.add(new_venue)
        db.session.commit()
        return redirect('/admin_dashboard')
    
    return render_template('add_venues.html')

@app.route('/view_venues')
def view_venues():
    all = Venue.query.all()
    return render_template("view_venues.html", all = all)


# #editing an existing venue 
 
@app.route('/edit_venue/<int:venue_id>', methods=['GET', 'POST'])
def edit_venue(venue_id):
    venue = Venue.query.get(venue_id)

    if request.method == 'POST':
        venue.venue_name = request.form['venue_name']
        venue.venue_place = request.form['venue_place']
        venue.venue_city = request.form['venue_city']
        venue.venue_capacity = request.form['venue_capacity']

        db.session.commit()
        return redirect('/admin_dashboard')

    return render_template('edit_venue.html', venue=venue)

  
#remove a venue

@app.route('/remove_venue/<int:venue_id>', methods=['GET', 'POST'])
def remove_venue(venue_id):
    remove_venue = Venue.query.get(venue_id)
    if not remove_venue:
        return redirect('/admin_dashboard')

    db.session.delete(remove_venue)
    db.session.commit()

    

    return redirect('/admin_dashboard')
    
    
#add show

@app.route('/add_shows', methods = ['GET', 'POST'])
def add_shows():
    if request.method == 'POST':
        show_name = request.form['show_name']
        show_rating = request.form['show_rating']
        start_time = datetime.strptime(request.form['start_time'], '%H:%M').time()
        end_time = datetime.strptime(request.form['end_time'], '%H:%M').time()
        show_genre = request.form['show_genre']
        show_price = request.form['show_price']
        venue_id = request.form['venue_id']
        available_seats = request.form['available_seats']

        venue = Venue.query.get(venue_id)
        
        new_show = Show(show_name=show_name, show_rating=show_rating, show_genre=show_genre, show_price=show_price, venue_id=venue_id,start_time=start_time,end_time=end_time,available_seats=available_seats)
       
        db.session.add(new_show)
        venue.shows.append(new_show)
        db.session.commit()

        return redirect('/admin_dashboard')
    
    venues = Venue.query.all()
    return render_template('add_shows.html', venues = venues)

#update show

@app.route('/show/<int:show_id>/update', methods=['GET', 'POST'])
def update_show(show_id):
    show = Show.query.get(show_id)
    available_seats= show.available_seats
   
    if request.method == 'POST':
        show_name = request.form['show_name']
        show_rating = request.form['show_rating']
        start_time = datetime.strptime(request.form['start_time'], '%H:%M').time()
        end_time = datetime.strptime(request.form['end_time'], '%H:%M').time()
        show_genre = request.form['show_genre']
        show_genre = request.form['show_genre']
        show_price = request.form['show_price']
        venue_id = request.form['venue_id']
        available_seats = request.form['available_seats']

        
        show.show_name = show_name
        show.show_rating = show_rating
        show.show_genre = show_genre
        show.show_price = show_price
        show.start_time = start_time
        show.end_time = end_time
        show.available_seats = request.form['available_seats']

        venues = Venue.query.get(venue_id)
        venues.shows.append(show)
        db.session.commit()

        return redirect('/admin_dashboard')
    venues = Venue.query.all()
    return render_template('edit_show.html', show=show, venues = venues,available_seats=available_seats)
    
print("Show added successfully")

#remove a show

@app.route('/remove_show/<int:show_id>', methods=['GET', 'POST'])
def remove_show(show_id):
    remove_show = Show.query.get(show_id)
    if not remove_show:
        return redirect('/admin_dashboard')

    db.session.delete(remove_show)
    db.session.commit()  

    return redirect('/admin_dashboard')


@app.route('/view_shows')
def view_shows():
    all = Show.query.all()
    return render_template("view_shows.html", all = all)

#admin logout 
@app.route('/admin_logout')
def admin_logout():
    return redirect('/admin/login')



    
#USER


#user login page

@app.route('/user_login' , methods = ['GET', 'POST'])
def user_login():
    if request.method == 'POST':
        user_name = request.form['user_name']
        user_password = request.form['user_password']
        if user_name == 'Radhika R' and user_password == '123456':
            return redirect('/user_dashboard')
        else:
            return redirect('/user_registration')
       
       
    return render_template('user_login.html')

#new_user registration page

@app.route('/user_registration' , methods = ['GET','POST'])
def user_registration():
    if request.method=='POST':
        user_name = request.form['user_name']
        user_email = request.form['user_email']
        user_password = request.form['user_password']
        user = User(user_name=user_name , user_email = user_email, user_password = user_password)
        db.session.add(user)
        db.session.commit()

        return redirect('/user_login')
    return render_template('user_registration.html')

@app.route('/user_dashboard')
def user_dashboard():
    user = User.query.all()
    all = Venue.query.all()

    return render_template('user_dashboard.html', all = all, user=user)

#user logout

@app.route('/user_logout')
def user_logout():
    return redirect('/user_login')


@app.route('/user_view')
def user_view():
    all = Venue.query.all()
    return render_template("user_view.html", all = all)





from flask import flash
from datetime import datetime

@app.route('/book_show/<int:show_id>', methods=['GET', 'POST'])
def book_show(show_id):
    show = Show.query.get(show_id)
    if request.method == 'POST':
        user_id = request.form['user_id']
        # show_id = request.form['show_id']
        venue_id = request.form['venue_id']
        date_str = request.form['date']
        number_of_seats = request.form['number_of_seats']
        if show.available_seats < int(number_of_seats):
            flash('Not enough seats available for booking!')
            return redirect(url_for('book_show', show_id=show_id))

    
        show.available_seats -= int(number_of_seats)
        db.session.commit()
        
 
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
        # Create a new Booking object and add it to the database
        booking = Booking(user_id=user_id, show_id=show_id, venue_id=venue_id, date=date, number_of_seats=number_of_seats)
        db.session.add(booking)
        db.session.commit()
        
        # Render the confirmation page with the booking details
        return render_template('confirmation.html', user_id=user_id, venue_id=venue_id, date=date, number_of_seats=number_of_seats)
    else:
        show = Show.query.get(show_id)
        available_seats = show.available_seats
        return render_template('book_show.html', available_seats=available_seats, show=show)

    

# search for venue and shows.....

@app.route('/search/venues', methods = ['GET'])
def search_venue():

    
    query = request.args.get('venue_search_query')
    venues = Venue.query.filter(Venue.venue_city.ilike("%"+query+"%")).all()
    
    return render_template('results.html', query=query, venues=venues)
print(str(Venue.query.filter_by(venue_city='query')))

@app.route('/search/shows', methods = ['GET'])
def search_show():

    
    query = request.args.get('show_search_query')
    shows = Show.query.filter(Show.show_name.ilike("%"+query+"%")).all()
    
    return render_template('showresults.html', query=query, shows=shows)

#ratings to give

@app.route("/ratings", methods=['POST', 'GET'])
def ratings():
    # Retrieve the user from the database
    user = User.query.all()
    # Retrieve all venues from the database
    venues = Venue.query.all()
    # Retrieve all shows from the database
    shows = Show.query.all()
    
    if request.method == 'POST':
        # Get the venue_id, show_id, and rating from the form submission
        user_id = request.form['user_id']
        venue_id = request.form['venue_id']
        show_id = request.form['show_id']
        rating = request.form['rating']
        
        # Create a new rating object with the retrieved data
        new_rating = Rating(venue_id=venue_id, show_id=show_id, rating=rating,user_id = user_id)
        
        # Add the new rating to the database and commit the transaction
        db.session.add(new_rating)
        db.session.commit()
        
        # Flash a success message to the user
        flash('Rating submitted!')
        
        # Redirect the user to the view_ratings page
        return redirect(url_for('ratings', venue_id=venue_id,show_id=show_id,rating=rating))
    
    # Render the ratings.html template with the retrieved data
    return render_template('ratings.html', user=user, venues=venues, shows=shows)

#ratings to view


@app.route('/view_ratings/<int:user_id>')
def view_ratings(user_id):
    
    user = User.query.get(user_id)
    ratings = Rating.query.filter_by(user_id=user_id).all()

    # Create a list to hold the rating data
    rating_data = []

    # Loop through the ratings and retrieve the venue and show names
    for rating in ratings:
        user = User.query.get(rating.user_id)
        venue = Venue.query.get(rating.venue_id)
        show = Show.query.get(rating.show_id)

        # Add some error handling for NoneType variables
        if not user or not venue or not show:
            continue

        rating_data.append({
            'user_name': user.user_name,
            'venue_name': venue.venue_name,
            'show_name': show.show_name,
            'rating': rating.rating
        })

    return render_template('view_ratings.html', user=user, ratings=rating_data,user_id=user_id)





# app.run(debug=True)




#adding venues to the database

def add_venue_if_not_existed():
    if db.session.query(Venue).count() == 0:
        v1=Venue(venue_name='Silver Screen', venue_place= 'Fame Hotel', venue_city= 'Berhampore', venue_capacity='300')
        v2=Venue(venue_name='Inox', venue_place= 'South City Mall', venue_city= 'Kolkata', venue_capacity='300')
        db.session.add(v1)
        db.session.add(v2)
        db.session.commit()

add_venue_if_not_existed()




@app.route('/summery')
def summery():
    return render_template("summery.html")

import matplotlib.pyplot as plt
import numpy as np
#1st chart
ratings = [rating.rating for rating in Rating.query.all()]
plt.clf()
plt.hist(ratings)
plt.title("Rating Chart")
plt.xlabel("rating")
plt.ylabel("Freq")

plt.savefig('rating_chart.jpg')

#2nd chart

for show in Show.query.all():
    available_seats = show.available_seats
    show_id = int(show.show_id)
    
    #plt.bar(available_seats,show_id)
    plt.hist(available_seats)
    plt.title("Available Seat Chart for Show")
    plt.ylabel("available_seats")
    plt.xlabel("show_id")

    plt.savefig('available_seats{show.show_id}.jpg')

#3rd chart
for venue in Venue.query.all():
    venue_id = venue.venue_id
    venue_capacity = venue.venue_capacity
    plt.bar(venue_id,venue_capacity)
    plt.hist(venue_capacity)
    plt.title("Venue capacity Chart")
    plt.ylabel("venue_capacity")
    plt.xlabel("venue_id")

    plt.savefig('venue_capacity.jpg')
