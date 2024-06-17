from .get_travel_spots import router as get_travel_spots_router
from .predict import router as predict_router
from .get_travel_spots_and_predict import router as get_travel_spots_and_predict_router

__all__ = ["get_travel_spots_router", "predict_router", "get_travel_spots_and_predict_router"]