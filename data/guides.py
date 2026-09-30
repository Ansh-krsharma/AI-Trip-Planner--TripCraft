"""The knowledge base: one ~200-300 word guide per destination.

Each entry also carries a (lat, lon) pair so the weather tool doesn't need a
separate geocoding call, and a rough per-day budget band so the planner has
real numbers to ground its cost estimates in instead of guessing.

Replace or extend this list with your own research and your own wording --
it is written from general knowledge as a starting point, not copied from
any source, and you should treat it the same way: your own words, your own
numbers.
"""

GUIDES = [
    {
        "destination": "Goa",
        "best_season": "November to February",
        "budget_level": "low to medium",
        "coords": (15.2993, 74.1240),
        "typical_cost_per_day_inr": {"low": 1500, "medium": 3500, "high": 8000},
        "text": (
            "Goa is India's smallest state, known for its beaches, Portuguese-era "
            "churches and relaxed pace. North Goa (Baga, Calangute, Anjuna) has the "
            "liveliest beach shacks, flea markets and nightlife; South Goa (Palolem, "
            "Agonda) is quieter and better for unwinding. Old Goa's Basilica of Bom "
            "Jesus and Se Cathedral are UNESCO-listed. Food centres on seafood -- "
            "prawn balchao, fish curry rice and bebinca for dessert. Best season is "
            "November to February, when the weather is dry and cool; the monsoon "
            "(June to September) closes many beach shacks. Budget travellers can "
            "manage on shared guesthouses and local thalis; mid-range trips add a "
            "scooter rental and beach-shack meals. Safety tips: rent from licensed "
            "operators, always wear a helmet, and avoid swimming during red-flag "
            "warnings, as rip currents are common. Sample 3-day plan: Day 1, Baga "
            "and Calangute beaches plus the Saturday Night Market; Day 2, Old Goa "
            "churches, a spice plantation tour and sunset at Fort Aguada; Day 3, a "
            "South Goa day trip to Palolem with a boat ride to spot dolphins."
        ),
    },
    {
        "destination": "Jaipur",
        "best_season": "October to March",
        "budget_level": "low to medium",
        "coords": (26.9124, 75.7873),
        "typical_cost_per_day_inr": {"low": 1200, "medium": 3000, "high": 7000},
        "text": (
            "Jaipur, the Pink City, is the gateway to Rajasthan. The City Palace, "
            "Jantar Mantar observatory and Hawa Mahal sit inside the old walled "
            "city; Amer Fort and Nahargarh Fort overlook it from the hills nearby. "
            "Local food includes dal baati churma, pyaaz kachori and ghewar. "
            "Bazaars such as Johari and Bapu Bazaar are known for gemstones, block "
            "prints and leather juttis -- bargaining is expected. Best season is "
            "October to March; summers (April to June) regularly cross 40C. A "
            "budget trip means shared autos and hostel stays; a medium budget adds "
            "a half-day car with driver for the forts. Safety tips: agree on auto "
            "and taxi fares before starting, and use a government-approved guide "
            "at Amer Fort to avoid overcharging touts. Sample 3-day plan: Day 1, "
            "City Palace, Jantar Mantar and Hawa Mahal; Day 2, Amer Fort by "
            "morning, Jal Mahal viewpoint and Bapu Bazaar in the evening; Day 3, "
            "Nahargarh Fort at sunset and a day trip option to Abhaneri stepwell."
        ),
    },
    {
        "destination": "Udaipur",
        "best_season": "September to March",
        "budget_level": "medium",
        "coords": (24.5854, 73.7125),
        "typical_cost_per_day_inr": {"low": 1500, "medium": 4000, "high": 10000},
        "text": (
            "Udaipur, the City of Lakes, is built around Lake Pichola and Fateh "
            "Sagar Lake, with the City Palace complex on the eastern shore. "
            "Jagmandir and the lake-island Taj Lake Palace are best seen from a "
            "sunset boat ride. Saheliyon ki Bari gardens and Bagore ki Haveli, "
            "which hosts an evening Rajasthani folk dance show, are popular half-"
            "day stops. Local food leans vegetarian -- dal baati, gatte ki sabzi "
            "and kachori. Best season is September to March for pleasant lake-"
            "side evenings; May and June are hot. A medium budget covers a "
            "heritage-style guesthouse with a lake view and a boat ride; budget "
            "travellers can stay just outside the old city and still walk in. "
            "Safety tips: book the sunset boat ride in advance in peak season, "
            "and confirm whether your hotel view is of the lake or a side street "
            "before paying a premium. Sample 3-day plan: Day 1, City Palace "
            "complex and a Lake Pichola sunset boat ride; Day 2, Saheliyon ki "
            "Bari, Bagore ki Haveli and the evening dance show; Day 3, Fateh "
            "Sagar Lake, Sajjangarh (Monsoon Palace) viewpoint at dusk."
        ),
    },
    {
        "destination": "Manali",
        "best_season": "March to June, and December for snow",
        "budget_level": "medium",
        "coords": (32.2396, 77.1887),
        "typical_cost_per_day_inr": {"low": 1800, "medium": 4000, "high": 9000},
        "text": (
            "Manali sits in the Kullu Valley in Himachal Pradesh and is a base "
            "for both easy sightseeing and serious mountain adventure. Old Manali "
            "has cafes, guesthouses and the Manu Temple; Solang Valley offers "
            "paragliding and zorbing in summer and skiing in winter. Rohtang Pass "
            "and Atal Tunnel lead toward Lahaul, though Rohtang often needs a "
            "permit and closes in heavy snow. Local food mixes Himachali dishes "
            "like siddu and dham with the backpacker cafes' pasta and pizza. Best "
            "season is March to June for clear valley views and pleasant trekking "
            "weather; December brings snow but colder, sometimes icy roads. A "
            "medium budget covers a valley-view guesthouse and one adventure "
            "activity; budget trips skip Solang's paid activities. Safety tips: "
            "check road and permit status for Rohtang before planning that day, "
            "and carry warm layers even in summer once above Solang. Sample "
            "3-day plan: Day 1, Old Manali cafes and Hadimba Temple; Day 2, "
            "Solang Valley activities; Day 3, Atal Tunnel and Sissu, or a short "
            "trek toward Jogini Falls."
        ),
    },
    {
        "destination": "Rishikesh",
        "best_season": "September to April",
        "budget_level": "low",
        "coords": (30.0869, 78.2676),
        "typical_cost_per_day_inr": {"low": 1000, "medium": 2500, "high": 6000},
        "text": (
            "Rishikesh, on the banks of the Ganga in Uttarakhand, is known as a "
            "centre for yoga and river adventure. Laxman Jhula and Ram Jhula "
            "footbridges connect the two riverbanks, and the Parmarth Niketan "
            "evening Ganga Aarti draws large crowds. Rafting trips typically run "
            "from Shivpuri or Brahmpuri down to Rishikesh, graded by rapid "
            "difficulty. Cafes along the river serve mostly vegetarian, no-onion-"
            "no-garlic ashram-style food alongside backpacker favourites. Best "
            "season is September to April; rafting is usually closed during the "
            "monsoon (July-August) when the river runs high. Rishikesh is one of "
            "the most budget-friendly stops in this guide -- shared dorms, cheap "
            "thalis and free or donation-based yoga sessions are common. Safety "
            "tips: book rafting only through registered operators with life "
            "jackets and a certified guide, and check the river's current grade "
            "before booking in monsoon shoulder months. Sample 3-day plan: Day 1, "
            "Laxman Jhula, Ram Jhula and the evening Ganga Aarti; Day 2, white-"
            "water rafting followed by a riverside cafe evening; Day 3, a short "
            "yoga or meditation session and a walk to Neelkanth Mahadev Temple."
        ),
    },
    {
        "destination": "Varanasi",
        "best_season": "October to March",
        "budget_level": "low",
        "coords": (25.3176, 82.9739),
        "typical_cost_per_day_inr": {"low": 1000, "medium": 2500, "high": 6000},
        "text": (
            "Varanasi, on the Ganga in Uttar Pradesh, is among the oldest "
            "continuously inhabited cities in the world and a major pilgrimage "
            "site. The ghats -- Dashashwamedh, Assi and Manikarnika among them -- "
            "line the river, and the Dashashwamedh Ganga Aarti at dusk is the "
            "city's signature evening ritual. A sunrise boat ride past the ghats "
            "is the classic way to see the city wake up. Kashi Vishwanath Temple "
            "and the narrow lanes of the old city are worth a half day; Sarnath, "
            "where the Buddha gave his first sermon, is a short trip out of town. "
            "Street food includes kachori-sabzi, chaat and the local lassi. Best "
            "season is October to March; summers are very hot and humid. This is "
            "a budget-friendly city -- guesthouses near the ghats, boat rides and "
            "street food keep daily costs low. Safety tips: agree on the boatman's "
            "fare before boarding, and be respectful and unobtrusive near "
            "cremation ghats, which are active religious sites, not photo stops. "
            "Sample 3-day plan: Day 1, sunrise boat ride and the ghats; Day 2, "
            "Kashi Vishwanath Temple and old-city lanes; Day 3, a half-day trip "
            "to Sarnath and the evening Ganga Aarti."
        ),
    },
    {
        "destination": "Hampi",
        "best_season": "October to February",
        "budget_level": "low",
        "coords": (15.3350, 76.4600),
        "typical_cost_per_day_inr": {"low": 1000, "medium": 2500, "high": 5500},
        "text": (
            "Hampi, in Karnataka, was the capital of the Vijayanagara Empire and "
            "is now a UNESCO World Heritage boulder-strewn ruin field. The "
            "Virupaksha Temple, Vittala Temple with its stone chariot, and the "
            "Royal Enclosure are the major sights, spread over a large area best "
            "covered by rented bicycle or scooter. Sunset from Matanga Hill or "
            "Hemakuta Hill over the boulder landscape is a highlight. The river "
            "side (Hampi Island, across the Tungabhadra) has a quieter, more "
            "laid-back cafe scene. Local food is simple South Indian thalis and "
            "cafe fare aimed at backpackers. Best season is October to February "
            "for cooler days spent walking between ruins; summers are very hot "
            "with little shade among the boulders. This is a low-cost "
            "destination -- guesthouses, bicycle rental and thali meals keep "
            "spending modest. Safety tips: carry water and sun protection since "
            "shade is scarce between sites, and check coracle-crossing timings to "
            "Hampi Island before sunset. Sample 3-day plan: Day 1, Virupaksha "
            "Temple and Hampi Bazaar; Day 2, Vittala Temple, the stone chariot "
            "and Royal Enclosure by bicycle; Day 3, Hampi Island cafes and sunset "
            "from Matanga Hill."
        ),
    },
    {
        "destination": "Mysuru",
        "best_season": "October to February",
        "budget_level": "low to medium",
        "coords": (12.2958, 76.6394),
        "typical_cost_per_day_inr": {"low": 1200, "medium": 3000, "high": 6500},
        "text": (
            "Mysuru (Mysore), in Karnataka, is known for the Mysore Palace, its "
            "silk sarees and sandalwood, and the Dasara festival. The palace is "
            "illuminated on Sunday evenings and during Dasara, when nearly a "
            "hundred thousand lights outline the building. Chamundi Hill, with "
            "the Chamundeshwari Temple and a giant Nandi statue partway up, "
            "overlooks the city. Nearby, Brindavan Gardens offers a musical "
            "fountain show in the evening. Local food includes Mysore masala "
            "dosa, Mysore pak and filter coffee. Best season is October to "
            "February, which also covers the Dasara festival period, though "
            "hotel prices rise sharply then. A medium budget covers a "
            "centrally located hotel and a half-day car for the palace and "
            "Chamundi Hill; budget travellers can use city buses and autos. "
            "Safety tips: book palace-illumination viewing early during Dasara "
            "as crowds are heavy, and confirm Brindavan Gardens' fountain-show "
            "schedule before travelling out, since timings vary by season. "
            "Sample 3-day plan: Day 1, Mysore Palace by day and its evening "
            "illumination; Day 2, Chamundi Hill and the city's markets for silk "
            "and sandalwood; Day 3, a day trip to Brindavan Gardens and "
            "Srirangapatna's Ranganathaswamy Temple."
        ),
    },
    {
        "destination": "Pondicherry",
        "best_season": "November to February",
        "budget_level": "medium",
        "coords": (11.9416, 79.8083),
        "typical_cost_per_day_inr": {"low": 1500, "medium": 3500, "high": 8000},
        "text": (
            "Pondicherry (Puducherry), on Tamil Nadu's coast, keeps a French "
            "colonial character in its White Town -- mustard-yellow villas, "
            "bougainvillea-lined streets and beachfront cafes along Rock Beach "
            "promenade. The Sri Aurobindo Ashram and, a short drive out, "
            "Auroville's Matrimandir draw visitors interested in its "
            "spiritual community, though Matrimandir viewing requires advance "
            "registration. Food mixes French-influenced cafe menus with South "
            "Indian and Tamil dishes. Best season is November to February; "
            "summers are hot and humid on the coast. A medium budget covers a "
            "heritage guesthouse in White Town and cafe meals; a rented scooter "
            "makes Auroville and nearby beaches easy day trips. Safety tips: "
            "book an Auroville visitor pass online ahead of time, since walk-in "
            "access to Matrimandir's inner chamber is limited, and be cautious "
            "swimming at Auroville and Paradise beaches, which can have strong "
            "currents. Sample 3-day plan: Day 1, White Town streets and Rock "
            "Beach promenade; Day 2, Auroville and Matrimandir viewing point; "
            "Day 3, Sri Aurobindo Ashram and a beach afternoon at Paradise "
            "Beach."
        ),
    },
    {
        "destination": "Coorg",
        "best_season": "October to March",
        "budget_level": "medium",
        "coords": (12.4244, 75.7382),
        "typical_cost_per_day_inr": {"low": 1800, "medium": 4000, "high": 9000},
        "text": (
            "Coorg (Kodagu), in Karnataka's Western Ghats, is a hill district "
            "known for coffee plantations, waterfalls and misty viewpoints. "
            "Abbey Falls and Iruppu Falls are the most-visited waterfalls; "
            "Raja's Seat and Mandalpatti are popular sunrise and sunset "
            "viewpoints over the hills. A coffee-plantation walk or tour, often "
            "run by homestays, explains how the region's Arabica and Robusta "
            "are grown and processed. Local Kodava cuisine includes pandi curry "
            "(pork) and akki roti. Best season is October to March for clear "
            "viewpoints and comfortable trekking weather; the monsoon (June to "
            "September) is very heavy here and many viewpoint roads become "
            "slippery. A medium budget covers a plantation-stay homestay and a "
            "jeep trip to Mandalpatti, whose last stretch is only accessible by "
            "4x4. Safety tips: book a jeep for Mandalpatti rather than driving a "
            "regular car up the final unpaved stretch, and check waterfall "
            "safety barriers and flow before monsoon-season visits. Sample "
            "3-day plan: Day 1, Abbey Falls and a coffee-plantation walk; Day 2, "
            "Mandalpatti viewpoint by jeep and Raja's Seat at sunset; Day 3, "
            "Iruppu Falls and the Nagarhole forest fringe."
        ),
    },
]

DESTINATION_NAMES = [g["destination"] for g in GUIDES]
COORDS_BY_DESTINATION = {g["destination"].lower(): g["coords"] for g in GUIDES}
