from sqlalchemy import create_engine, Column, String, Float, Boolean, JSON, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import json
import os

# ===== DATABASE SETUP =====
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH  = os.path.join(BASE_DIR, "../data/moodmap.db")

engine       = create_engine(f"sqlite:///{DB_PATH}", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
Base         = declarative_base()


# ===== PLACE MODEL =====
class Place(Base):
    __tablename__ = "places"

    id             = Column(String, primary_key=True)
    name           = Column(String)
    city           = Column(String)
    state          = Column(String)
    type           = Column(String)
    moods          = Column(JSON)
    tags           = Column(JSON)
    rating         = Column(Float)
    budget         = Column(String)
    best_time      = Column(String)
    description    = Column(String)
    image_url      = Column(String)
    lat            = Column(Float)
    lng            = Column(Float)
    duration_hrs   = Column(Float)
    solo_friendly  = Column(Boolean)
    group_friendly = Column(Boolean)
    indoor         = Column(Boolean)


# ===== CREATE TABLES =====
def init_db():
    Base.metadata.create_all(bind=engine)
    print("✅ Tables created!")


# ===== SEED FROM places.json =====
def seed_db():
    session = SessionLocal()

    # Check if already seeded
    if session.query(Place).count() > 0:
        print("⚠️ Database already has data — skipping seed.")
        session.close()
        return

    # Load places.json
    json_path = os.path.join(BASE_DIR, "../data/places.json")
    with open(json_path, "r", encoding="utf-8") as f:
        places = json.load(f)

    # Insert each place
    for p in places:
        place = Place(
            id             = p.get("id"),
            name           = p.get("name"),
            city           = p.get("city"),
            state          = p.get("state"),
            type           = p.get("type"),
            moods          = p.get("moods"),
            tags           = p.get("tags"),
            rating         = p.get("rating"),
            budget         = p.get("budget"),
            best_time      = p.get("best_time"),
            description    = p.get("description"),
            image_url      = p.get("image_url"),
            lat            = p.get("lat"),
            lng            = p.get("lng"),
            duration_hrs   = p.get("duration_hrs"),
            solo_friendly  = p.get("solo_friendly"),
            group_friendly = p.get("group_friendly"),
            indoor         = p.get("indoor"),
        )
        session.add(place)

    session.commit()
    session.close()
    print(f"✅ Seeded {len(places)} places into database!")


# ===== RUN =====
if __name__ == "__main__":
    init_db()
    seed_db()