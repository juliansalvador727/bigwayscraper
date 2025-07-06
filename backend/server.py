from flask import Flask, jsonify
from restaurant import Restaurant
from scraper import scrape_line_size
import json

app = Flask(__name__)
@app.route("/api/waitlist")
def get_waitlist():
    restaurants = [
        Restaurant(2979, "Burnaby", "#7-4300 Kingsway, Burnaby, BC V5H 1Z8"),
        Restaurant(7289, "Kingsway", "4250 Kingsway #5, Burnaby, BC V5H 4V6"),
        Restaurant(8273, "Richmond", "4940 Number 3 Rd #123, Richmond, BC V6X 3A5"),
        Restaurant(9043, "Robson", "778 Robson St, Vancouver, BC V6Z 1N4"),
        Restaurant(9371, "Kerrisdale", "2145 W 41st Ave, Vancouver, BC V6M 1Z6"),
        Restaurant(2863, "Ackroyd", "8100 Ackroyd Rd Unit 175, Richmond, BC V6X 3K2"),
        Restaurant(7862, "New Westminister", "800 Carnarvon St #344 (3rd Floor New Westminster Station, New Westminster, BC V3M 0G3"),
        Restaurant(4561, "West End", "1479 Robson St, Vancouver, BC V6G 1C1"),
        Restaurant(5065, "Coquitlam", "2929 Barnet Hwy Unit 2660, Coquitlam, BC V3B 5R5"),
       Restaurant(2980, "UBC", "2155 Allison Rd #222, Vancouver, BC V6T 1T5"),
        Restaurant(5540, "Langley", "20202 66 Ave #130, Langley Twp, BC V2Y 1P3")
    ]
    
    for bigway in restaurants:
        bigway.set_line_size(scrape_line_size(bigway.store_id))
        
    with open("data.json", "w") as file:
        json.dump([bigway.to_dict() for bigway in restaurants], file, indent=2)

    return jsonify([bigway.to_dict() for bigway in restaurants])

if __name__ == "__main__":
    app.run(debug=True)
    