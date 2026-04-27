from langchain_core.tools import tool
from pydantic import BaseModel, Field

class SearchInput(BaseModel):
    location: str = Field(description="The city or area to search for properties")
    guests: int = Field(description="Number of guests")

@tool("search_available_properties", args_schema=SearchInput)
def search_available_properties(location: str, guests: int):
    """Search for available properties based on location and guest count."""
    return f"Searching for properties in {location} for {guests} guests..."

class DetailsInput(BaseModel):
    listing_id: str = Field(description="The UUID of the listing")

@tool("get_listing_details", args_schema=DetailsInput)
def get_listing_details(listing_id: str):
    """Get detailed information about a specific property."""
    return f"Fetching details for listing {listing_id}..."

class BookingInput(BaseModel):
    listing_id: str = Field(description="The UUID of the listing to book")
    guest_name: str = Field(description="Full name of the guest")
    check_in: str = Field(description="Check-in date (YYYY-MM-DD)")
    check_out: str = Field(description="Check-out date (YYYY-MM-DD)")

@tool("create_booking", args_schema=BookingInput)
def create_booking(listing_id: str, guest_name: str, check_in: str, check_out: str):
    """Create a new booking for a property."""
    return f"Booking confirmed for {guest_name} at listing {listing_id} from {check_in} to {check_out}."
