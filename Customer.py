class Customer:
    customers = []

    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name
        self.id = len(Customer.customers) + 1
        Customer.customers.append(self)

    def given_name(self):
        return self.first_name

    def family_name(self):
        return self.last_name

    def full_name(self):
        return f"{self.last_name} {self.first_name}"

    @classmethod
    def all(cls):
        return cls.customers

    def num_reviews(self):
        return len([review for review in Review.all() if review.customer == self])

    @classmethod
    def find_by_name(cls, name):
        for customer in cls.customers:
            if customer.full_name() == name:
                return customer
        return None

    @classmethod
    def find_all_by_given_name(cls, given_name):
        return [customer for customer in cls.customers if customer.given_name() == given_name]

    def restaurants(self):
        return list(set([review.restaurant for review in Review.all() if review.customer == self]))

    def add_review(self, restaurant, rating):
        review = Review(self, restaurant, rating)
        return review


class Restaurant:
    restaurants = []

    def __init__(self, name):
        self.name = name
        self.id = len(Restaurant.restaurants) + 1
        Restaurant.restaurants.append(self)

    def name(self):
        return self.name

    def reviews(self):
        return [review for review in Review.all() if review.restaurant == self]

    def customers(self):
        return list(set([review.customer for review in self.reviews()]))

    def average_star_rating(self):
        ratings = [review.rating for review in self.reviews()]
        return sum(ratings) / len(ratings) if ratings else 0


class Review:
    reviews = []

    def __init__(self, customer, restaurant, rating):
        self.customer = customer
        self.restaurant = restaurant
        self.rating = rating
        self.id = len(Review.reviews) + 1
        Review.reviews.append(self)

    @classmethod
    def all(cls):
        return cls.reviews

    def rating(self):
        return self.rating

    def customer(self):
        return self.customer

    def restaurant(self):
        return self.restaurant


# Usage example

# Create instances
customer1 = Customer("John", "Doe")
customer2 = Customer("Alice", "Smith")
restaurant1 = Restaurant("Tasty Bites")
restaurant2 = Restaurant("Sizzling Grill")

# Add reviews
review1 = Review(customer1, restaurant1, 4)
review2 = Review(customer2, restaurant1, 5)
review3 = Review(customer1, restaurant2, 3)

# Print customer information
print("\nCustomers in the database:")
for customer in Customer.all():
    print(f"Customer ID: {customer.id}, Name: {customer.full_name()}, Number of Reviews: {customer.num_reviews()}")

# Print restaurant information
print("\nRestaurants in the database:")
for restaurant in Restaurant.restaurants:
    print(f"Restaurant ID: {restaurant.id}, Name: {restaurant.name}, Average Star Rating: {restaurant.average_star_rating()}")

# Print review information
print("\nReviews in the database:")
for review in Review.all():
    print(f"Review ID: {review.id}, Customer: {review.customer.full_name()}, Restaurant: {review.restaurant.name}, Rating: {review.rating}")

# Add a new review
customer1.add_review(restaurant2, 5)

# Print updated review information
print("\nReviews in the database after adding a new review:")
for review in Review.all():
    print(f"Review ID: {review.id}, Customer: {review.customer.full_name()}, Restaurant: {review.restaurant.name}, Rating: {review.rating}")
