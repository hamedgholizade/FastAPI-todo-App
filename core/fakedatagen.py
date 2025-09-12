from sqlalchemy.orm import Session
from faker import Faker

from core.database import SessionLocal
from tasks.models import TaskModel
from users.models import UserModel
from users.utils import get_password_hash


fake = Faker()

def seed_users(db):
    user = UserModel(
        username=fake.user_name(),
        password=get_password_hash('Aa@12345')
        )
    db.add(user)
    db.commit()
    db.refresh(user)
    print(f"User created with username: {user.username} and ID: {user.id}")
    return user

def seed_tasks(db, user, count=10):
    tasks_list = []
    for _ in range(count):
        tasks_list.append(
            TaskModel(
                user_id=user.id,
                title=fake.sentence(nb_words=6),
                description=fake.text(),
                is_completed=fake.boolean()
            )
        )
    db.add_all(tasks_list)
    db.commit()
    print(f"Added {count} tasks for user_id: {user.id}")

def main():
    db = SessionLocal()
    
    try:
        user = seed_users(db)
        seed_tasks(db, user)
    finally:
        db.close()

if __name__ == '__main__':
    main()
