from flask import request, session
from flask_restful import Resource
from models import db, User, Exercise, Workout, WorkoutExercise, UserExercise, Instructor

# User Resources
class UserListResource(Resource):
    def get(self):
        try:
            users = User.query.all()
            return [user.to_dict() for user in users]
        except Exception as e:
            return {'error': str(e)}, 500
    
    def post(self):
        data = request.get_json()
        user = User(**data)
        db.session.add(user)
        db.session.commit()
        return user.to_dict(), 201

class UserResource(Resource):
    def get(self, id):
        user = User.query.get_or_404(id)
        return user.to_dict()
    
    def patch(self, id):
        user = User.query.get_or_404(id)
        data = request.get_json()
        for key, value in data.items():
            setattr(user, key, value)
        db.session.commit()
        return user.to_dict()
    
    def delete(self, id):
        user = User.query.get_or_404(id)
        db.session.delete(user)
        db.session.commit()
        return '', 204

# Exercise Resources
class ExerciseListResource(Resource):
    def get(self):
        try:
            exercises = Exercise.query.all()
            return [exercise.to_dict() for exercise in exercises]
        except Exception as e:
            return {'error': str(e)}, 500
    
    def post(self):
        data = request.get_json()
        exercise = Exercise(**data)
        db.session.add(exercise)
        db.session.commit()
        return exercise.to_dict(), 201

class ExerciseResource(Resource):
    def get(self, id):
        exercise = Exercise.query.get_or_404(id)
        return exercise.to_dict()
    
    def patch(self, id):
        exercise = Exercise.query.get_or_404(id)
        data = request.get_json()
        for key, value in data.items():
            setattr(exercise, key, value)
        db.session.commit()
        return exercise.to_dict()
    
    def delete(self, id):
        exercise = Exercise.query.get_or_404(id)
        db.session.delete(exercise)
        db.session.commit()
        return '', 204

# Workout Resources
class WorkoutListResource(Resource):
    def get(self):
        try:
            workouts = Workout.query.filter(Workout.user_id.is_(None)).all()
            return [workout.to_dict() for workout in workouts]
        except Exception as e:
            return {'error': str(e)}, 500
    
    def post(self):
        if 'user_id' not in session:
            return {'error': 'Not logged in'}, 401
        try:
            data = request.get_json()
            if 'instructor_id' not in data:
                return {'error': 'instructor_id is required'}, 400
            
            data['user_id'] = session['user_id']  # Force current user for personal workouts
            workout = Workout(**data)
            db.session.add(workout)
            db.session.commit()
            return workout.to_dict(), 201
        except Exception as e:
            return {'error': str(e)}, 400

class WorkoutResource(Resource):
    def get(self, id):
        workout = Workout.query.get_or_404(id)
        return workout.to_dict()
    
    def patch(self, id):
        workout = Workout.query.get_or_404(id)
        if 'user_id' not in session:
            return {'error': 'Not logged in'}, 401
        
        user = User.query.get(session['user_id'])
        if workout.user_id != session['user_id'] and not user.is_admin:
            return {'error': 'Not authorized'}, 403
            
        data = request.get_json()
        for key, value in data.items():
            setattr(workout, key, value)
        db.session.commit()
        return workout.to_dict()
    
    def delete(self, id):
        workout = Workout.query.get_or_404(id)
        if 'user_id' not in session:
            return {'error': 'Not logged in'}, 401
        
        user = User.query.get(session['user_id'])
        if workout.user_id != session['user_id'] and not user.is_admin:
            return {'error': 'Not authorized'}, 403
            
        db.session.delete(workout)
        db.session.commit()
        return '', 204

# WorkoutExercise Resources
class WorkoutExerciseListResource(Resource):
    def post(self):
        data = request.get_json()
        workout_exercise = WorkoutExercise(**data)
        db.session.add(workout_exercise)
        db.session.commit()
        return workout_exercise.to_dict(), 201

class WorkoutExerciseResource(Resource):
    def patch(self, id):
        workout_exercise = WorkoutExercise.query.get_or_404(id)
        data = request.get_json()
        for key, value in data.items():
            setattr(workout_exercise, key, value)
        db.session.commit()
        return workout_exercise.to_dict()

# UserExercise Resources
class UserExerciseListResource(Resource):
    def get(self):
        if 'user_id' not in session:
            return {'error': 'Not logged in'}, 401
        try:
            user_exercises = UserExercise.query.filter_by(user_id=session['user_id']).all()
            return [ue.to_dict() for ue in user_exercises]
        except Exception as e:
            return {'error': str(e)}, 500
    
    def post(self):
        if 'user_id' not in session:
            return {'error': 'Not logged in'}, 401
        try:
            data = request.get_json()
            data['user_id'] = session['user_id']  # Force current user
            
            existing = UserExercise.query.filter_by(
                user_id=session['user_id'], 
                exercise_id=data['exercise_id']
            ).first()
            
            if existing:
                return {'error': 'Exercise already in your profile'}, 400
            
            user_exercise = UserExercise(**data)
            db.session.add(user_exercise)
            db.session.commit()
            return user_exercise.to_dict(), 201
        except Exception as e:
            return {'error': str(e)}, 400

class UserExerciseResource(Resource):
    def delete(self, id):
        user_exercise = UserExercise.query.get_or_404(id)
        if 'user_id' not in session:
            return {'error': 'Not logged in'}, 401
        
        user = User.query.get(session['user_id'])
        if user_exercise.user_id != session['user_id'] and not user.is_admin:
            return {'error': 'Not authorized'}, 403
            
        db.session.delete(user_exercise)
        db.session.commit()
        return '', 204

# Instructor Resources
class InstructorListResource(Resource):
    def get(self):
        try:
            instructors = Instructor.query.all()
            return [instructor.to_dict() for instructor in instructors]
        except Exception as e:
            return {'error': str(e)}, 500
    
    def post(self):
        try:
            data = request.get_json()
            instructor = Instructor(**data)
            db.session.add(instructor)
            db.session.commit()
            return instructor.to_dict(), 201
        except Exception as e:
            return {'error': str(e)}, 400

class InstructorResource(Resource):
    def get(self, id):
        instructor = Instructor.query.get_or_404(id)
        return instructor.to_dict()
    
    def patch(self, id):
        instructor = Instructor.query.get_or_404(id)
        data = request.get_json()
        for key, value in data.items():
            setattr(instructor, key, value)
        db.session.commit()
        return instructor.to_dict()
    
    def delete(self, id):
        instructor = Instructor.query.get_or_404(id)
        db.session.delete(instructor)
        db.session.commit()
        return '', 204

# Authentication Routes
def register():
    try:
        data = request.get_json()
        if not data or not all(k in data for k in ['name', 'email', 'password', 'fitness_level']):
            return {'error': 'Missing required fields'}, 400
            
        existing_user = User.query.filter_by(email=data['email']).first()
        if existing_user:
            return {'error': 'User already exists'}, 400
        
        user = User(
            name=data['name'],
            email=data['email'],
            fitness_level=data['fitness_level']
        )
        user.set_password(data['password'])
        db.session.add(user)
        db.session.commit()
        session['user_id'] = user.id
        return user.to_dict(), 201
    except Exception as e:
        db.session.rollback()
        return {'error': str(e)}, 400

def login():
    try:
        data = request.get_json()
        if not data or not all(k in data for k in ['email', 'password']):
            return {'error': 'Missing email or password'}, 400
            
        user = User.query.filter_by(email=data['email']).first()
        if user and user.check_password(data['password']):
            session['user_id'] = user.id
            return user.to_dict()
        return {'error': 'Invalid email or password'}, 401
    except Exception as e:
        return {'error': str(e)}, 400

def logout():
    session.pop('user_id', None)
    return {'message': 'Logged out'}

def current_user():
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        if user:
            return user.to_dict()
    return {'error': 'Not logged in'}, 401

def my_exercises():
    if 'user_id' not in session:
        return {'error': 'Not logged in'}, 401
    
    try:
        user_exercises = UserExercise.query.filter_by(user_id=session['user_id']).all()
        return [ue.to_dict() for ue in user_exercises]
    except Exception as e:
        return {'error': str(e)}, 500

def my_workouts():
    if 'user_id' not in session:
        return {'error': 'Not logged in'}, 401
    
    try:
        workouts = Workout.query.filter(
            Workout.user_id == session['user_id'],
            Workout.user_id.isnot(None)
        ).all()
        return [workout.to_dict() for workout in workouts]
    except Exception as e:
        return {'error': str(e)}, 500