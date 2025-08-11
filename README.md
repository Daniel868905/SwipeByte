# SwipeByte

SwipeByte is a full-stack application for discovering restaurants with a swipe interface.

## Installation

Clone the repository and set up both the backend and frontend.

### Backend
1. `cd backend`
2. (Optional) create a virtual environment: `python -m venv venv && source venv/bin/activate`
3. Install dependencies: `pip install django djangorestframework django-cors-headers`
4. Run database migrations: `python manage.py migrate`
5. Start the server: `python manage.py runserver`

### Frontend
1. `cd frontend/swipebyte`
2. Install packages: `npm install`
3. Start the development server: `npm run dev`

## Story of Operations
1. New users sign up or existing users log in.
2. Users search for restaurants based on distance and price.
3. Restaurants appear as cards that can be swiped to like or dislike.
4. Liked restaurants may match with other members, and matches are displayed.
5. Favorites can be saved for quick access.
6. The theme toggle in the navigation bar switches between light and dark modes with food-and-code inspired backgrounds.