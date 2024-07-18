from .default import default_router
from .registration import registration_router
from .select_meet import meet_selection_router

all_routers = [default_router, registration_router, meet_selection_router]