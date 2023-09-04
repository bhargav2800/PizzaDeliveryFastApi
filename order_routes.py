from fastapi import APIRouter, Depends, Header, status, HTTPException, Form, UploadFile, File
from pydantic import EmailStr
from auth.auth_bearer import JWTBearer, get_current_user
from models import Order
from schemas import OrderModel, FormDataModel
from database import session
from fastapi.encoders import jsonable_encoder

order_router = APIRouter(
    prefix='/orders',
    tags=['orders']
)


@order_router.get('/', dependencies=[Depends(JWTBearer())])
async def hello():
    return {"message": "Hello order"}


@order_router.post('/order', dependencies=[Depends(JWTBearer())], status_code=status.HTTP_201_CREATED)
async def place_an_order(order: OrderModel, authorization: str = Header(None)):
    schema, token = authorization.split()
    current_user = get_current_user(token)

    new_order = Order(
        pizza_size=order.pizza_size,
        quantity=order.quantity
    )

    new_order.user = current_user

    session.add(new_order)

    session.commit()

    response = {
        "pizza_size": new_order.pizza_size,
        "quantity": new_order.quantity,
        "id": new_order.id,
        "order_status": new_order.order_status
    }

    return jsonable_encoder(response)


@order_router.get('/orders', dependencies=[Depends(JWTBearer())], status_code=status.HTTP_200_OK)
async def list_all_orders(authorization: str = Header(None)):
    schema, token = authorization.split()
    current_user = get_current_user(token)

    if current_user.is_staff:
        orders = session.query(Order).all()
        return jsonable_encoder(orders)

    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not a superuser.")


@order_router.get('/orders/{id}', dependencies=[Depends(JWTBearer())], status_code=status.HTTP_200_OK)
async def get_order_by_id(id: int, authorization: str = Header(None)):
    schema, token = authorization.split()
    current_user = get_current_user(token)

    if current_user.is_staff:
        order = session.query(Order).filter(Order.id == id).first()

        return jsonable_encoder(order)

    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not a superuser.")


@order_router.get('/user/orders', dependencies=[Depends(JWTBearer())], status_code=status.HTTP_200_OK)
async def get_current_user_orders(authorization: str = Header(None)):
    schema, token = authorization.split()
    current_user = get_current_user(token)
    return jsonable_encoder(current_user.orders)


@order_router.get('/user/orders/{order_id}', dependencies=[Depends(JWTBearer())], status_code=status.HTTP_200_OK)
async def get_current_user_specific_order(order_id: int, authorization: str = Header(None)):
    schema, token = authorization.split()
    current_user = get_current_user(token)
    order = session.query(Order).filter(Order.id == order_id, Order.user == current_user).first()
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return jsonable_encoder(order)


@order_router.put('/order/update/{order_id}', dependencies=[Depends(JWTBearer())], status_code=status.HTTP_200_OK)
async def update_order(order_id: int, order: OrderModel, authorization: str = Header(None)):
    schema, token = authorization.split()
    current_user = get_current_user(token)
    if current_user.is_staff:
        order_obj = session.query(Order).filter(Order.id == order_id).first()

        if order_obj is None:
            raise HTTPException(status_code=404, detail="Order not found")

        order_obj.quantity = order.quantity
        order_obj.pizza_size = order.pizza_size

        session.commit()

        session.refresh(order_obj)

        return jsonable_encoder(order_obj)

    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not a superuser.")
