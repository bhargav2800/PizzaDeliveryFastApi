from fastapi import APIRouter, status, Depends

from auth.auth_bearer import JWTBearer
from auth.auth_handler import CreateAccessRefreshToken

from database import session
from schemas import SignUpModel, LoginModel
from models import User
from fastapi.exceptions import HTTPException
from werkzeug.security import generate_password_hash, check_password_hash

auth_router = APIRouter(
    prefix='/auth',
    tags=['auth']
)


@auth_router.get('/', dependencies=[Depends(JWTBearer())])
async def hello():
    return {"message": "Hello auth"}


@auth_router.post('/signup', response_model=SignUpModel, status_code=status.HTTP_201_CREATED)
async def signup(user: SignUpModel):
    db_email = session.query(User).filter(User.email == user.email).first()

    if db_email is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="User with the email already exists"
                            )

    db_username = session.query(User).filter(User.username == user.username).first()

    if db_username is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="User with the username already exists"
                            )

    new_user = User(
        username=user.username,
        email=user.email,
        password=generate_password_hash(user.password),
        is_active=user.is_active,
        is_staff=user.is_staff,
    )

    session.add(new_user)

    session.commit()

    return new_user


# Login route
@auth_router.post('/login', status_code=status.HTTP_200_OK)
async def login(user: LoginModel):
    db_user = session.query(User).filter(User.username == user.username).first()

    if db_user and check_password_hash(db_user.password, user.password):
        return CreateAccessRefreshToken(db_user.username)

    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Invalid Username or Password")
