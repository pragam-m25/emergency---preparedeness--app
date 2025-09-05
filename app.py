import streamlit as st  # type: ignore

# Sidebar for Video Upload
with st.sidebar:
    st.header("📹 Video Analysis")
    st.write("Upload video of your situation")
    
    uploaded_video = st.file_uploader(
        "Choose video file", 
        type=['mp4', 'avi', 'mov', 'mkv']
    )
    
    if uploaded_video is not None:
        st.video(uploaded_video)
        
        # Available resources
        st.subheader("🎒 Available Resources")
        resources = st.multiselect(
            "What do you have?",
            ["Water", "Food", "Flashlight", "First aid", "Phone", "Rope", "Blankets"]
        )
        
        location = st.selectbox(
            "Current location:",
            ["Home", "Office", "Outdoors", "Vehicle"]
        )
        
        people = st.number_input("People with you:", min_value=1, value=1)
        
        if st.button("🔍 Analyze"):
            st.success("✅ Analysis Complete!")
            
            # Emergency measures
            st.subheader("⚠️ Immediate Actions")
            if "Phone" in resources:
                st.write("✓ Call 112 for help")
            else:
                st.error("❌ Find communication method")
                
            if "Water" in resources:
                st.write("✓ Ration water supply")
            else:
                st.warning("⚠️ Find clean water source")
            
            # Solutions based on location
            st.subheader("💡 Solutions")
            if location == "Home":
                st.write("🏠 Stay indoors if safe")
                st.write("🔌 Turn off utilities if needed")
            elif location == "Outdoors":
                st.write("🌲 Find shelter immediately")
                st.write("📡 Signal for help")
            
            # Priority actions
            st.subheader("📋 Priority List")
            st.write("1. Ensure safety")
            st.write("2. Call for help")
            st.write("3. Secure shelter")
            st.write(f"4. Plan for {people} people")

st.title("🚨 Emergency Preparedness")
st.header("🚨 Be ready for work")

st.subheader("Few lines on disaster management")
st.write(""" 

Disaster management is the process of preparing for, responding to, and recovering from natural or man-made disasters.

It aims to reduce loss of life, property damage, and economic disruption.

Key steps include preparedness, mitigation, response, and recovery.

Awareness and training help communities react calmly and effectively during emergencies.

Schools and institutions play a vital role in educating students about disaster safety protocols.

Technology such as early warning systems, mobile apps, and virtual drills can strengthen preparedness.

A strong disaster management system builds a resilient society that can face challenges with confidence.

""")
st.video("https://youtu.be/XLrp2czggB8")

col1,col2=st.columns(2)
with col1 :
    st.write("Few safety tips")
    st.write("""
    1. Stay calm and focused during emergencies.
    2. Be prepared for unexpected situations.
    3. Keep your home safe and secure.
    4. Listen to emergency alerts and follow instructions.
    5. Stay informed about local disaster management.
    6. Be aware of your surroundings and your surroundings.
    7. Stay connected with emergency services.
    8. Be prepared for potential hazards.
    9. Stay informed about the latest updates.
    10. Stay informed about the latest updates.
    """)
with col2:
    st.write("EMERGENCY CONTACTS")
    st.write("""
    1. Police: 100
    2. Fire Department: 101
    3. Ambulance: 108
    4. Disaster Management: 112
    5. National Disaster Response Center: 112
    6. Emergency Medical Services: 112
    7. National Emergency Operations Center: 112
    8. National Emergency Response System: 112
    9. National Emergency Operations Center: 112
    10. National Emergency Response System: 112
    """)

# Create tabs for different features
tab1, tab2, tab3 = st.tabs(["Disaster Info", "Video Analysis", "First Aid Guide"])

with tab1:
    languagetype=st.selectbox("select your language :",["hindi", "english"])
    disastertype=st.selectbox("select type of disaster :", ["volcano","floods","ज्वालामुखी","बाढ़","None"])

    # Disaster information in tab1
    st.divider()
    
    if languagetype=="english":
        st.subheader(f"📋 Safety Measures for {disastertype.title()}")
    else:
        st.subheader(f"📋 {disastertype} से बचाव के उपाय")

    if disastertype=="volcano" and languagetype=="english":
     st.markdown("**Measures for volcanic eruptions**")
     st.write(""" Before a Volcanic Eruption

Stay informed: Listen to government warnings, geological updates, and emergency alerts.

Prepare an emergency kit: Include water, food, torch, batteries, mask, first-aid kit, and important documents.

Know evacuation routes: Identify safe shelters and practice evacuation drills.

Protect your house: Seal windows/doors to prevent ash entry, and keep roofs strong (ash can be heavy).

During a Volcanic Eruption

Follow official instructions immediately—evacuate if told to.

Stay indoors if evacuation is not possible; close all openings.

Use masks or cloth to cover nose and mouth to avoid inhaling ash.


Protect eyes with goggles; avoid wearing contact lenses.

Stay away from rivers and streams (they may carry lava or mudflows).

Do not drive unless necessary—ash reduces visibility and damages vehicles.

After a Volcanic Eruption

Wait for official “all clear” before returning home.

Avoid ash-covered areas as much as possible.

Clean roofs carefully—ash is heavy and can collapse structures.

Wear protective gear while cleaning ash.

Boil or filter water before drinking (ash can contaminate supplies).

Help neighbors, especially children, elderly, and people with disabilities.
""")

if disastertype=="floods" and languagetype=="english":
    st.markdown("**Measures for floods**")
    st.write(""" Before a Flood

Stay informed: Monitor weather reports and flood warnings.

Prepare emergency kit: Water, food, flashlight, radio, first-aid supplies.

Know evacuation routes: Identify higher ground and safe shelters.

Secure your home: Move valuables to higher floors, turn off utilities if advised.

During a Flood

Evacuate immediately if told by authorities.

Never walk or drive through flood water - "Turn Around, Don't Drown".

Stay away from downed power lines.

Seek higher ground immediately.

After a Flood

Wait for authorities to declare area safe.

Avoid flood water - it may be contaminated.

Document damage with photos for insurance.

Clean and disinfect everything that got wet.
""")

elif disastertype=="ज्वालामुखी" and languagetype=="hindi":
    st.write("""🌋 ज्वालामुखी विस्फोट से बचाव के उपाय
🔹 विस्फोट से पहले (तैयारी)

🏠 सुरक्षित निकासी मार्ग (evacuation plan) और शरण स्थल पहले से तय कर लो।

📻 रेडियो/टीवी से सरकार द्वारा दी गई चेतावनियों पर ध्यान दो।

📦 आपातकालीन किट तैयार रखो – टॉर्च, मास्क, पानी, भोजन, प्राथमिक उपचार।

😷 धूल से बचने के लिए मास्क और चश्मा साथ रखो।

🔹 विस्फोट के दौरान

⛰️ ज्वालामुखी के पास बिल्कुल मत जाओ, तुरंत सुरक्षित स्थान पर चले जाओ।

🏃‍♂️ सरकार या प्रशासन के निकासी आदेश का पालन करो।

🪟 खिड़कियाँ और दरवाज़े बंद रखो ताकि राख (ash) अंदर न आ सके।

😷 मास्क या गीले कपड़े से मुँह और नाक को ढककर सांस लो।

🚗 गाड़ी चलाने से बचो, राख से सड़क फिसलन भरी और इंजन खराब हो सकता है।

🔹 विस्फोट के बाद

✅ प्रशासन द्वारा "सुरक्षित" घोषित किए जाने के बाद ही घर वापस जाओ।

💧 राख को सावधानी से साफ करो (गीले कपड़े/पानी से), झाड़ू से सूखी सफाई मत करो।

🚰 पीने का पानी छानकर या उबालकर इस्तेमाल करो, क्योंकि पानी दूषित हो सकता है।

🧍 घायल और प्रभावित लोगों की मदद करो।""")

elif disastertype=="बाढ़" and languagetype=="hindi":
    st.write("""🌊 बाढ़ से बचाव के उपाय
🔹 बाढ़ से पहले (तैयारी)

🌧️ मौसम की जानकारी और बाढ़ की चेतावनी पर ध्यान दो।

🎒 आपातकालीन किट तैयार रखो – पानी, खाना, टॉर्च, रेडियो।

🏠 घर के महत्वपूर्ण सामान ऊंची जगह पर रखो।

🔹 बाढ़ के दौरान

🏃♂️ प्रशासन के निकासी आदेश का पालन करो।

⚠️ बाढ़ के पानी में कभी मत चलो या गाड़ी मत चलाओ।

⚡ टूटी बिजली की तारों से दूर रहो।

🔹 बाढ़ के बाद

✅ प्रशासन द्वारा सुरक्षित घोषित करने के बाद ही घर वापस जाओ।

📷 नुकसान की तस्वीरें लो बीमा के लिए।

🧽 सब कुछ साफ और कीटाणुरहित करो।""")

# Handle cross-language selections
elif disastertype=="volcano" and languagetype=="hindi":
    st.write("कृपया हिंदी में 'ज्वालामुखी' चुनें")

elif disastertype=="floods" and languagetype=="hindi":
    st.write("कृपया हिंदी में 'बाढ़' चुनें")

elif disastertype=="ज्वालामुखी" and languagetype=="english":
    st.write("Please select 'volcano' for English")

elif disastertype=="बाढ़" and languagetype=="english":
    st.write("Please select 'floods' for English")

elif disastertype=="None":
    if languagetype=="english":
        st.write("Select a disaster type to see safety measures")
    else:
        st.write("आपदा की जानकारी देखने के लिए कोई आपदा चुनें")

with tab2:
    st.subheader("🎯 Situation Analysis")
    st.write("Upload video in sidebar for personalized guidance")
    
    col1, col2 = st.columns(2)
    with col1:
        st.info("📹 Video Features:")
        st.write("- Situation detection")
        st.write("- Resource analysis")
        st.write("- Location advice")
        
    with col2:
        st.success("🎯 Smart Help:")
        st.write("- Immediate actions")
        st.write("- Feasible solutions")
        st.write("- Priority planning")

with tab3:
    st.subheader("🏥 First Aid Guide")
    
    aid_type = st.selectbox(
        "Emergency type:",
        ["Cuts", "Burns", "Choking", "Heart Attack"]
    )
    
    if aid_type == "Cuts":
        st.write("🩹 For Cuts:")
        st.write("1. Clean hands")
        st.write("2. Stop bleeding")
        st.write("3. Clean wound")
        st.write("4. Apply bandage")
        
    elif aid_type == "Burns":
        st.write("🔥 For Burns:")
        st.write("1. Cool with water (10-20 min)")
        st.write("2. Remove jewelry")
        st.write("3. Cover with clean cloth")
        st.write("4. Seek medical help")
        
    elif aid_type == "Choking":
        st.write("🫁 For Choking:")
        st.write("1. Encourage coughing")
        st.write("2. Give 5 back blows")
        st.write("3. Give 5 abdominal thrusts")
        st.write("4. Call 108 if needed")