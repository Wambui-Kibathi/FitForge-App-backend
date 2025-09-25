# FitForge App Backend

A Flask-based REST API for the FitForge workout planning application.

## Setup

1. **Navigate to the server directory:**
   ```bash
   cd server
   ```

2. **Install dependencies:**
   ```bash
   pipenv install
   ```

3. **Start the server:**
   ```bash
   pipenv run python app.py
   ```
   
   Or use the start script:
   ```bash
   ./start.sh
   ```

## API Endpoints

- `GET /` - API status
- `POST /register` - User registration
- `POST /login` - User login
- `POST /logout` - User logout
- `GET /current-user` - Get current user
- `GET /my-exercises` - Get user's exercises
- `GET /my-workouts` - Get user's workouts

### Resources
- `/users` - User management
- `/exercises` - Exercise management
- `/workouts` - Workout management
- `/instructors` - Instructor management
- `/workout-exercises` - Workout-Exercise relationships
- `/user-exercises` - User-Exercise relationships

## Database Schema

- **Users**: User accounts and profiles
- **Instructors**: Fitness instructors
- **Exercises**: Individual exercises with instructions
- **Workouts**: Workout routines
- **WorkoutExercises**: Exercise-workout relationships
- **UserExercises**: User-exercise tracking

## Database

- Database file: `instance/fitforge.db` (SQLite)
- Migrations folder: `migrations/`
- Pre-seeded with sample data (instructors, users, exercises, workouts)

## Development

The server runs on `http://localhost:5001` by default.
Frontend CORS is configured for `http://localhost:5173`.

Database is already initialized and seeded - just run the app!