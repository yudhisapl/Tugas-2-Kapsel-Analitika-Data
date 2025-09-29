from fastapi import FastAPI
from modules.items.routes import createUser, readUser, updateUser, deleteUser

app = FastAPI(title="Users CRUD API (Modules Layout)")

# In-memory store
app.state.users = {}
app.state._id_seq = 0

# register routers
app.include_router(createUser.router)
app.include_router(readUser.router)
app.include_router(updateUser.router)
app.include_router(deleteUser.router)