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
3.(Optional) set the backend URL: `export VITE_API_BASE_URL=http://localhost:8000`
4. Start the development server: `npm run dev`


## Story of Operations
1. New users sign up or existing users log in.
2. Users search for restaurants based on distance and price.
3. Restaurants appear as cards that can be swiped to like or dislike.
4. Liked restaurants may match with other members, and matches are displayed.
5. Favorites can be saved for quick access.
6. The theme toggle in the navigation bar switches between light and dark modes with food-and-code inspired backgrounds.

## Deployment Notes

The backend is configured for secure production use:

* Email verification is required for new accounts. Configure SMTP settings via
  ``EMAIL_BACKEND`` and ``DEFAULT_FROM_EMAIL`` environment variables.
* Authentication tokens are stored in an ``auth_token`` cookie and all cookies
  are marked ``Secure`` and ``HttpOnly``. Serve the app over HTTPS.
* Set ``ALLOWED_HOSTS``, ``CSRF_TRUSTED_ORIGINS`` and ``CORS_ALLOWED_ORIGINS``
  environment variables to match your Amazon AWS domain.
* ``SECURE_SSL_REDIRECT`` and HSTS are enabled by default. Ensure your load
  balancer forwards the ``X-Forwarded-Proto`` header.

pip install django-extensions
python manage.py runserver_plus --cert-file dev-cert.pem 0.0.0.0:8000
