from flask import Flask, render_template_string, request, redirect, url_for
from datetime import datetime
import math

app = Flask(__name__)

# ------------------------------------------------------------------
# 1  CITY DATA  (lat, lon, misc_per_person/day Rs, sights, hotels)
# ------------------------------------------------------------------
CITY = {
    "Karachi":   (24.86, 67.00, 1800,
        ["Clifton Beach", "Mazar-e-Quaid", "Port Grand"],
        [("Avari Towers", 12000, 4.4), ("Hotel Mehran", 7500, 3.9), ("Regent Plaza", 9000, 4.0)]),
    "Hyderabad": (25.40, 68.36, 1500,
        ["Sindh Museum", "Rani Bagh"],
        [("Indus Hotel", 6000, 3.8), ("Hotel Faran", 5000, 3.5)]),
    "Sukkur":    (27.70, 68.85, 1400,
        ["Lansdowne Bridge", "Sadhu Belo"],
        [("Hotel One", 7000, 4.1), ("Palm Lodge", 3500, 3.4)]),
    "Gwadar":    (25.12, 62.32, 1900,
        ["Hammerhead", "Gwadar Beach", "Koh-e-Battil"],
        [("PC Gwadar", 15000, 4.3), ("Sadaf Resort", 7000, 3.9)]),
    "Quetta":    (30.18, 66.97, 1600,
        ["Hanna Lake", "Ziarat Residency"],
        [("Quetta Serena", 13000, 4.4), ("Bloom Star", 5500, 3.7)]),
    "Multan":    (30.15, 71.52, 1600,
        ["Shrine Shah Rukn-e-Alam", "Multan Fort"],
        [("Ramada Multan", 11000, 4.2), ("Hotel One", 7500, 4.0)]),
    "Bahawalpur":(29.39, 71.68, 1500,
        ["Noor Mahal", "Derawar Fort"],
        [("Hotel One", 8000, 4.1), ("Step Inn", 4500, 3.5)]),
    "Lahore":    (31.52, 74.35, 2000,
        ["Badshahi Mosque", "Lahore Fort", "Shalimar Gardens"],
        [("PC Lahore", 14000, 4.5), ("Hotel One", 8000, 4.1), ("Luxus Grand", 9500, 4.3)]),
    "Faisalabad":(31.45, 73.13, 1500,
        ["Clock Tower", "Lyallpur Museum"],
        [("Grand Regent", 6000, 3.9)]),
    "Islamabad": (33.68, 73.04, 2200,
        ["Faisal Mosque", "Daman-e-Koh", "Monal"],
        [("Serena Hotel", 16000, 4.7), ("Envoy Continental", 9000, 4.2)]),
    "Rawalpindi":(33.56, 73.01, 2100,
        ["Ayub Park", "Raja Bazaar"],
        [("PC Rawalpindi", 13500, 4.3), ("Flashman Hotel", 7000, 3.8)]),
    "Peshawar":  (34.01, 71.58, 1700,
        ["Bala Hissar Fort", "Qissa Khwani Bazaar"],
        [("Shelton Rezidor", 8000, 4.0), ("Greens Hotel", 6000, 3.8)]),
    "Abbottabad":(34.16, 73.22, 1800,
        ["Shimla Hill", "Thandiani"],
        [("Hotel One", 7500, 4.0)]),
    "Swat":      (34.80, 72.35, 1800,
        ["Malam Jabba", "Fizagat Park", "White Palace"],
        [("Swat Serena", 12000, 4.5), ("PTDC Motel", 6500, 3.9)]),
    "Murree":    (33.90, 73.39, 1900,
        ["Mall Road", "Patriata Chairlift"],
        [("Shangrila Resort", 14000, 4.4), ("Lockwood Hotel", 8500, 4.0)]),
    "Hunza":     (36.31, 74.65, 2100,
        ["Baltit Fort", "Altit Fort", "Eagle’s Nest"],
        [("Serena Altit", 16000, 4.7), ("Hunza Embassy", 9500, 4.2)]),
    "Skardu":    (35.29, 75.68, 2100,
        ["Shangrila Lake", "Deosai Plains"],
        [("Shangrila Resort", 18000, 4.6), ("Hotel Reego", 8000, 4.0)]),
    "Gilgit":    (35.92, 74.30, 1900,
        ["Naltar Valley", "Kargah Buddha"],
        [("Serena Gilgit", 15000, 4.4), ("Madina Hotel-2", 6000, 3.8)]),
    "Chitral":   (35.85, 71.78, 1800,
        ["Kalash Valley", "Chitral Fort"],
        [("Tirich Mir View", 7000, 4.0)]),
    "Sialkot":   (32.50, 74.53, 1500,
        ["Iqbal Manzil"],
        [("Hotel Javson", 9000, 4.1)]),
    "Gujranwala":(32.16, 74.18, 1500,
        ["Sheranwala Bagh"],
        [("Marian Hotel", 5500, 3.7)]),
    "Mardan":    (34.20, 72.05, 1500,
        ["Takht-i-Bahi"],
        [("Shelton House", 6000, 3.9)]),
    "Kasur":     (31.12, 74.45, 1400,
        ["Shrine Bulleh Shah"],
        [("Royal City", 4000, 3.5)]),
    "Muzaffarabad":(34.37, 73.47, 1700,
        ["Pir Chinasi"],
        [("Neelum View", 6500, 4.0)]),
    "Kalat":     (29.03, 66.59, 1400,
        ["Meeri Kal’at"],
        [("Sadaf Inn", 4000, 3.4)]),
    "Khuzdar":   (27.80, 66.64, 1400,
        ["Chotok Waterfall"],
        [("Galaxy Hotel", 3500, 3.3)]),
    "D.I. Khan": (31.83, 70.90, 1400,
        ["Gomal Zoo"],
        [("Al Haram Hotel", 4000, 3.4)]),
    "D.G. Khan": (30.06, 70.64, 1400,
        ["Fort Munro"],
        [("Shangrila DGK", 5000, 3.6)])
}

REASON_NOTE = {
    "relax":     "Light itinerary with ample rest and scenic views.",
    "business":  "Stay near commercial hubs and allocate time for meetings.",
    "adventure": "Include hiking and outdoor thrills.",
    "culture":   "Focus on heritage sites, museums and local cuisine."
}

# ------------------------------------------------------------------
# 2  HELPERS
# ------------------------------------------------------------------
def haversine_km(a, b):
    lat1, lon1 = CITY[a][:2]; lat2, lon2 = CITY[b][:2]
    R, p = 6371, math.pi/180
    return 2*R*math.asin(math.sqrt(
        math.sin((lat2-lat1)*p/2)**2 +
        math.cos(lat1*p)*math.cos(lat2*p)*math.sin((lon2-lon1)*p/2)**2))

def transport_cost(a, b, persons):        # Rs 3 per km per person
    return int(haversine_km(a, b) * 3 * persons)

def select_hotel(city, persons, budget_left):
    for name, price, rating in sorted(CITY[city][4], key=lambda h: h[1]):
        if price*math.ceil(persons/2) <= budget_left*0.6:
            return name, price, rating
    return CITY[city][4][0]                          # fallback cheapest

def build_plan(start, dest, persons, budget, reason):
    t_cost = transport_cost(start, dest, persons)
    if t_cost >= budget:
        return {"error": "Budget is lower than round-trip transport cost (Rs {})".format(t_cost)}
    avail = budget - t_cost
    hotel_name, hotel_price, rating = select_hotel(dest, persons, avail)
    daily_misc = CITY[dest][2] * persons
    days = max(1, avail // (hotel_price + daily_misc))
    return {
        "start": start, "dest": dest, "persons": persons, "budget": budget,
        "transport": t_cost, "hotel": hotel_name, "hotel_price": hotel_price,
        "rating": rating, "days": days, "sights": ", ".join(CITY[dest][3]),
        "note": REASON_NOTE[reason]
    }

# ------------------------------------------------------------------
# 3  BASE LAYOUT (Bootstrap 5)
# ------------------------------------------------------------------
LAYOUT = """
<!doctype html><html lang="en"><head>
<title>{{title}}</title>
<meta charset="utf-8">
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
<style>
body{padding-top:4.2rem;background:#eef4fa;font-family:"Segoe UI",sans-serif}
footer{margin-top:4rem;padding:1.2rem 0;background:#dfe7ed}
.navbar-brand{font-weight:600;font-size:1.3rem}
</style></head><body>
<nav class="navbar navbar-expand-lg navbar-dark bg-primary fixed-top">
 <div class="container">
  <a class="navbar-brand" href="/">AI Travel Planner</a>
  <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#nav">
   <span class="navbar-toggler-icon"></span>
  </button>
  <div class="collapse navbar-collapse" id="nav">
   <ul class="navbar-nav ms-auto">
    <li class="nav-item"><a class="nav-link {%if active=='home'%}active{%endif%}" href="/">Home</a></li>
    <li class="nav-item"><a class="nav-link {%if active=='plan'%}active{%endif%}" href="/plan">Plan Trip</a></li>
    <li class="nav-item"><a class="nav-link {%if active=='about'%}active{%endif%}" href="/about">About</a></li>
   </ul>
  </div>
 </div>
</nav>
<div class="container mt-4">{{content|safe}}</div>
<footer class="text-center"><small>&copy; {{now.year}} AI Travel Planner</small></footer>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
</body></html>
"""

# ------------------------------------------------------------------
# 4  PAGE FRAGMENTS
# ------------------------------------------------------------------
HOME_HTML = """
<div class="p-5 bg-light rounded-3 text-center border shadow-sm">
 <h1 class="display-5 fw-bold">Discover Pakistan on Your Terms</h1>
 <p class="lead">Enter your preferences and get a ready-made itinerary that fits your budget.</p>
 <a class="btn btn-success btn-lg" href="/plan">Start Planning</a>
</div>
"""

FORM_HTML = """
<h2 class="mb-4">Plan Your Trip</h2>
<form method="post" class="row g-3">
 <div class="col-md-6">
  <label class="form-label">Current City</label>
  <select name="start" class="form-select" required>
   <option value="" disabled selected>Select...</option>
   {%for c in cities%}<option>{{c}}</option>{%endfor%}
  </select>
 </div>
 <div class="col-md-6">
  <label class="form-label">Destination City</label>
  <select name="dest" class="form-select" required>
   <option value="" disabled selected>Select...</option>
   {%for c in cities%}<option>{{c}}</option>{%endfor%}
  </select>
 </div>
 <div class="col-md-4">
  <label class="form-label">Budget (Rs)</label>
  <input type="number" name="budget" class="form-control" min="5000" step="500" required>
 </div>
 <div class="col-md-4">
  <label class="form-label">Persons</label>
  <input type="number" name="persons" class="form-control" min="1" max="10" value="1" required>
 </div>
 <div class="col-md-4">
  <label class="form-label">Reason</label>
  <select name="reason" class="form-select">
   {%for r in reasons%}<option value="{{r}}">{{r.capitalize()}}</option>{%endfor%}
  </select>
 </div>
 <div class="col-12"><button class="btn btn-primary" type="submit">Generate Plan</button></div>
</form>

{% if plan %}
<hr>
{% if plan.error %}
<div class="alert alert-danger">{{plan.error}}</div>
{% else %}
<div class="card shadow-sm">
 <div class="card-body">
  <h4 class="card-title mb-3">Suggested {{plan.days}}-day itinerary for {{plan.dest}}</h4>
  <ul class="list-group list-group-flush">
   <li class="list-group-item">Round-trip transport: <strong>Rs {{plan.transport}}</strong></li>
   <li class="list-group-item">Hotel: <strong>{{plan.hotel}}</strong> – Rs {{plan.hotel_price}}/night (rating {{plan.rating}}★)</li>
   <li class="list-group-item">Key sights: {{plan.sights}}</li>
   <li class="list-group-item">{{plan.note}}</li>
  </ul>
 </div>
</div>
{% endif %}
{% endif %}
"""

ABOUT_HTML = """
<div class="bg-white p-4 rounded shadow-sm">
 <h2>About Us</h2>
 <p>At WanderScape, we believe that travel is more than just visiting new places – it's about experiencing the world in a way that inspires, educates, and connects people. Our mission is to make every journey memorable by offering reliable travel information, expert tips, and handpicked destinations that cater to all types of explorers.

Whether you’re planning a weekend getaway, a solo backpacking adventure, or a luxurious vacation, we’re here to guide you every step of the way. From travel itineraries and destination guides to packing tips and cultural insights, our content is designed to help you travel smarter and better.

Our team of travel enthusiasts and writers is constantly on the move to bring you the most up-to-date and trustworthy travel inspiration. Join our community of adventurers and start discovering the world—one unforgettable trip at a time.</p>
</div>
"""

# ------------------------------------------------------------------
# 5  RENDERING SHORTCUT
# ------------------------------------------------------------------
def render(page_html, **ctx):
    inner = render_template_string(page_html, **ctx)
    return render_template_string(LAYOUT, content=inner,
        title=ctx.get("title","AI Travel Planner"), active=ctx.get("active","home"),
        now=datetime.now())

# ------------------------------------------------------------------
# 6  ROUTES
# ------------------------------------------------------------------
@app.route('/')
def home():  return render(HOME_HTML, active="home", title="AI Travel Planner")

@app.route('/plan', methods=['GET', 'POST'])
def plan():
    plan_data = None
    if request.method == 'POST':
        start = request.form.get('start'); dest = request.form.get('dest')
        if not start or not dest or start == dest:                              # basic validation
            return redirect(url_for('plan'))
        try:
            budget  = int(request.form.get('budget', 0))
            persons = int(request.form.get('persons', 1))
        except ValueError:
            return redirect(url_for('plan'))
        reason  = request.form.get('reason', 'relax')
        plan_data = build_plan(start, dest, persons, budget, reason)
    return render(FORM_HTML, active="plan", title="Plan Trip",
                  cities=sorted(CITY.keys()), reasons=REASON_NOTE, plan=plan_data)

@app.route('/about')
def about(): return render(ABOUT_HTML, active="about", title="About")

# ------------------------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)
