import logging

from langchain_core.tools import tool

from services.google.place import (
    get_place_details,
    search_place
)


logger = logging.getLogger('ai')

@tool
async def search_place_and_rating(place: str) -> dict:
    """
    The function can search for place and return it rating.
    
    Args:
        place: palce name
        
    Returns: Data and rating of the place.
    """
    logger.info("Searching for place: {}".format(place))
    place_id = await search_place(place)
    
    if not place_id:
        return {}
    
    logger.info("Get details for {} with id {}".format(place, place_id))
    data = await get_place_details(place_id)
    
    logger.debug(f"Place data: {data}")
    
    return data