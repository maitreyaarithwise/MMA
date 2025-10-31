from fastapi import APIRouter, HTTPException
import requests
import logging
from typing import Optional
from app.schemas.pinnacle import (
    PinnaclePeriodsResponse,
    PinnacleSportsResponse,
    # PinnacleSpecialMarketsResponse,
    PinnacleArchiveEventsResponse,
    PinnacleLeaguesResponse,
    PinnacleMarketsResponse,
    PinnacleEventDetailsResponse
)
from app.core.config import settings

router = APIRouter(prefix="/pinnacle", tags=["pinnacle"])
logger = logging.getLogger(__name__)

def get_headers():
    return {
        "x-rapidapi-key": settings.PINNACLE_API_KEY,
        "x-rapidapi-host": settings.PINNACLE_HOST
    }

@router.get("/periods", response_model=PinnaclePeriodsResponse)
async def get_pinnacle_periods(sport_id: int = 7):
    """Get Pinnacle periods for a specific sport"""
    url = "https://pinnacle-odds.p.rapidapi.com/kit/v1/meta-periods"
    querystring = {"sport_id": str(sport_id)}
    headers = get_headers()
    
    try:
        logger.info(f"Making request to Pinnacle periods API with sport_id: {sport_id}")
        response = requests.get(url, headers=headers, params=querystring)
        logger.info(f"Response status: {response.status_code}")
        
        if response.status_code == 403:
            logger.error("403 Forbidden - Check API key and headers")
            raise HTTPException(status_code=403, detail="API access forbidden. Please check API key and headers.")
        
        response.raise_for_status()
        data = response.json()
        return PinnaclePeriodsResponse(**data)
    except requests.exceptions.RequestException as e:
        logger.error(f"Request failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch periods: {str(e)}")

@router.get("/sports", response_model=PinnacleSportsResponse)
async def get_pinnacle_sports():
    """Get all available sports from Pinnacle"""
    url = "https://pinnacle-odds.p.rapidapi.com/kit/v1/sports"
    headers = get_headers()
    
    try:
        logger.info("Making request to Pinnacle sports API")
        response = requests.get(url, headers=headers)
        logger.info(f"Response status: {response.status_code}")
        
        if response.status_code == 403:
            logger.error("403 Forbidden - Check API key and headers")
            raise HTTPException(status_code=403, detail="API access forbidden. Please check API key and headers.")
        
        response.raise_for_status()
        data = response.json()
        return PinnacleSportsResponse(sports=data)
    except requests.exceptions.RequestException as e:
        logger.error(f"Request failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch sports: {str(e)}")

# @router.get("/special-markets", response_model=PinnacleSpecialMarketsResponse)
# async def get_pinnacle_special_markets(
#     event_type: str = "prematch",
#     sport_id: int = 7,
#     is_have_odds: bool = True,
#     league_ids: Optional[str] = "889"
# ):
#     """Get special markets for NFL"""
#     url = "https://pinnacle-odds.p.rapidapi.com/kit/v1/special-markets"
#     querystring = {
#         "event_type": event_type,
#         "sport_id": str(sport_id),
#         "is_have_odds": str(is_have_odds).lower(),
#         "league_ids": league_ids
#     }
#     headers = get_headers()

#     try:
#         logger.info(f"Making request to Pinnacle special markets API with sport_id: {sport_id}")
#         response = requests.get(url, headers=headers, params=querystring)
#         logger.info(f"Response status: {response.status_code}")

#         if response.status_code == 403:
#             logger.error("403 Forbidden - Check API key and headers")
#             raise HTTPException(status_code=403, detail="API access forbidden. Please check API key and headers.")

#         response.raise_for_status()
#         data = response.json()
#         return PinnacleSpecialMarketsResponse(**data)
#     except requests.exceptions.RequestException as e:
#         logger.error(f"Request failed: {str(e)}")
#         raise HTTPException(status_code=500, detail=f"Failed to fetch special markets: {str(e)}")

@router.get("/archive-events", response_model=PinnacleArchiveEventsResponse)
async def get_pinnacle_archive_events(
    sport_id: int = 7,
    page_num: int = 1,
    league_ids: Optional[str] = "889"
):
    """Get archived events for NFL"""
    url = "https://pinnacle-odds.p.rapidapi.com/kit/v1/archive"
    querystring = {
        "sport_id": str(sport_id),
        "page_num": str(page_num),
        "league_ids": league_ids
    }
    headers = get_headers()
    
    try:
        logger.info(f"Making request to Pinnacle archive API with sport_id: {sport_id}")
        response = requests.get(url, headers=headers, params=querystring)
        logger.info(f"Response status: {response.status_code}")
        
        if response.status_code == 403:
            logger.error("403 Forbidden - Check API key and headers")
            raise HTTPException(status_code=403, detail="API access forbidden. Please check API key and headers.")
        
        response.raise_for_status()
        data = response.json()
        # Normalize to expected schema: { "events": [PinnacleArchiveEvent, ...] }
        if isinstance(data, dict) and "events" in data:
            normalized = data
        elif isinstance(data, list):
            normalized = {"events": data}
        elif isinstance(data, dict):
            # Single event object
            normalized = {"events": [data]}
        else:
            raise HTTPException(status_code=502, detail="Unexpected response format from archive API")
        return PinnacleArchiveEventsResponse(**normalized)
    except requests.exceptions.RequestException as e:
        logger.error(f"Request failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch archive events: {str(e)}")

@router.get("/leagues", response_model=PinnacleLeaguesResponse)
async def get_pinnacle_leagues(sport_id: int = 7):
    """Get leagues for a specific sport"""
    url = "https://pinnacle-odds.p.rapidapi.com/kit/v1/leagues"
    querystring = {"sport_id": str(sport_id)}
    headers = get_headers()
    
    try:
        logger.info(f"Making request to Pinnacle leagues API with sport_id: {sport_id}")
        response = requests.get(url, headers=headers, params=querystring)
        logger.info(f"Response status: {response.status_code}")
        
        if response.status_code == 403:
            logger.error("403 Forbidden - Check API key and headers")
            raise HTTPException(status_code=403, detail="API access forbidden. Please check API key and headers.")
        
        response.raise_for_status()
        data = response.json()
        return PinnacleLeaguesResponse(**data)
    except requests.exceptions.RequestException as e:
        logger.error(f"Request failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch leagues: {str(e)}")

@router.get("/markets", response_model=PinnacleMarketsResponse)
async def get_pinnacle_markets(
    event_type: str = "prematch",
    sport_id: int = 7,
    is_have_odds: bool = True,
    league_ids: Optional[str] = "889",
    event_ids: Optional[str] = "1617646879"
):
    """Get markets for NFL"""
    url = "https://pinnacle-odds.p.rapidapi.com/kit/v1/markets"
    querystring = {
        "event_type": event_type,
        "sport_id": str(sport_id),
        "is_have_odds": str(is_have_odds).lower(),
        "league_ids": league_ids,
        "event_ids": event_ids
    }
    headers = get_headers()
    
    try:
        logger.info(f"Making request to Pinnacle markets API with sport_id: {sport_id}")
        response = requests.get(url, headers=headers, params=querystring)
        logger.info(f"Response status: {response.status_code}")
        
        if response.status_code == 403:
            logger.error("403 Forbidden - Check API key and headers")
            raise HTTPException(status_code=403, detail="API access forbidden. Please check API key and headers.")
        
        response.raise_for_status()
        data = response.json()
        # Normalize to expected schema: { "markets": [PinnacleMarket, ...] }
        if isinstance(data, dict) and "markets" in data:
            normalized = data
        elif isinstance(data, list):
            normalized = {"markets": data}
        elif isinstance(data, dict):
            # Single market object
            normalized = {"markets": [data]}
        else:
            raise HTTPException(status_code=502, detail="Unexpected response format from markets API")
        return PinnacleMarketsResponse(**normalized)
    except requests.exceptions.RequestException as e:
        logger.error(f"Request failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch markets: {str(e)}")

@router.get("/event-details", response_model=PinnacleEventDetailsResponse)
async def get_pinnacle_event_details(event_id: str = "1617646879"):
    """Get details for a specific event"""
    url = "https://pinnacle-odds.p.rapidapi.com/kit/v1/details"
    querystring = {"event_id": event_id}
    headers = get_headers()
    
    try:
        logger.info(f"Making request to Pinnacle event details API with event_id: {event_id}")
        response = requests.get(url, headers=headers, params=querystring)
        logger.info(f"Response status: {response.status_code}")
        
        if response.status_code == 403:
            logger.error("403 Forbidden - Check API key and headers")
            raise HTTPException(status_code=403, detail="API access forbidden. Please check API key and headers.")
        
        response.raise_for_status()
        data = response.json()
        return PinnacleEventDetailsResponse(**data)
    except requests.exceptions.RequestException as e:
        logger.error(f"Request failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch event details: {str(e)}")
