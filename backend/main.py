from fastapi import FastAPI, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from groq import Groq
from database import SessionLocal, Place, init_db, seed_db
from dotenv import load_dotenv
import os

load_dotenv()

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
app = FastAPI()

# ===== STARTUP — create & seed DB if needed =====
@app.on_event("startup")
def startup():
    init_db()
    seed_db()
    # Force reseed if empty
    session = SessionLocal()
    count = session.query(Place).count()
    session.close()
    print(f"✅ Database has {count} places")

app.mount("/frontend", StaticFiles(directory="../frontend"), name="static")

# ===== PAGE ROUTES =====
@app.get("/")
def home():
    return FileResponse("../frontend/index.html")

@app.get("/mood")
def mood_page():
    return FileResponse("../frontend/mood.html")

@app.get("/inputs")
def inputs():
    return FileResponse("../frontend/inputs.html")

@app.get("/results")
def results():
    return FileResponse("../frontend/results.html")

@app.get("/saved")
def saved():
    return FileResponse("../frontend/saved.html")

@app.get("/place")
def place():
    return FileResponse("../frontend/place.html")


# ===== RECOMMEND API =====
@app.get("/api/recommend")
def recommend(mood: str = Query(...), city: str = Query("")):

    mood_type_map = {
        "foodie":    ["restaurant", "cafe", "street walk"],
        "relaxed":   ["beach", "park", "cafe", "bookstore"],
        "adventure": ["sports", "trekking", "wildlife", "amusement park", "outdoor activity"],
        "nature":    ["park", "wildlife", "lake", "nature", "beach"],
        "creative":  ["museum", "art", "workshop", "heritage", "bookstore", "cafe"]
    }

    mood_tag_map = {
        "foodie":    ["happy", "social", "calm"],
        "relaxed":   ["calm", "reflective", "romantic", "sad"],
        "adventure": ["adventurous", "energetic"],
        "nature":    ["calm", "adventurous", "reflective"],
        "creative":  ["creative", "curious", "calm", "reflective"]
    }

    allowed_types = mood_type_map.get(mood.lower(), [])
    allowed_tags  = mood_tag_map.get(mood.lower(), [])

    session = SessionLocal()

    try:
        # Query all places from SQLite
        query = session.query(Place)

        # City filter
        if city.strip():
            query = query.filter(
                Place.city.ilike(f"%{city.strip()}%")
            )

        all_places = query.all()

        # Filter by mood type and tags
        results = []
        for place in all_places:
            place_type  = (place.type or "").lower()
            place_moods = [m.lower() for m in (place.moods or [])]

            type_match = place_type in allowed_types
            mood_match = any(m in place_moods for m in allowed_tags)

            if type_match and mood_match:
                results.append({
                    "id":            place.id,
                    "name":          place.name,
                    "city":          place.city,
                    "state":         place.state,
                    "type":          place.type,
                    "moods":         place.moods,
                    "tags":          place.tags,
                    "rating":        place.rating,
                    "budget":        place.budget,
                    "best_time":     place.best_time,
                    "description":   place.description,
                    "image_url":     place.image_url,
                    "lat":           place.lat,
                    "lng":           place.lng,
                    "duration_hrs":  place.duration_hrs,
                    "solo_friendly": place.solo_friendly,
                    "group_friendly":place.group_friendly,
                    "indoor":        place.indoor,
                })

        # Sort by rating
        results.sort(key=lambda x: x.get("rating", 0), reverse=True)
        return {"places": results[:10]}

    finally:
        session.close()


# ===== ITINERARY API =====
@app.get("/api/itinerary")
def get_itinerary(
    name: str = Query(...),
    type: str = Query(...),
    city: str = Query(...),
    mood: str = Query(...)
):
    try:
        prompt = f"""You are a fun travel guide. A user is feeling {mood} and wants to visit {name}, a {type} in {city}, India.
Write a short, exciting 3-4 line visit suggestion. Include what to do there, best time to go, and one insider tip. Keep it friendly and fun!"""

        response = groq_client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150
        )
        return {"suggestion": response.choices[0].message.content}

    except Exception as e:
        print(f"GROQ ERROR: {e}")
        return {"suggestion": f"Error: {str(e)}"}