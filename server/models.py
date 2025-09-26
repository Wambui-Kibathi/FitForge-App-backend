from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class Instructor(db.Model, SerializerMixin):
    __tablename__ = 'instructors'
    
    serialize_rules = ('-exercises', '-workouts')
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    specialty = db.Column(db.String(100), nullable=False)
    bio = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    exercises = db.relationship('Exercise', backref='instructor', lazy=True)
    workouts = db.relationship('Workout', backref='instructor', lazy=True)

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'
    
    serialize_rules = ('-workouts', '-user_exercises', '-password_hash')
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    fitness_level = db.Column(db.String(20), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    workouts = db.relationship('Workout', backref='user', lazy=True, cascade='all, delete-orphan')
    user_exercises = db.relationship('UserExercise', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Exercise(db.Model, SerializerMixin):
    __tablename__ = 'exercises'
    
    serialize_rules = ('-workout_exercises', '-user_exercises', '-instructor.exercises')
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    muscle_group = db.Column(db.String(50), nullable=False)
    difficulty = db.Column(db.String(20), nullable=False)
    instructions = db.Column(db.Text, nullable=False)
    instructor_id = db.Column(db.Integer, db.ForeignKey('instructors.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    workout_exercises = db.relationship('WorkoutExercise', backref='exercise', lazy=True, cascade='all, delete-orphan')
    user_exercises = db.relationship('UserExercise', backref='exercise', lazy=True, cascade='all, delete-orphan')

class Workout(db.Model, SerializerMixin):
    __tablename__ = 'workouts'
    
    serialize_rules = ('-user.workouts', '-user.user_exercises', '-workout_exercises', '-instructor.workouts')
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    duration = db.Column(db.Integer, nullable=False)  # in minutes
    instructor_id = db.Column(db.Integer, db.ForeignKey('instructors.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)  # For user's personal workouts
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    workout_exercises = db.relationship('WorkoutExercise', backref='workout', lazy=True, cascade='all, delete-orphan')

class WorkoutExercise(db.Model, SerializerMixin):
    __tablename__ = 'workout_exercises'
    
    serialize_rules = ('-workout.workout_exercises', '-exercise.workout_exercises')
    
    id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(db.Integer, db.ForeignKey('workouts.id'), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.id'), nullable=False)
    sets = db.Column(db.Integer, nullable=False)
    reps = db.Column(db.Integer, nullable=False)
    weight = db.Column(db.Float)  # user submittable attribute
    rest_time = db.Column(db.Integer)  # in seconds, user submittable attribute

class UserExercise(db.Model, SerializerMixin):
    __tablename__ = 'user_exercises'
    
    serialize_rules = ('-user.user_exercises', '-exercise.user_exercises')
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.id'), nullable=False)
    personal_record = db.Column(db.Float)  # user submittable attribute
    notes = db.Column(db.Text)  # user submittable attribute
    created_at = db.Column(db.DateTime, default=datetime.utcnow)