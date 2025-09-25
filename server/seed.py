from app import app
from models import db, User, Exercise, Workout, WorkoutExercise, UserExercise, Instructor

def seed_data():
    with app.app_context():
        # Clear existing data
        db.drop_all()
        db.create_all()
        
        # Create instructors
        instructors = [
            Instructor(name="Jake Gallagher", specialty="Strength Training", bio="Expert in powerlifting and muscle building techniques"),
            Instructor(name="Waruiru Kibathi", specialty="Cardio & Endurance", bio="Marathon runner specializing in cardiovascular fitness"),
            Instructor(name="Levi Waithaka", specialty="Functional Fitness", bio="Functional movement and athletic performance specialist"),
            Instructor(name="Zelda Wambui", specialty="Flexibility & Recovery", bio="Yoga instructor and mobility expert")
        ]
        
        for instructor in instructors:
            db.session.add(instructor)
        
        # Create users (F1 drivers as app users)
        users = [
            User(name="Admin User", email="admin@fitforge.com", fitness_level="Advanced", is_admin=True),
            User(name="Lewis Hamilton", email="lewis.hamilton@fitforge.com", fitness_level="Advanced"),
            User(name="Max Verstappen", email="max.verstappen@fitforge.com", fitness_level="Advanced"),
            User(name="Charles Leclerc", email="charles.leclerc@fitforge.com", fitness_level="Intermediate"),
            User(name="Lando Norris", email="lando.norris@fitforge.com", fitness_level="Intermediate")
        ]
        
        for user in users:
            db.session.add(user)
        
        # Create exercises by instructors
        exercises = [
            Exercise(
                name="Power Push-ups",
                category="Bodyweight",
                muscle_group="Chest",
                difficulty="Intermediate",
                instructions="Jake's explosive push-up technique for upper body strength.",
                instructor_id=1
            ),
            Exercise(
                name="Endurance Running",
                category="Cardio",
                muscle_group="Legs",
                difficulty="Beginner",
                instructions="Waruiru's marathon training technique for cardiovascular fitness.",
                instructor_id=2
            ),
            Exercise(
                name="Functional Deadlifts",
                category="Weightlifting",
                muscle_group="Back",
                difficulty="Advanced",
                instructions="Levi's functional deadlift movement for athletic performance.",
                instructor_id=3
            ),
            Exercise(
                name="Flexibility Flow",
                category="Yoga",
                muscle_group="Full Body",
                difficulty="Beginner",
                instructions="Zelda's yoga flow sequence for flexibility and recovery.",
                instructor_id=4
            ),
            Exercise(
                name="Strength Squats",
                category="Weightlifting",
                muscle_group="Legs",
                difficulty="Intermediate",
                instructions="Jake's powerlifting squat technique for maximum strength.",
                instructor_id=1
            ),
            Exercise(
                name="Core Stability",
                category="Bodyweight",
                muscle_group="Core",
                difficulty="Intermediate",
                instructions="Levi's functional core training for athletic stability.",
                instructor_id=3
            )
        ]
        
        for exercise in exercises:
            db.session.add(exercise)
        
        db.session.commit()
        
        # Create instructor workouts (no user_id - these are instructor templates)
        workouts = [
            Workout(name="Strength Builder", description="Jake's complete strength training program", duration=75, instructor_id=1, user_id=None),
            Workout(name="Cardio Endurance", description="Waruiru's marathon training workout", duration=90, instructor_id=2, user_id=None),
            Workout(name="Functional Athlete", description="Levi's athletic performance routine", duration=60, instructor_id=3, user_id=None),
            Workout(name="Flexibility & Recovery", description="Zelda's yoga and mobility session", duration=45, instructor_id=4, user_id=None)
        ]
        
        for workout in workouts:
            db.session.add(workout)
        
        db.session.commit()
        
        # Create workout exercises
        workout_exercises = [
            WorkoutExercise(workout_id=1, exercise_id=1, sets=4, reps=15, weight=0, rest_time=45),
            WorkoutExercise(workout_id=1, exercise_id=5, sets=3, reps=60, weight=0, rest_time=30),
            WorkoutExercise(workout_id=2, exercise_id=2, sets=5, reps=12, weight=0, rest_time=60),
            WorkoutExercise(workout_id=2, exercise_id=6, sets=4, reps=8, weight=0, rest_time=90),
            WorkoutExercise(workout_id=3, exercise_id=3, sets=5, reps=5, weight=225, rest_time=180),
            WorkoutExercise(workout_id=4, exercise_id=4, sets=4, reps=1, weight=0, rest_time=30)
        ]
        
        for we in workout_exercises:
            db.session.add(we)
        
        # No user exercises or personal workouts created by default
        # All users (including Admin) start with empty profiles
        # Users will add content using "Add to My Profile" buttons
        
        db.session.commit()
        print("Database seeded successfully!")

if __name__ == '__main__':
    seed_data()