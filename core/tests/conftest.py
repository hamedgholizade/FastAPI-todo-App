from fastapi.testclient import TestClient
from sqlalchemy import StaticPool
import pytest
from faker import Faker

from tasks.models import TaskModel
from users.models import UserModel
from users.utils import get_password_hash, generate_access_token
from core.database import Base, create_engine, sessionmaker, get_db
from main import app

# object of faker
fake = Faker()

# create connector for connecting database
SQLARCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLARCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)

# create cursor for database
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# module
@pytest.fixture(scope="package")
def db_session():
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()

# Override dependency from get_db with override_get_db of app
# module
@pytest.fixture(scope="module",autouse=True)
def override_dependencies(db_session):
    app.dependency_overrides[get_db] = lambda: db_session
    yield
    app.dependency_overrides.pop(get_db,None)

# create base class for declaring tables
# session
@pytest.fixture(scope="session",autouse=True)
def tear_up_and_down_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

# package
@pytest.fixture(scope="package")
def anon_client():
    client = TestClient(app)
    yield client

# package
@pytest.fixture(scope="package")
def auth_client(db_session):
    client = TestClient(app)
    user = db_session.query(UserModel).filter_by(username="testuser").first()
    access_token = generate_access_token(user.id)
    client.headers.update({"Authorization": f"Bearer {access_token}"})
    yield client

# generating fake data by faker package
# module
@pytest.fixture(scope="module",autouse=True)
def generate_fake_data(db_session):
    user = UserModel(
        username="testuser", password=get_password_hash("Aa@12345")
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    print(f"User created with username: {user.username} and ID: {user.id}")

    tasks_list = []
    for _ in range(10):
        tasks_list.append(
            TaskModel(
                user_id=user.id,
                title=fake.sentence(nb_words=6),
                description=fake.text(),
                is_completed=fake.boolean(),
            )
        )
    db_session.add_all(tasks_list)
    db_session.commit()
    print(f"Added 10 tasks for user_id: {user.id}")

# function
@pytest.fixture(scope="function")
def random_task(db_session):
    user = db_session.query(UserModel).filter_by(username="testuser").first()
    task_obj = db_session.query(TaskModel).filter_by(user_id=user.id).first()
    return task_obj
    