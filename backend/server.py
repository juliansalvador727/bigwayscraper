from flask import Flask, jsonify
from restaurant import Restaurant
from scraper import scrape_line_size
import json
import logging
import concurrent.futures
from datetime import datetime
from typing import List

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Restaurant configuration
RESTAURANTS = [
    Restaurant(2979, "Burnaby", "#7-4300 Kingsway, Burnaby, BC V5H 1Z8"),
    Restaurant(7289, "Kingsway", "4250 Kingsway #5, Burnaby, BC V5H 4V6"),
    Restaurant(8273, "Richmond", "4940 Number 3 Rd #123, Richmond, BC V6X 3A5"),
    Restaurant(9043, "Robson", "778 Robson St, Vancouver, BC V6Z 1N4"),
    Restaurant(9371, "Kerrisdale", "2145 W 41st Ave, Vancouver, BC V6M 1Z6"),
    Restaurant(2863, "Ackroyd", "8100 Ackroyd Rd Unit 175, Richmond, BC V6X 3K2"),
    Restaurant(7862, "New Westminster", "800 Carnarvon St #344 (3rd Floor New Westminster Station, New Westminster, BC V3M 0G3"),
    Restaurant(4561, "West End", "1479 Robson St, Vancouver, BC V6G 1C1"),
    Restaurant(5065, "Coquitlam", "2929 Barnet Hwy Unit 2660, Coquitlam, BC V3B 5R5"),
    Restaurant(2980, "UBC", "2155 Allison Rd #222, Vancouver, BC V6T 1T5"),
    Restaurant(5540, "Langley", "20202 66 Ave #130, Langley Twp, BC V2Y 1P3")
]

def scrape_single_restaurant(restaurant: Restaurant) -> Restaurant:
    """Scrape a single restaurant's waitlist data."""
    try:
        line_size = scrape_line_size(restaurant.store_id)
        restaurant.set_line_size(line_size)
        logger.info(f"✓ {restaurant.city}: {line_size} parties in line")
        return restaurant
    except Exception as e:
        logger.error(f"✗ {restaurant.city}: Error - {e}")
        restaurant.set_line_size(None)
        return restaurant

def scrape_all_restaurants(max_workers: int = 11) -> List[Restaurant]:
    """
    Scrape all restaurants concurrently.
    
    Args:
        max_workers: Maximum number of concurrent workers
        
    Returns:
        List of Restaurant objects with updated waitlist data
    """
    logger.info(f"Starting scrape of {len(RESTAURANTS)} restaurants with {max_workers} workers")
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all scraping tasks
        future_to_restaurant = {
            executor.submit(scrape_single_restaurant, restaurant): restaurant 
            for restaurant in RESTAURANTS
        }
        
        # Collect results
        restaurants = []
        for future in concurrent.futures.as_completed(future_to_restaurant):
            restaurant = future.result()
            restaurants.append(restaurant)
    
    # Sort by city name for consistent ordering
    restaurants.sort(key=lambda r: r.city)
    return restaurants

@app.route("/api/waitlist")
def get_waitlist():
    """Get current waitlist data for all restaurants."""
    try:
        start_time = datetime.now()
        restaurants = scrape_all_restaurants()
        end_time = datetime.now()
        
        # Save to JSON file
        data = [restaurant.to_dict() for restaurant in restaurants]
        with open("data.json", "w") as file:
            json.dump({
                "last_updated": start_time.isoformat(),
                "scrape_duration_seconds": (end_time - start_time).total_seconds(),
                "restaurants": data
            }, file, indent=2)
        
        logger.info(f"Scraping completed in {(end_time - start_time).total_seconds():.2f} seconds")
        
        return jsonify({
            "success": True,
            "last_updated": start_time.isoformat(),
            "scrape_duration_seconds": (end_time - start_time).total_seconds(),
            "restaurants": data
        })
        
    except Exception as e:
        logger.error(f"Error in get_waitlist: {e}")
        return jsonify({
            "success": False,
            "error": str(e),
            "restaurants": []
        }), 500

@app.route("/api/health")
def health_check():
    """Health check endpoint."""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "total_restaurants": len(RESTAURANTS)
    })

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)