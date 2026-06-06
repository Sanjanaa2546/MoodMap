// ===== TYPEWRITER (index.html only) =====
const words = ["your mood 😌", "your vibe ⚡", "your hunger 🍜", "your energy 🌿", "your soul 🎨"];
let wordIndex = 0, charIndex = 0, deleting = false;

function typeWriter() {
  const el = document.getElementById('typewriter');
  if (!el) return;
  const word = words[wordIndex];
  if (!deleting) {
    el.textContent = word.substring(0, charIndex + 1);
    charIndex++;
    if (charIndex === word.length) {
      deleting = true;
      setTimeout(typeWriter, 1800);
      return;
    }
  } else {
    el.textContent = word.substring(0, charIndex - 1);
    charIndex--;
    if (charIndex === 0) {
      deleting = false;
      wordIndex = (wordIndex + 1) % words.length;
    }
  }
  setTimeout(typeWriter, deleting ? 60 : 100);
}
typeWriter();


// ===== SAVE TO LOCALSTORAGE =====
function saveSelection(key, value) {
  localStorage.setItem(key, value);
}
function getSelection(key) {
  return localStorage.getItem(key);
}
// ===== ALL PLACES DATA (single source of truth) =====
const allPlaces = [
  { name: "Marina Beach",              type: "Beach",      cost: 0,   duration: 2, rating: 4.5, tags: ["outdoor","free","scenic"],          mood: "relaxed"   },
  { name: "Semmozhi Poonga",           type: "Park",       cost: 30,  duration: 2, rating: 4.3, tags: ["garden","peaceful","nature"],        mood: "relaxed"   },
  { name: "Elliots Beach",             type: "Beach",      cost: 0,   duration: 2, rating: 4.2, tags: ["calm","sunset","walk"],              mood: "relaxed"   },
  { name: "Amethyst Cafe",             type: "Cafe",       cost: 300, duration: 2, rating: 4.6, tags: ["cozy","coffee","heritage"],          mood: "relaxed"   },
  { name: "Murugan Idli Shop",         type: "Restaurant", cost: 150, duration: 1, rating: 4.7, tags: ["south indian","breakfast","iconic"], mood: "foodie"    },
  { name: "Rayar's Mess",              type: "Restaurant", cost: 100, duration: 1, rating: 4.6, tags: ["authentic","lunch","local"],         mood: "foodie"    },
  { name: "Marina Beach Food",         type: "Street Food",cost: 100, duration: 1, rating: 4.4, tags: ["sundal","snacks","beachside"],       mood: "foodie"    },
  { name: "Saravana Bhavan",           type: "Restaurant", cost: 200, duration: 1, rating: 4.5, tags: ["vegetarian","thali","iconic"],       mood: "foodie"    },
  { name: "Muttukadu Backwaters",      type: "Outdoor",    cost: 400, duration: 3, rating: 4.3, tags: ["boating","water","activity"],        mood: "adventure" },
  { name: "MGM Dizzee World",          type: "Theme Park", cost: 500, duration: 4, rating: 4.1, tags: ["rides","fun","thrilling"],           mood: "adventure" },
  { name: "Kart Centre Chennai",       type: "Sports",     cost: 450, duration: 2, rating: 4.4, tags: ["go-kart","racing","adrenaline"],     mood: "adventure" },
  { name: "Covelong Beach",            type: "Beach",      cost: 200, duration: 3, rating: 4.5, tags: ["surfing","waves","outdoor"],         mood: "adventure" },
  { name: "Guindy National Park",      type: "Park",       cost: 30,  duration: 3, rating: 4.4, tags: ["wildlife","trails","serene"],        mood: "nature"    },
  { name: "Muttukadu Lake",            type: "Lake",       cost: 0,   duration: 2, rating: 4.2, tags: ["birds","nature","calm"],             mood: "nature"    },
  { name: "Theosophical Society",      type: "Garden",     cost: 0,   duration: 2, rating: 4.5, tags: ["heritage","trees","peaceful"],       mood: "nature"    },
  { name: "Government Museum",         type: "Museum",     cost: 15,  duration: 3, rating: 4.3, tags: ["history","art","culture"],           mood: "creative"  },
  { name: "DakshinaChitra",            type: "Museum",     cost: 150, duration: 4, rating: 4.6, tags: ["heritage","crafts","art"],           mood: "creative"  },
  { name: "Amethyst Bookstore",        type: "Bookstore",  cost: 0,   duration: 2, rating: 4.5, tags: ["books","cozy","creative"],           mood: "creative"  },
  { name: "Cholamandal Artist Village",type: "Gallery",    cost: 50,  duration: 3, rating: 4.7, tags: ["art","paintings","unique"],          mood: "creative"  },
];