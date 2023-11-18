from fastapi import APIRouter, status, Depends
from fastapi.security import OAuth2PasswordBearer
from .controller import AuthController
from .schemas import UserAuthCreate, HashingAlgorithmCreate, UserAuthResponse, UserAuthLogin, TokenResponse, UserRoleCreate, UserRoleResponse, RoleUpdate

router = APIRouter()
hashing_router = APIRouter()
user_roles_router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.post("/user/", status_code=status.HTTP_201_CREATED, response_model=UserAuthResponse)
def create_user(user_data: UserAuthCreate):
    """API endpoint to create a new user."""
    return AuthController.create(user_data)


@router.post("/users/login", status_code=status.HTTP_200_OK, response_model=TokenResponse)
def login(user_data: UserAuthLogin):
    """API endpoint to authenticate a user and generate a JWT token."""
    return AuthController.login(user_data)


@router.post("/token/refresh", status_code=status.HTTP_200_OK, response_model=TokenResponse)
def refresh_token(token: str = Depends(oauth2_scheme)):
    """API endpoint to refresh a JWT token."""
    return AuthController.refresh_token(token)


@hashing_router.post("/hashing-algorithms/")
def create_hashing_algorithm(algorithm_name: HashingAlgorithmCreate):
    """API endpoint to create a new hashing algorithm."""
    return AuthController.create_hashing_algorithm(algorithm_name)


@hashing_router.get("/hashing-algorithms/")
def get_all_hashing_algorithms():
    """Get all hashing algorithms."""
    return AuthController.get_all_hashing_algorithms()


@hashing_router.get("/hashing-algorithms/{algorithm_id}")
def get_hashing_algorithm_by_id(algorithm_id: int):
    """Get a hashing algorithm by its ID."""
    return AuthController.get_hashing_algorithm_by_id(algorithm_id)


@hashing_router.get("/hashing-algorithms/name/{algorithm_name}")
def get_hashing_algorithm_by_name(algorithm_name: str):
    """Get a hashing algorithm by its name."""
    return AuthController.get_hashing_algorithm_by_name(algorithm_name)


@hashing_router.put("/hashing-algorithms/{algorithm_id}")
def update_hashing_algorithm(algorithm_id: int, algorithm_name: HashingAlgorithmCreate):
    """API endpoint to update a hashing algorithm."""
    return AuthController.update_hashing_algorithm(algorithm_id, algorithm_name.algorithm_name)


@hashing_router.delete("/hashing-algorithms/{algorithm_id}")
def delete_hashing_algorithm(algorithm_id: int):
    """API endpoint to delete a hashing algorithm."""
    return AuthController.delete_hashing_algorithm(algorithm_id)


@user_roles_router.post("/users/roles/", status_code=status.HTTP_200_OK, response_model=UserRoleResponse)
def create_user_role(role_name: UserRoleCreate):
    """API endpoint to create a new user role."""
    return AuthController.create_role(role_name)


@user_roles_router.get("/users/roles/", status_code=status.HTTP_200_OK, response_model=list[UserRoleResponse])
def get_all_user_roles():
    """API endpoint to get all user roles."""
    return AuthController.get_all_roles()


@user_roles_router.get("/users/roles/id/{role_id}", status_code=status.HTTP_200_OK, response_model=UserRoleResponse)
def get_user_role_by_id(role_id: int):
    """API endpoint to get a user role by ID."""
    return AuthController.get_role_by_id(role_id)


@user_roles_router.get("/users/roles/name/{role_name}", status_code=status.HTTP_200_OK, response_model=UserRoleResponse)
def get_user_role_by_name(role_name: str):
    """API endpoint to get a user role by name or id."""
    return AuthController.get_role_by_name(role_name)


@user_roles_router.put("/users/roles/id/{role_id}", status_code=status.HTTP_200_OK, response_model=UserRoleCreate)
def update_user_role_by_id(role_id: int, role_name: UserRoleCreate):
    """API endpoint to update a user role."""
    return AuthController.update_role_by_id(role_id, role_name)


@user_roles_router.put("/users/roles/name/{old_role_name}", status_code=status.HTTP_200_OK, response_model=UserRoleCreate)
def update_user_role_by_name(old_role_name: str, role_update: RoleUpdate):
    """API endpoint to update a user role."""
    return AuthController.update_role_by_name(old_role_name, role_update.new_role_name)


@user_roles_router.delete("/users/roles/id/{role_id}", status_code=status.HTTP_200_OK)
def delete_user_role_by_id(role_id: int):
    """API endpoint to delete a user role."""
    return AuthController.delete_role_by_id(role_id)


@user_roles_router.delete("/users/roles/name/{role_name}", status_code=status.HTTP_200_OK)
def delete_user_role_by_name(role_name: str):
    """API endpoint to delete a user role."""
    return AuthController.delete_role_by_name(role_name)
