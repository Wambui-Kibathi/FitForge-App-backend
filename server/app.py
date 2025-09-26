from flask import Flask
from flask_restful import Api
from flask_migrate import Migrate
from flask_cors import CORS
import os
from dotenv import load_dotenv
from models import db
from routes import (
    UserListResource, UserResource,
    ExerciseListResource, ExerciseResource,
    WorkoutListResource, WorkoutResource,
    WorkoutExerciseListResource, WorkoutExerciseResource,
    UserExerciseListResource, UserExerciseResource,
    InstructorListResource, InstructorResource,
    register, login, logout, current_user, my_exercises, my_workouts
)

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///fitforge.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SESSION_COOKIE_SAMESITE'] = 'None'
app.config['SESSION_COOKIE_SECURE'] = True  # HTTPS required for production

db.init_app(app)
migrate = Migrate(app, db)
api = Api(app)
CORS(app, supports_credentials=True, origins=['http://localhost:5173'])

# Authentication routes
app.add_url_rule('/register', 'register', register, methods=['POST'])
app.add_url_rule('/login', 'login', login, methods=['POST'])
app.add_url_rule('/logout', 'logout', logout, methods=['POST'])
app.add_url_rule('/current-user', 'current_user', current_user)
app.add_url_rule('/my-exercises', 'my_exercises', my_exercises)
app.add_url_rule('/my-workouts', 'my_workouts', my_workouts)

# Register API resources
api.add_resource(UserListResource, '/users')
api.add_resource(UserResource, '/users/<int:id>')
api.add_resource(ExerciseListResource, '/exercises')
api.add_resource(ExerciseResource, '/exercises/<int:id>')
api.add_resource(WorkoutListResource, '/workouts')
api.add_resource(WorkoutResource, '/workouts/<int:id>')
api.add_resource(WorkoutExerciseListResource, '/workout-exercises')
api.add_resource(WorkoutExerciseResource, '/workout-exercises/<int:id>')
api.add_resource(UserExerciseListResource, '/user-exercises')
api.add_resource(UserExerciseResource, '/user-exercises/<int:id>')
api.add_resource(InstructorListResource, '/instructors')
api.add_resource(InstructorResource, '/instructors/<int:id>')

@app.route('/')
def home():
    return {"message": "FitForge Workout Planner API"}

if __name__ == '__main__':
    app.run(debug=True, port=5001)