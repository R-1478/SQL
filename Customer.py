import sqlite3

class Database:
    def __init__(self):
        self.conn = sqlite3.connect(':memory:')
        self.cursor = self.conn.cursor()

        # Create Customer table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Customer (
                id INTEGER PRIMARY KEY,
                first_name TEXT,
                last_name TEXT
            )
        ''')

        # Create Restaurant table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Restaurant (
                id INTEGER PRIMARY KEY,
                name TEXT
            )
        ''')

        # Create Review table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Review (
                id INTEGER PRIMARY KEY,
                customer_id INTEGER,
                restaurant_id INTEGER,
                rating INTEGER,
                FOREIGN KEY (customer_id) REFERENCES Customer (id),
                FOREIGN KEY (restaurant_id) REFERENCES Restaurant (id)
            )
        ''')

    def commit(self):
        self.conn.commit()

class Customer:
    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name
        self.id = None  # Will be set when saved to the database

    def given_name(self):
        return self.first_name

    def family_name(self):
        return self.last_name

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def save(self, db):
        db.cursor.execute('''
            INSERT INTO Customer (first_name, last_name)
            VALUES (?, ?)
        ''', (self.first_name, self.last_name))
        self.id = db.cursor.lastrowid

    @classmethod
    def find_by_name(cls, db, full_name):
        db.cursor.execute('''
            SELECT * FROM Customer
            WHERE first_name || ' ' || last_name = ?
        ''', (full_name,))
        row = db.cursor.fetchone()
        if row:
            customer = cls(row[1], row[2])
            customer.id = row[0]
            return customer
        return None

    @classmethod
    def find_all_by_given_name(cls, db, given_name):
        db.cursor.execute('''
            SELECT * FROM Customer
            WHERE first_name = ?
        ''', (given_name,))
        rows = db.cursor.fetchall()
        customers = []
        for row in rows:
            customer = cls(row[1], row[2])
            customer.id = row[0]
            customers.append(customer)
        return customers
    @classmethod
    def find_by_id(cls, db, id):
        db.cursor.execute('SELECT * FROM Customer WHERE id = ?', (id,))
        row = db.cursor.fetchone()
        if row:
            customer = cls(row[1], row[2])
        customer.id = row[0]
        return customer
       

class Restaurant:
    def __init__(self, name):
        self.name = name
        self.id = None  # Will be set when saved to the database

    def save(self, db):
        db.cursor.execute('''
            INSERT INTO Restaurant (name)
            VALUES (?)
        ''', (self.name,))
        self.id = db.cursor.lastrowid

    def average_star_rating(self, db):
        db.cursor.execute('''
            SELECT AVG(rating) FROM Review
            WHERE restaurant_id = ?
        ''', (self.id,))
        result = db.cursor.fetchone()[0]
        return result if result else 0
    @classmethod
    def find_by_id(cls, db, id):
        db.cursor.execute('SELECT * FROM Restaurant WHERE id = ?', (id,))
        row = db.cursor.fetchone()
        if row:
            restaurant = cls(row)
            restaurant.id = row[0]
            return restaurant
        else:
            return None

class Review:
    def __init__(self, customer, restaurant, rating):
        self.customer = customer
        self.restaurant = restaurant
        self.rating = rating
        self.id = None  # Will be set when saved to the database

    def save(self, db):
        db.cursor.execute('''
            INSERT INTO Review (customer_id, restaurant_id, rating)
            VALUES (?, ?, ?)
        ''', (self.customer.id, self.restaurant.id, self.rating))
        self.id = db.cursor.lastrowid

    @classmethod
    def all(cls, db):
        db.cursor.execute('SELECT * FROM Review')
        rows = db.cursor.fetchall()
        reviews = []
        for row in rows:
            customer = Customer.find_by_id(db, row[1])
            restaurant = Restaurant.find_by_id(db, row[2])
            review = cls(customer, restaurant, row[3])
            review.id = row[0]
            reviews.append(review)
        return reviews

# Usage example
db = Database()

# Creating instances
customer1 = Customer("John", "Doe")
restaurant1 = Restaurant("Good Eats")
review1 = Review(customer1, restaurant1, 4)

# Saving instances to the database
customer1.save(db)
restaurant1.save(db)
review1.save(db)

# Retrieving all reviews from the database
all_reviews = Review.all(db)
for review in all_reviews:
    print(f"Review ID: {review.id}, Customer: {review.customer.full_name()}, Restaurant: {review.restaurant.name}, Rating: {review.rating}")

# Retrieving average star rating for a restaurant
average_rating = restaurant1.average_star_rating(db)
print(f"Average Star Rating for {restaurant1.name}: {average_rating}")

# Finding a customer by name
found_customer = Customer.find_by_name(db, "John Doe")
print(f"Found Customer: {found_customer.full_name()}")

# Finding all customers by given name
customers_with_given_name = Customer.find_all_by_given_name(db, name="John")
for customer in customers_with_given_name:
    print(customer.full_name())
