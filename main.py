from fastapi import FastAPI
from auth_routes import auth_router
from order_routes import order_router
# from debug_toolbar.middleware import DebugToolbarMiddleware


app = FastAPI(debug=True)

# Performance checking tools
# app.add_middleware(
#     DebugToolbarMiddleware,
#     panels=["debug_toolbar.panels.sqlalchemy.SQLAlchemyPanel"],
#     session_generators=["database:session"]  # Add the full python path of your session generators
# )

app.include_router(order_router)
app.include_router(auth_router)