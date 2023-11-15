# Task: Design an eBay-like e-commerce auction site that will allow users to post auction listings, place bids on listings, comment on those listings, and add listings to a “watchlist.”

# Commerce Project Requirements:

## Models

Your application should have the following models in addition to the User model:

1. **Auction Listings Model**
   - Fields: Title, Description, Starting Bid, Image URL (optional), Category (optional)

2. **Bids Model**
   - Fields: Bid Amount, Listing (foreign key), Bidder (foreign key)

3. **Comments Model**
   - Fields: Comment Text, Listing (foreign key), Commenter (foreign key)

You may include additional models if needed.

## Create Listing

- Users should be able to visit a page to create a new listing.
- Specify: Title, Description, Starting Bid.
- Optional: Provide an Image URL and/or select a category (e.g., Fashion, Toys, Electronics, Home, etc.).

## Active Listings Page

- Default route displays all currently active auction listings.
- Display for each listing: Title, Description, Current Price, Photo (if available).

## Listing Page

- Clicking on a listing takes users to a page specific to that listing.
- Users can view all details about the listing, including the current price.

### User Actions on Listing Page

- If signed in:
  - Add the item to their "Watchlist."
  - Bid on the item (must meet bid criteria).
  - If the creator, have the ability to "close" the auction.
  - If a winner, display winning message.

- Users can add comments to the listing page.
- Display all comments made on the listing.

## Watchlist

- Signed-in users can visit a Watchlist page.
- Display all listings added to their watchlist.
- Clicking on any listing takes the user to that listing’s page.

## Categories

- Users can visit a page displaying a list of all listing categories.
- Clicking on a category name takes the user to a page displaying all active listings in that category.

## Django Admin Interface

- Site administrators can use the Django admin interface to:
  - View, add, edit, and delete listings.
  - View, add, edit, and delete comments.
  - View, add, edit, and delete bids made on the site.
