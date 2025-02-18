# Commerce

Commerce is a web application developed as part of Harvard's CS50W course, designed to emulate an eBay-like auction site. It enables users to create auction listings, place bids, comment on listings, and manage a personal watchlist.

## Features

- **User Authentication**: Secure registration and login system to manage user accounts.
- **Auction Listings**: Users can create new listings with a title, description, starting bid, optional image URL, and category.
- **Bidding System**: Authenticated users can place bids on active listings, with validations ensuring bids exceed the current highest bid.
- **Watchlist**: Users can add or remove listings from their watchlist for easy access.
- **Categories**: Browse listings by categories to find items of interest.
- **Comments**: Authenticated users can add comments to listings, facilitating discussions.
- **Auction Closure**: Sellers can close auctions, declaring the highest bidder as the winner.

## Installation

1. **Clone the repository**

2. **Install dependencies**:
   Ensure you have Python and Django installed. You can install Django using pip:
   ```bash
   pip install Django
   ```

3. **Apply migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. **Create a superuser**:
   ```bash
   python manage.py createsuperuser
   ```

5. **Run the development server**:
   ```bash
   python manage.py runserver
   ```

6. **Access the application**:
   Open your web browser and navigate to `http://127.0.0.1:8000/`.

## Usage

- **Register**: Create a new account using the registration page.
- **Login**: Access your account using your credentials.
- **Create Listings**: Navigate to the "Create Listing" page to auction an item.
- **Bid on Listings**: View active listings and place bids on items of interest.
- **Manage Watchlist**: Add or remove items from your watchlist for quick access.
- **Comment**: Engage with other users by commenting on listings.
- **Close Auctions**: If you created a listing, you can close the auction to declare a winner.

## Models

The application includes the following models:

- **User**: Extends Django's AbstractUser model to include additional fields as needed.
- **Listing**: Represents an item up for auction, including details like title, description, starting bid, current bid, image URL, category, and status (active/closed).
- **Bid**: Records bids placed by users on listings, including the bid amount and the associated listing.
- **Comment**: Stores comments made by users on listings, including the content of the comment and the associated listing.

## Templates

The application utilizes Django's templating system with the following templates:

- **layout.html**: Base template that includes common HTML structure and navigation.
- **index.html**: Displays all active listings.
- **login.html**: Form for user login.
- **register.html**: Form for user registration.
- **create_listing.html**: Form to create a new auction listing.
- **listing.html**: Detailed view of a specific listing, including bids and comments.
- **watchlist.html**: Displays the user's watchlist.

## Admin Interface

The Django admin interface allows superusers to manage the application's data models:

- **Access Admin Panel**: Navigate to `http://127.0.0.1:8000/admin/` and log in with your superuser credentials.
- **Manage Models**: Add, edit, or delete users, listings, bids, and comments directly through the admin interface.

## Acknowledgments

This project was developed as part of Harvard University's CS50W course. Special thanks to the course instructors and staff for their guidance and support.
