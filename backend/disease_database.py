# Comprehensive Disease Database with Risk Levels, Treatments, and Recommendations
DISEASE_DATABASE = {
    # SKIN DISEASES (22 types)
    'Acne': {
        'risk_level': 'Low',
        'description': 'Common skin condition with pimples, blackheads, and whiteheads',
        'medications': [
            'Benzoyl Peroxide 2.5-10%',
            'Salicylic Acid 0.5-2%',
            'Adapalene (Differin)',
            'Isotretinoin (for severe cases)',
            'Oral Antibiotics (Doxycycline, Minocycline)'
        ],
        'treatments': [
            'Regular face washing with mild soap',
            'Avoid touching face',
            'Use non-comedogenic products',
            'Chemical peels (Glycolic or Salicylic acid)',
            'Laser therapy for severe scarring'
        ],
        'home_remedies': [
            'Tea tree oil (diluted)',
            'Honey masks',
            'Aloe vera gel',
            'Ice compress for inflammation',
            'Green tea topical application'
        ],
        'diet_advice': [
            'Reduce high-glycemic foods',
            'Avoid dairy and fatty foods',
            'Increase water intake (8-10 glasses/day)',
            'Include antioxidant-rich foods',
            'Omega-3 fatty acids (fish, flaxseed)'
        ],
        'activities': [
            'Light exercise (30 mins daily)',
            'Yoga for stress management',
            'Swimming with proper hygiene',
            'Walking in morning sunlight',
            'Stress-reducing activities (meditation)'
        ],
        'duration': '4-8 weeks for visible improvement'
    },
    'Psoriasis': {
        'risk_level': 'Medium',
        'description': 'Autoimmune condition causing thick, silvery scales on skin',
        'medications': [
            'Topical Corticosteroids',
            'Vitamin D analogs (Calcipotriene)',
            'Retinoids (Tretinoin)',
            'TNF inhibitors (Biological therapy)',
            'Methotrexate (for severe cases)'
        ],
        'treatments': [
            'Phototherapy (UVB or PUVA therapy)',
            'Topical treatments',
            'Moisturizing regularly',
            'Tar-based treatments',
            'Systemic therapy for severe cases'
        ],
        'home_remedies': [
            'Oatmeal baths',
            'Coconut oil application',
            'Aloe vera gel',
            'Apple cider vinegar soaks',
            'Turmeric paste'
        ],
        'diet_advice': [
            'Anti-inflammatory diet',
            'Limit gluten intake',
            'Reduce alcohol consumption',
            'Omega-3 rich foods',
            'Avoid triggers (spicy, fatty foods)'
        ],
        'activities': [
            'Light yoga (non-stressful)',
            '30 minutes daily walking',
            'Swimming in heated pools',
            'Stress management meditation',
            'Regular stretching'
        ],
        'duration': '2-6 weeks for flare reduction'
    },
    'Eczema': {
        'risk_level': 'Low',
        'description': 'Inflammatory skin condition causing itching, redness, and cracking',
        'medications': [
            'Topical Corticosteroids',
            'Topical Calcineurin inhibitors',
            'Antihistamines (for itching)',
            'Emollients/Moisturizers',
            'Dupilumab (Biologic)'
        ],
        'treatments': [
            'Regular moisturizing',
            'Avoid irritants and allergens',
            'Use gentle cleansers',
            'Topical steroid creams',
            'Phototherapy for severe cases'
        ],
        'home_remedies': [
            'Coconut oil',
            'Oatmeal baths',
            'Aloe vera',
            'Honey application',
            'Avoid hot water baths'
        ],
        'diet_advice': [
            'Identify food triggers',
            'Include omega-3 foods',
            'Stay hydrated',
            'Avoid excessive sugar',
            'Probiotic-rich foods'
        ],
        'activities': [
            'Light exercise without sweating',
            'Yoga for relaxation',
            '20-30 minutes daily walking',
            'Swimming in chlorine-free water',
            'Stress reduction techniques'
        ],
        'duration': '1-2 weeks for itch relief'
    },
    'Rosacea': {
        'risk_level': 'Low',
        'description': 'Chronic condition causing facial redness and visible blood vessels',
        'medications': [
            'Topical Metronidazole',
            'Azelaic Acid',
            'Oral Antibiotics (Doxycycline, Minocycline)',
            'Sulfacetamide-Sulfur',
            'Laser therapy'
        ],
        'treatments': [
            'Sun protection (SPF 30+)',
            'Gentle skincare routine',
            'Avoid triggers',
            'Laser/IPL therapy',
            'Topical vasoconstrictors'
        ],
        'home_remedies': [
            'Chamomile tea compress',
            'Aloe vera gel',
            'Green tea extract',
            'Honey face masks',
            'Licorice extract application'
        ],
        'diet_advice': [
            'Avoid spicy foods',
            'Limit alcohol (especially red wine)',
            'Avoid hot beverages',
            'Anti-inflammatory foods',
            'Include antioxidants'
        ],
        'activities': [
            'Indoor exercise preferred',
            'Gentle yoga',
            'Swimming in cool water',
            'Walking during cooler times',
            'Stress management'
        ],
        'duration': '3-4 weeks for improvement'
    },
    'Vitiligo': {
        'risk_level': 'Low',
        'description': 'Loss of skin pigmentation causing white patches',
        'medications': [
            'Topical Corticosteroids',
            'Topical Calcineurin inhibitors',
            'JAK inhibitors (Ruxolitinib)',
            'Oral Corticosteroids',
            'Phototherapy agents'
        ],
        'treatments': [
            'Phototherapy (NB-UVB)',
            'Excimer laser',
            'Surgical grafting',
            'Depigmentation (for extensive vitiligo)',
            'Cosmetic camouflage'
        ],
        'home_remedies': [
            'Turmeric and coconut oil paste',
            'Neem oil application',
            'Ginger and turmeric paste',
            'Mustard oil massage',
            'Basil leaves application'
        ],
        'diet_advice': [
            'Copper-rich foods (mushrooms, almonds)',
            'Vitamin B12 supplements',
            'Increase antioxidants',
            'Vitamin D from sunlight',
            'Iron-rich foods'
        ],
        'activities': [
            'Morning sun exposure (10-15 mins)',
            'Light yoga',
            'Walking',
            'Stress reduction (important)',
            'Swimming with sunscreen'
        ],
        'duration': '3-6 months for visible improvement'
    },
    'SkinCancer': {
        'risk_level': 'High',
        'description': 'Malignant skin lesion - REQUIRES IMMEDIATE MEDICAL ATTENTION',
        'medications': [
            'URGENT: Consult Dermatologist/Oncologist',
            'Immunotherapy drugs (Pembrolizumab, Nivolumab)',
            'Targeted therapy based on mutation',
            'Chemotherapy agents'
        ],
        'treatments': [
            'IMMEDIATE MEDICAL CONSULTATION REQUIRED',
            'Surgical excision with margins',
            'Mohs micrographic surgery',
            'Radiation therapy',
            'Immunotherapy or targeted therapy'
        ],
        'home_remedies': [
            'No home treatment - MEDICAL EMERGENCY',
            'Follow doctor\'s post-treatment care',
            'Proper wound care',
            'Sun protection absolutely critical'
        ],
        'diet_advice': [
            'Consult oncologist for nutrition plan',
            'Anti-inflammatory diet',
            'High protein intake',
            'Adequate vitamin D',
            'Antioxidant-rich foods'
        ],
        'activities': [
            'Rest per medical advice',
            'Avoid sun exposure completely',
            'Gentle activities as cleared by doctor',
            'Mental health support recommended',
            'Regular follow-ups mandatory'
        ],
        'duration': 'Variable - Requires ongoing treatment'
    },
    'Warts': {
        'risk_level': 'Low',
        'description': 'Benign skin growth caused by HPV virus',
        'medications': [
            'Salicylic Acid (Over-the-counter)',
            'Imiquimod',
            'Podofilox',
            'Cryotherapy (Liquid nitrogen)',
            'Laser removal'
        ],
        'treatments': [
            'Cryotherapy (freezing)',
            'Laser therapy',
            'Chemical peels',
            'Electrocautery',
            'Surgical removal'
        ],
        'home_remedies': [
            'Salicylic acid application',
            'Tea tree oil',
            'Apple cider vinegar',
            'Duct tape occlusion',
            'Garlic application'
        ],
        'diet_advice': [
            'Boost immune system',
            'Vitamin C-rich foods',
            'Zinc-rich foods (oysters, beef)',
            'Iron-rich foods',
            'Antioxidant-rich vegetables'
        ],
        'activities': [
            'Regular exercise (boosts immunity)',
            'Yoga and meditation',
            'Walking 30 minutes daily',
            'Stress management',
            'Proper hygiene'
        ],
        'duration': '2-8 weeks depending on treatment'
    },
    'Moles': {
        'risk_level': 'Low',
        'description': 'Common benign skin growth from pigment cells',
        'medications': [
            'No medication needed for benign moles',
            'Removal agents if cosmetically desired',
            'Regular monitoring important'
        ],
        'treatments': [
            'Observation (safe if stable)',
            'Laser removal',
            'Surgical excision',
            'Chemical peels'
        ],
        'home_remedies': [
            'Regular monitoring for changes',
            'Apple cider vinegar application',
            'Onion juice application',
            'Castor oil with baking soda',
            'Garlic paste application'
        ],
        'diet_advice': [
            'Antioxidant-rich foods',
            'Vitamin E (nuts, seeds)',
            'Vitamin C (citrus, berries)',
            'Sun protection through diet',
            'Regular green tea consumption'
        ],
        'activities': [
            'Sun protection (SPF 30+ daily)',
            'Regular skin check',
            'Avoid UV exposure',
            'Gentle outdoor activities',
            'PhotoCheck monitoring every 6 months'
        ],
        'duration': 'Continuous monitoring required'
    },
    'Actinic_Keratosis': {
        'risk_level': 'Medium',
        'description': 'Precancerous lesion from sun damage - Monitor closely',
        'medications': [
            'Fluorouracil (5-FU cream)',
            'Imiquimod',
            'Diclofenac gel',
            'Ingenol mebutate',
            'Topical retinoids'
        ],
        'treatments': [
            'Cryotherapy (primary option)',
            'Laser therapy',
            'Chemical peels',
            'Photodynamic therapy',
            'Topical medications'
        ],
        'home_remedies': [
            'Regular sun protection',
            'Avoid known triggers',
            'Vitamin E oil application',
            'Aloe vera for irritated skin',
            'Follow medical treatment'
        ],
        'diet_advice': [
            'Antioxidant-rich foods',
            'Vitamin D supplementation',
            'Vitamin C foods',
            'Green tea',
            'Water intake (8-10 glasses)'
        ],
        'activities': [
            'Sun avoidance critical',
            'SPF 30+ daily application',
            'Light outdoor activities',
            'Regular skin examinations',
            'Protective clothing when outdoors'
        ],
        'duration': '2-4 weeks per treatment session'
    },
    'Candidate': {
        'risk_level': 'Low',
        'description': 'Fungal infection causing white patches or redness',
        'medications': [
            'Topical Antifungals (Clotrimazole, Miconazole)',
            'Oral Antifungals (Fluconazole, Terbinafine)',
            'Topical Corticosteroids',
            'Nystatin cream/powder'
        ],
        'treatments': [
            'Antifungal creams applied twice daily',
            'Keep area clean and dry',
            'Avoid moisture accumulation',
            'Use antifungal powder',
            'Topical treatments for 2-4 weeks'
        ],
        'home_remedies': [
            'Keep skin dry',
            'Tea tree oil application',
            'Apple cider vinegar soaks',
            'Coconut oil application',
            'Baking soda paste'
        ],
        'diet_advice': [
            'Reduce sugar intake',
            'Increase yogurt (probiotics)',
            'Garlic consumption',
            'Avoid yeast-rich foods',
            'Increase antifungal herbs (oregano, thyme)'
        ],
        'activities': [
            'Keep area dry and ventilated',
            'Avoid tight clothing',
            'Regular gentle exercise',
            'Sweat management important',
            'Proper hygiene maintenance'
        ],
        'duration': '2-4 weeks of treatment needed'
    },
    'Lichen': {
        'risk_level': 'Low',
        'description': 'Inflammatory skin condition with flat, purple bumps',
        'medications': [
            'Topical Corticosteroids',
            'Retinoids (Tretinoin)',
            'Topical Calcineurin inhibitors',
            'Oral Corticosteroids (severe cases)',
            'Antihistamines'
        ],
        'treatments': [
            'Topical steroid application',
            'Avoid irritants',
            'Regular moisturizing',
            'Phototherapy',
            'Oral medications for systemic involvement'
        ],
        'home_remedies': [
            'Aloe vera gel',
            'Oatmeal baths',
            'Coconut oil',
            'Licorice root paste',
            'Avoid scratching'
        ],
        'diet_advice': [
            'Anti-inflammatory diet',
            'Avoid spicy foods',
            'Increase vitamin C',
            'Omega-3 fatty acids',
            'Stress-reducing herbs'
        ],
        'activities': [
            'Stress management crucial',
            'Gentle yoga',
            'Light exercise',
            'Meditation',
            'Avoid triggers (stress, certain medications)'
        ],
        'duration': '2-6 weeks for improvement'
    },
    'Bullous': {
        'risk_level': 'Medium',
        'description': 'Condition characterized by large fluid-filled blisters',
        'medications': [
            'Topical/Oral Corticosteroids',
            'Topical Antibiotics (infection prevention)',
            'Immunosuppressants',
            'Doxycycline',
            'Intravenous Immunoglobulin'
        ],
        'treatments': [
            'Blister protection and care',
            'Topical steroid application',
            'Wound care to prevent infection',
            'Oral medications for systemic cases',
            'Phototherapy if indicated'
        ],
        'home_remedies': [
            'Avoid friction on blisters',
            'Padding and protective dressing',
            'Keep blisters clean and dry',
            'Aloe vera on healed areas',
            'Do not pop blisters'
        ],
        'diet_advice': [
            'Avoid foods that trigger blisters',
            'Increase antioxidants',
            'Vitamin C rich foods',
            'Zinc supplementation',
            'Anti-inflammatory foods'
        ],
        'activities': [
            'Avoid friction and injury',
            'Light, non-strenuous activities',
            'Proper clothing (soft, loose)',
            'Stress management',
            'Gentle activities as healing progresses'
        ],
        'duration': '2-4 weeks depending on severity'
    },
    'Benign_tumors': {
        'risk_level': 'Low',
        'description': 'Non-cancerous growths in skin tissue',
        'medications': [
            'Generally no medication needed',
            'Topical treatments if irritated',
            'Pain relief if needed'
        ],
        'treatments': [
            'Regular monitoring',
            'Surgical removal if desired',
            'Laser removal',
            'Freezing therapy'
        ],
        'home_remedies': [
            'Regular monitoring for changes',
            'Avoid irritation',
            'Vitamin E oil application',
            'Sun protection',
            'Keep area clean and dry'
        ],
        'diet_advice': [
            'Antioxidant-rich foods',
            'Vitamin D supplementation',
            'Balanced nutrition',
            'Adequate water intake',
            'Anti-inflammatory foods'
        ],
        'activities': [
            'Regular skin checks',
            'Sun protection',
            'Gentle outdoor activities',
            'Non-strenuous exercise',
            'Stress management'
        ],
        'duration': 'Continuous monitoring'
    },
    'DrugEruption': {
        'risk_level': 'Medium',
        'description': 'Skin reaction to medication or drug side effect',
        'medications': [
            'STOP causative drug immediately',
            'Topical Corticosteroids',
            'Oral Antihistamines',
            'Topical Moisturizers',
            'Alternative medications as prescribed'
        ],
        'treatments': [
            'Identify and discontinue offending drug',
            'Supportive care with topical therapy',
            'Oral antihistamines',
            'Systemic corticosteroids if severe',
            'Monitor for progression'
        ],
        'home_remedies': [
            'Cool compresses for itching',
            'Oatmeal baths',
            'Aloe vera application',
            'Moisturize regularly',
            'Avoid triggers'
        ],
        'diet_advice': [
            'Avoid known medication triggers',
            'Hydrate well',
            'Anti-inflammatory foods',
            'Avoid additives and dyes',
            'Increase antioxidants'
        ],
        'activities': [
            'Limited activities until improved',
            'Avoid sun exposure if photosensitive',
            'Gentle exercise',
            'Stress management',
            'Rest and recovery important'
        ],
        'duration': '1-3 weeks after drug discontinuation'
    },
    'Infestations_Bites': {
        'risk_level': 'Low',
        'description': 'Parasitic infection or insect bites causing itching and rash',
        'medications': [
            'Permethrin cream (for scabies)',
            'Oral Ivermectin',
            'Antifungals if secondary infection',
            'Antihistamines (itching)',
            'Topical Corticosteroids'
        ],
        'treatments': [
            'Antiparasitic treatment',
            'Wash all bedding and clothing',
            'Topical antiparasitic application',
            'Treat household members/close contacts',
            'Avoid scratching to prevent infection'
        ],
        'home_remedies': [
            'Neem oil application',
            'Tea tree oil (diluted)',
            'Sulfur cream',
            'Maintain excellent hygiene',
            'Keep nails short'
        ],
        'diet_advice': [
            'Boost immune system',
            'Increase garlic consumption',
            'Vitamin C rich foods',
            'Zinc-rich foods',
            'Antioxidant vegetables'
        ],
        'activities': [
            'Maintain strict hygiene',
            'Avoid close contact during treatment',
            'Regular laundry changes',
            'Light exercise as comfortable',
            'Stress reduction important'
        ],
        'duration': '1-2 weeks with treatment'
    },
    'Lupus': {
        'risk_level': 'High',
        'description': 'Autoimmune disease affecting skin and systemic organs',
        'medications': [
            'Hydroxychloroquine (first-line)',
            'Corticosteroids',
            'NSAIDs (Ibuprofen, Naproxen)',
            'Immunosuppressants',
            'Biologic agents (Belimumab)'
        ],
        'treatments': [
            'Regular rheumatologist follow-ups',
            'Sunscreen SPF 50+ daily',
            'Topical corticosteroids',
            'Photoprotection (clothing, umbrella)',
            'Systemic treatment as needed'
        ],
        'home_remedies': [
            'Strict sun avoidance',
            'Vitamin D supplementation',
            'Stress management crucial',
            'Adequate rest',
            'Ginger and turmeric (anti-inflammatory)'
        ],
        'diet_advice': [
            'Anti-inflammatory diet',
            'Omega-3 fatty acids (fish oil)',
            'Avoid alfalfa (triggers flares)',
            'Antioxidant-rich foods',
            'Limit alcohol consumption'
        ],
        'activities': [
            'Sun protection absolutely critical',
            'Gentle yoga',
            'Swimming indoors',
            'Stress management (meditation)',
            'Regular moderate exercise'
        ],
        'duration': 'Chronic - Ongoing management required'
    },
    'Vascular_Tumors': {
        'risk_level': 'Low',
        'description': 'Non-cancerous blood vessel growths (hemangiomas, port-wine stains)',
        'medications': [
            'Topical medications may help',
            'Beta-blockers if vasoproliferative lesion',
            'Pain management if painful'
        ],
        'treatments': [
            'Laser therapy (primary option)',
            'Surgical excision',
            'Sclerotherapy',
            'Observation for stable lesions',
            'Cosmetic coverage'
        ],
        'home_remedies': [
            'Regular monitoring for changes',
            'Protective cosmetic cover-up',
            'Avoid trauma to area',
            'Vitamin E application',
            'Sun protection'
        ],
        'diet_advice': [
            'Antioxidant-rich foods',
            'Vitamin E foods (nuts, oils)',
            'Vitamin C foods',
            'Adequate protein for healing',
            'Anti-inflammatory foods'
        ],
        'activities': [
            'Avoid trauma to affected area',
            'Gentle activities',
            'Sun protection',
            'Regular skin examinations',
            'Stress management'
        ],
        'duration': 'Variable - Some may resolve spontaneously'
    },
    'Vasculitis': {
        'risk_level': 'High',
        'description': 'Inflammation of blood vessels causing skin lesions',
        'medications': [
            'Corticosteroids (primary treatment)',
            'Immunosuppressants',
            'NSAIDs',
            'Antibiotics if related to infection',
            'Biologic agents in refractory cases'
        ],
        'treatments': [
            'Systemic corticosteroid therapy',
            'Address underlying cause',
            'Treat skin lesions topically',
            'Regular monitoring',
            'Immunosuppressive therapy if needed'
        ],
        'home_remedies': [
            'Rest and elevation',
            'Avoid triggers',
            'Cool compresses',
            'Support stockings if lower extremity',
            'Stress management'
        ],
        'diet_advice': [
            'Anti-inflammatory diet',
            'Omega-3 fatty acids',
            'Avoid allergens',
            'Antioxidant-rich foods',
            'Adequate protein intake'
        ],
        'activities': [
            'Rest important during flares',
            'Gentle activities as tolerated',
            'Elevation of affected areas',
            'Avoid heat exposure',
            'Stress reduction crucial'
        ],
        'duration': 'Variable - Depends on underlying cause'
    },
    'Seborrh_Keratoses': {
        'risk_level': 'Low',
        'description': 'Common benign growths appearing brown, black, or tan',
        'medications': [
            'No medication needed',
            'Topical treatments for irritation',
            'Optional removal methods'
        ],
        'treatments': [
            'Cryotherapy (freezing)',
            'Electrocautery',
            'Curettage (scraping)',
            'Laser removal',
            'Observation (safe, benign)'
        ],
        'home_remedies': [
            'Apple cider vinegar application',
            'Garlic paste application',
            'Vitamin E oil',
            'Castor oil with baking soda',
            'Avoid scratching or irritating'
        ],
        'diet_advice': [
            'Antioxidant-rich foods',
            'Vitamin E foods',
            'Vitamin C foods',
            'Adequate water intake',
            'Anti-aging antioxidants'
        ],
        'activities': [
            'Sun protection',
            'Regular skin monitoring',
            'Gentle outdoor activities',
            'Non-strenuous exercise',
            'Protective clothing in sun'
        ],
        'duration': 'Stable lesions - monitoring sufficient'
    },
    'Sun_Sunlight_Damage': {
        'risk_level': 'Medium',
        'description': 'Skin damage from UV exposure causing wrinkles, spots, and texture changes',
        'medications': [
            'Topical Retinoids (Tretinoin, Adapalene)',
            'Vitamin C serums',
            'Sunscreen SPF 30+',
            'Alpha Hydroxy Acids (AHA)',
            'Beta Hydroxy Acids (BHA)'
        ],
        'treatments': [
            'Strict sun avoidance',
            'Daily SPF 30+ sunscreen',
            'Laser resurfacing',
            'Chemical peels',
            'Microdermabrasion',
            'Topical retinoid therapy'
        ],
        'home_remedies': [
            'Daily sunscreen application',
            'Protective clothing',
            'Antioxidant serums',
            'Vitamin C and E oils',
            'Aloe vera for healed areas'
        ],
        'diet_advice': [
            'Antioxidant-rich foods (berries)',
            'Vitamin C foods (citrus)',
            'Vitamin E foods (nuts)',
            'Beta-carotene foods (carrots)',
            'Green tea consumption'
        ],
        'activities': [
            'Sun avoidance during peak hours (10 AM - 4 PM)',
            'Wear protective clothing',
            'Use SPF 30+ daily',
            'Avoid tanning beds',
            'Indoor exercise preferred'
        ],
        'duration': '6-12 weeks for visible improvement'
    },
    'Tinea': {
        'risk_level': 'Low',
        'description': 'Fungal infection causing ring-shaped rash (ringworm, athlete\'s foot)',
        'medications': [
            'Topical Antifungals (Terbinafine, Miconazole)',
            'Oral Antifungals (Terbinafine, Itraconazole)',
            'Topical Corticosteroids (if inflamed)',
            'Antifungal powders'
        ],
        'treatments': [
            'Topical antifungal application twice daily',
            'Keep area clean and dry',
            'Use antifungal powder',
            'Avoid moisture accumulation',
            'Oral treatment for stubborn cases'
        ],
        'home_remedies': [
            'Tea tree oil (diluted)',
            'Apple cider vinegar soaks',
            'Coconut oil application',
            'Salt water soaks',
            'Neem oil application'
        ],
        'diet_advice': [
            'Reduce sugar and yeast foods',
            'Increase garlic consumption',
            'Probiotics (yogurt)',
            'Antifungal herbs (oregano, thyme)',
            'Vitamin C foods'
        ],
        'activities': [
            'Keep area dry and ventilated',
            'Avoid tight clothing',
            'Regular exercise (not excessive sweating)',
            'Proper hygiene crucial',
            'Avoid shared items'
        ],
        'duration': '2-4 weeks of treatment needed'
    },
    'Unknown_Normal': {
        'risk_level': 'Low',
        'description': 'Normal skin with no identified disease',
        'medications': ['No medication needed'],
        'treatments': [
            'Maintain regular skincare routine',
            'Sun protection (SPF 15+)',
            'Moisturize daily',
            'Healthy lifestyle'
        ],
        'home_remedies': [
            'Daily cleansing',
            'Moisturizing',
            'Sun protection',
            'Antioxidant products'
        ],
        'diet_advice': [
            'Balanced diet',
            'Antioxidant-rich foods',
            'Adequate hydration',
            'Fruits and vegetables',
            'Healthy skin-supporting nutrients'
        ],
        'activities': [
            'Regular exercise',
            'Stress management',
            'Adequate sleep',
            'Sun protection outdoors',
            'Maintain healthy lifestyle'
        ],
        'duration': 'Preventive care ongoing'
    },

    # SYSTEMIC DISEASES (from symptoms data)
    'Diabetes': {
        'risk_level': 'High',
        'description': 'Blood sugar regulation disorder - High priority management needed',
        'medications': [
            'Metformin (first-line)',
            'Insulin (Type 1 and advanced Type 2)',
            'Sulfonylureas (Glibenclamide)',
            'DPP-4 inhibitors (Sitagliptin)',
            'SGLT2 inhibitors (Empagliflozin)'
        ],
        'treatments': [
            'Regular blood glucose monitoring',
            'Insulin therapy if needed',
            'Oral medications',
            'Dietary management',
            'Regular exercise program'
        ],
        'home_remedies': [
            'Regular blood sugar monitoring',
            'Cinnamon supplements (may help)',
            'Fenugreek seed water',
            'Bitter melon juice',
            'Indian gooseberry (Amla)'
        ],
        'diet_advice': [
            'Low glycemic index foods',
            'High fiber foods',
            'Limit refined carbohydrates',
            'No sugary drinks',
            'Portion control crucial',
            'Regular meal timing'
        ],
        'activities': [
            '150 minutes weekly aerobic exercise',
            'Resistance training 2-3 times/week',
            'Brisk walking 30 mins daily',
            'Yoga for stress management',
            'Avoid sedentary behavior'
        ],
        'duration': 'Lifelong management required'
    },
    'Hypertension': {
        'risk_level': 'High',
        'description': 'High blood pressure - Increases heart disease and stroke risk',
        'medications': [
            'ACE inhibitors (Lisinopril)',
            'Beta-blockers (Metoprolol)',
            'Calcium channel blockers (Amlodipine)',
            'Diuretics (Hydrochlorothiazide)',
            'Combination therapy often needed'
        ],
        'treatments': [
            'Regular BP monitoring',
            'Medication adherence',
            'Lifestyle modifications',
            'Stress management',
            'Regular medical check-ups'
        ],
        'home_remedies': [
            'Garlic supplement',
            'Hibiscus tea',
            'Celery juice',
            'Reduce salt intake',
            'Coconut water'
        ],
        'diet_advice': [
            'DASH diet (Dietary Approaches to Stop Hypertension)',
            'Reduce sodium to <2300 mg/day',
            'Potassium-rich foods (bananas, spinach)',
            'Limit alcohol',
            'Reduce caffeine',
            'Healthy fats (olive oil)'
        ],
        'activities': [
            '150 minutes moderate aerobic activity/week',
            'Walk 30 minutes daily',
            'Stick stretching',
            'Yoga and meditation',
            'Avoid stress'
        ],
        'duration': 'Lifelong management required'
    },
    'Heart attack': {
        'risk_level': 'High',
        'description': 'MEDICAL EMERGENCY - Call ambulance immediately (911/999)',
        'medications': [
            'EMERGENCY: Call ambulance immediately',
            'In hospital: Aspirin, Anticoagulants',
            'Beta-blockers, ACE inhibitors post-recovery',
            'Statins, Clopidogrel'
        ],
        'treatments': [
            'EMERGENCY MEDICAL CARE REQUIRED',
            'Angioplasty or bypass surgery',
            'ICU monitoring',
            'Cardiac rehabilitation',
            'Lifestyle modifications'
        ],
        'home_remedies': [
            'NO HOME TREATMENT - CALL EMERGENCY',
            'Chew aspirin if instructed',
            'Lie down and rest',
            'Follow cardiac rehabilitation'
        ],
        'diet_advice': [
            'Consult cardiologist for diet plan',
            'Anti-inflammatory diet',
            'Low saturated fat',
            'Omega-3 rich foods',
            'High fiber foods'
        ],
        'activities': [
            'Cardiac rehabilitation as prescribed',
            'Gradual activity increase',
            'Stress management absolutely critical',
            'Follow doctor\'s activity guidelines',
            'Regular monitoring mandatory'
        ],
        'duration': 'Requires intensive care and rehabilitation'
    },
    'Bronchial Asthma': {
        'risk_level': 'High',
        'description': 'Chronic respiratory condition with airway inflammation',
        'medications': [
            'Albuterol (rescue inhaler)',
            'Corticosteroid inhalers (maintenance)',
            'Long-acting beta-agonists (LABA)',
            'Leukotriene inhibitors',
            'Biologic therapies (Omalizumab)'
        ],
        'treatments': [
            'Use rescue inhaler as needed',
            'Daily maintenance inhaler',
            'Identify and avoid triggers',
            'Peak flow monitoring',
            'Asthma action plan'
        ],
        'home_remedies': [
            'Garlic consumption',
            'Ginger and turmeric drinks',
            'Honey and lemon',
            'Licorice root tea',
            'Mustard oil massage'
        ],
        'diet_advice': [
            'Avoid allergen foods',
            'Vitamin C rich foods',
            'Antioxidant vegetables',
            'Avoid sulfites',
            'Include omega-3 fats'
        ],
        'activities': [
            'Avoid allergen and trigger exposure',
            'Swimming in chlorine-free water',
            'Light exercise with warm-up',
            'Breathing exercises',
            'Stress management'
        ],
        'duration': 'Chronic - Requires ongoing management'
    },
    'Pneumonia': {
        'risk_level': 'High',
        'description': 'Severe lung infection - Requires medical treatment',
        'medications': [
            'Antibiotics (type depends on organism)',
            'Amoxicillin, Azithromycin',
            'Antivirals if viral',
            'Fever/pain relief (Acetaminophen, Ibuprofen)',
            'Cough suppressants'
        ],
        'treatments': [
            'Antibiotics as prescribed',
            'Rest and fluids',
            'Oxygen therapy (if needed)',
            'Chest X-ray monitoring',
            'Hospitalization if severe'
        ],
        'home_remedies': [
            'Rest (critical for recovery)',
            'Increase fluid intake',
            'Honey cough relief',
            'Ginger tea',
            'Garlic and turmeric',
            'Vapor inhalation'
        ],
        'diet_advice': [
            'High protein foods',
            'Vitamin C foods',
            'Zinc-rich foods',
            'Fluid intake crucial',
            'Soft, easy-to-digest foods'
        ],
        'activities': [
            'Rest absolutely critical',
            'Avoid physical exertion',
            'Stay hydrated',
            'Sleep improvement paramount',
            'Gradual activity resumption'
        ],
        'duration': '7-21 days depending on severity'
    },
    'Tuberculosis': {
        'risk_level': 'High',
        'description': 'Serious infectious disease - Requires extended antibiotics',
        'medications': [
            'RIPE therapy (Rifampin, Isoniazid, Pyrazinamide, Ethambutol)',
            '6-month standard course (2 months intensive)',
            '4 drugs initially, 2 drugs continuation',
            'Vitamin B6 supplementation',
            'Monitoring for side effects'
        ],
        'treatments': [
            'Directly observed therapy (DOT)',
            'Full antibiotic course completion (critical)',
            'Regular sputum tests',
            'Chest X-rays',
            'Isolation if infectious'
        ],
        'home_remedies': [
            'Strict medication adherence',
            'Nutritious diet',
            'Rest and sleep',
            'Avoid alcohol',
            'Ginger and turmeric tea'
        ],
        'diet_advice': [
            'High protein diet',
            'Vitamin B foods',
            'Vitamin C foods',
            'Eggs, milk, meat',
            'Avoid alcohol completely'
        ],
        'activities': [
            'Rest during intensive phase',
            'Gradual work resumption',
            'Avoid close contact with others',
            'Proper hygiene (covering mouth)',
            'Support group engagement'
        ],
        'duration': '6-9 months total treatment'
    },
    'GERD': {
        'risk_level': 'Medium',
        'description': 'Acid reflux disease - Chronic condition management needed',
        'medications': [
            'Proton pump inhibitors (Omeprazole)',
            'H2-receptor blockers (Ranitidine)',
            'Antacids (Calcium carbonate)',
            'Metoclopramide for motility',
            'Sucralfate'
        ],
        'treatments': [
            'Elevate head while sleeping (6 inches)',
            'Avoid trigger foods',
            'Small frequent meals',
            'Don\'t eat 2-3 hours before bed',
            'Maintain healthy weight'
        ],
        'home_remedies': [
            'Ginger tea',
            'Aloe vera juice',
            'Licorice root',
            'Honey',
            'Chamomile tea'
        ],
        'diet_advice': [
            'Avoid spicy foods',
            'Limit chocolate and coffee',
            'No alcohol',
            'Limit citrus and tomatoes',
            'No fatty foods',
            'Small portions'
        ],
        'activities': [
            'Avoid lying down after meals',
            'Light walking after eating',
            'Stress management important',
            'Gentle yoga',
            'Sleep elevation recommended'
        ],
        'duration': '4-8 weeks for improvement with treatment'
    },
    'Migraine': {
        'risk_level': 'Medium',
        'description': 'Severe headache disorder with potential neurological symptoms',
        'medications': [
            'Acetaminophen or Ibuprofen (acute)',
            'Sumatriptan (triptan class)',
            'Propranolol (preventive)',
            'Topiramate (preventive)',
            'Amitriptyline (preventive)'
        ],
        'treatments': [
            'Rest in dark, quiet room',
            'Cold/warm compress',
            'Triptan medications',
            'Medication adherence',
            'Identify and avoid triggers'
        ],
        'home_remedies': [
            'Peppermint essential oil (temples)',
            'Lavender oil',
            'Ginger tea',
            'Feverfew herb',
            'Magnesium supplements'
        ],
        'diet_advice': [
            'Identify trigger foods',
            'Avoid alcohol (especially red wine)',
            'Limit caffeine',
            'Regular meal timing',
            'Stay hydrated',
            'Magnesium-rich foods'
        ],
        'activities': [
            'Regular sleep schedule',
            'Yoga for stress relief',
            'Meditation',
            'Avoid triggers (stress, hormonal changes)',
            'Regular exercise'
        ],
        'duration': '4-72 hours per migraine episode'
    },
}

def get_disease_info(disease_name):
    """Get comprehensive information about a disease"""
    return DISEASE_DATABASE.get(disease_name, None)

def get_risk_level(disease_name):
    """Get risk level of a disease"""
    disease = get_disease_info(disease_name)
    return disease['risk_level'] if disease else 'Unknown'

def get_treatment_suggestions(disease_name):
    """Get treatment suggestions for a disease"""
    disease = get_disease_info(disease_name)
    return disease['treatments'] if disease else []

def get_medications(disease_name):
    """Get medications for a disease"""
    disease = get_disease_info(disease_name)
    return disease['medications'] if disease else []

def get_diet_advice(disease_name):
    """Get diet advice for a disease"""
    disease = get_disease_info(disease_name)
    return disease['diet_advice'] if disease else []

def get_activity_recommendations(disease_name):
    """Get activity recommendations for a disease"""
    disease = get_disease_info(disease_name)
    return disease['activities'] if disease else []
