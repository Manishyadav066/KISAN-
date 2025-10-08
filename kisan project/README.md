# Kisan Project - Farmer Management System

A Django-based web application for managing farmer information, crops, market prices, and weather data.

## Features

- Farmer profiles with detailed information
- Crop management with seasonal tracking
- Market price comparison tool
- Weather information dashboard
- Analytics and reporting
- Notification system

## Local Development Setup

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run migrations:
   ```bash
   python manage.py migrate
   ```
5. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```
6. Load sample data (optional):
   ```bash
   python create_sample_data.py
   ```
7. Run the development server:
   ```bash
   python manage.py runserver
   ```

## Deployment

### Environment Variables

Set the following environment variables for production:

- `SECRET_KEY`: Django secret key
- `DEBUG`: Set to False for production
- `ALLOWED_HOSTS`: Comma-separated list of allowed hosts
- Database settings:
  - `DB_NAME`: Database name
  - `DB_USER`: Database user
  - `DB_PASSWORD`: Database password
  - `DB_HOST`: Database host
  - `DB_PORT`: Database port

### Heroku Deployment

1. Create a new Heroku app
2. Add the Heroku Postgres addon
3. Set environment variables in Heroku config vars
4. Deploy using Git:
   ```bash
   git push heroku main
   ```

### Other Platforms

For platforms like Render, AWS, or DigitalOcean:

1. Ensure Python 3.11+ is available
2. Install dependencies from requirements.txt
3. Run migrations:
   ```bash
   python manage.py migrate
   ```
4. Collect static files:
   ```bash
   python manage.py collectstatic --noinput
   ```
5. Start the server with Gunicorn:
   ```bash
   gunicorn kisan_project.wsgi:application
   ```

## Project Structure

- `kisan_app/`: Main application with models, views, and templates
- `kisan_project/`: Django project settings
- `templates/`: HTML templates
- `static/`: Static files (CSS, JavaScript, images)
- `media/`: User uploaded files

## Database Models

- Farmer: Farmer profiles with contact information
- Crop: Crop information with seasonal data
- CropCategory: Categories for different crop types
- MarketPrice: Market price tracking
- WeatherData: Weather information storage
- Notification: System notifications for farmers

## API Endpoints

- `/`: Home page with dashboard
- `/farmers/`: List of farmers
- `/farmer/<id>/`: Farmer detail page
- `/crops/`: List of crops
- `/analytics/`: Analytics dashboard
- `/calculator/`: Price calculator tool
- `/weather/`: Weather information
- `/notifications/`: Notification system

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a pull request