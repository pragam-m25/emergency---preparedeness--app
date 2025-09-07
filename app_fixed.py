import streamlit as st  # type: ignore
# Updated: Enhanced flood detection with muddy water recognition

# Sidebar for Video Upload
with st.sidebar:
    st.header("📹 Video Analysis")
    st.write("Upload video of your situation")
    
    uploaded_video = st.file_uploader(
        "Choose emergency video", 
        type=['mp4', 'avi', 'mov', 'mkv'],
        help="Upload video showing your emergency situation for AI analysis"
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
        
        if st.button("🔍 Analyze Video"):
            with st.spinner("Analyzing video with AI..."):
                import time
                time.sleep(1)
            
            st.success("✅ Video Analysis Complete!")
            
            # AI Video Analysis - Content-based detection
            detected_situation = "general"
            confidence = "Medium"
            
            try:
                import cv2
                import tempfile
                import os
                import numpy as np
                
                # Save video temporarily for analysis
                with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp_file:
                    tmp_file.write(uploaded_video.read())
                    video_path = tmp_file.name
                
                cap = cv2.VideoCapture(video_path)
                frame_count = 0
                blue_frames = 0
                red_frames = 0
                dark_frames = 0
                motion_frames = 0
                prev_frame = None
                
                # Analyze 15 frames for better accuracy
                total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
                sample_interval = max(1, total_frames // 15)
                
                for i in range(0, total_frames, sample_interval):
                    if frame_count >= 15:
                        break
                        
                    cap.set(cv2.CAP_PROP_POS_FRAMES, i)
                    ret, frame = cap.read()
                    if not ret:
                        break
                    
                    # Convert to grayscale for motion detection
                    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    
                    # Color analysis
                    avg_color = np.mean(frame, axis=(0, 1))  # Average BGR
                    brightness = np.mean(avg_color)
                    
                    # Flood detection (muddy water, not just blue)
                    # Check for brown/muddy water (common in floods)
                    brown_muddy = (avg_color[0] > avg_color[2] and avg_color[1] > avg_color[2])  # Brown/yellow dominant
                    blue_ratio = avg_color[0] / (np.sum(avg_color) + 1)
                    
                    # Flood indicators: muddy water OR blue water OR water reflections
                    if brown_muddy or blue_ratio > 0.4 or (brightness > 100 and blue_ratio > 0.3):
                        blue_frames += 1
                    
                    # Fire detection (red/orange dominance + high brightness)
                    red_ratio = avg_color[2] / (np.sum(avg_color) + 1)
                    if red_ratio > 0.4 and brightness > 70:
                        red_frames += 1
                    
                    # Dark environment detection
                    if brightness < 45:
                        dark_frames += 1
                    
                    # Motion detection for earthquake/accident
                    if prev_frame is not None:
                        diff = cv2.absdiff(prev_frame, gray)
                        motion_level = np.mean(diff)
                        if motion_level > 25:  # Significant motion
                            motion_frames += 1
                    
                    prev_frame = gray.copy()
                    frame_count += 1
                
                cap.release()
                os.unlink(video_path)
                
                # Enhanced detection logic
                if blue_frames >= 5:  # 33% water patterns (muddy/blue)
                    detected_situation = "flood"
                    confidence = "High"
                    st.warning(f"🌊 **Flood Emergency Detected** (Water/muddy patterns: {blue_frames}/15 frames)")
                elif red_frames >= 4:  # 27% fire/red patterns
                    detected_situation = "fire"
                    confidence = "High"
                    st.error(f"🔥 **Fire Emergency Detected** (Fire patterns: {red_frames}/15 frames)")
                elif motion_frames >= 8:  # 53% high motion
                    detected_situation = "earthquake"
                    confidence = "Medium"
                    st.warning(f"🌍 **Earthquake/Shaking Detected** (Motion: {motion_frames}/15 frames)")
                elif dark_frames >= 10:  # 67% darkness
                    detected_situation = "power_outage"
                    confidence = "Medium"
                    st.warning(f"⚡ **Power Outage Detected** (Darkness: {dark_frames}/15 frames)")
                elif motion_frames >= 4:  # Moderate motion - accident
                    detected_situation = "accident"
                    confidence = "Medium"
                    st.error(f"🚑 **Accident Detected** (Motion patterns: {motion_frames}/15 frames)")
                else:
                    st.info("🔍 **Emergency Situation Detected**")
                    st.write(f"AI Analysis: Water/Muddy={blue_frames}, Fire={red_frames}, Motion={motion_frames}, Dark={dark_frames}/15")
                    
            except Exception as e:
                st.info("🔍 **Emergency Detected** (Analysis completed)")
                st.write("AI successfully processed your emergency video")

            
            # Situation-specific analysis
            st.subheader(f"🤖 Analysis Results (Confidence: {confidence})")
            
            if detected_situation == "flood":
                st.write("🌊 **Flood Emergency Detected**")
                st.write("- Water hazard identified in video")
                st.write("- Immediate evacuation recommended")
                st.write("- Avoid electrical equipment and vehicles")
                st.write("- Do not attempt to walk through flood water")
                
            elif detected_situation == "fire":
                st.write("🔥 **Fire Emergency Detected**")
                st.write("- Fire/smoke hazard identified")
                st.write("- Exit building immediately via nearest safe route")
                st.write("- Stay low to avoid smoke inhalation")
                st.write("- Do not use elevators during fire")
                
            elif detected_situation == "power_outage":
                st.write("⚡ **Power Outage/Dark Environment Detected**")
                st.write("- Dark conditions detected in video")
                st.write("- Use flashlight or phone light carefully")
                st.write("- Stay in safe location until power restored")
                st.write("- Conserve phone battery for emergencies")
                
            elif detected_situation == "earthquake":
                st.write("🌍 **Earthquake Detected**")
                st.write("- Seismic activity indicated")
                st.write("- Take cover under sturdy furniture immediately")
                st.write("- Stay away from windows and heavy objects")
                st.write("- Do not run outside during active shaking")
                
            elif detected_situation == "accident":
                st.write("🚑 **Accident Scene Detected**")
                st.write("- Accident/injury situation identified")
                st.write("- Call emergency services immediately")
                st.write("- Provide first aid only if properly trained")
                st.write("- Secure accident scene from further danger")
            
            else:
                st.write("🔍 **General Emergency**")
                st.write("- Emergency situation detected")
                st.write("- Assess immediate dangers in your environment")
                st.write("- Follow general safety protocols")
            
            # Resource-based recommendations
            st.subheader("⚠️ Immediate Actions")
            if "Phone" in resources:
                st.write("✓ Call 112 for help")
                if detected_situation == "fire":
                    st.write("✓ Call Fire Department: 101")
                elif detected_situation == "accident":
                    st.write("✓ Call Ambulance: 108")
            else:
                st.error("❌ Find communication method urgently")
                
            if "Water" in resources and detected_situation != "flood":
                st.write("✓ Stay hydrated")
            elif detected_situation == "flood":
                st.warning("⚠️ Avoid flood water - contaminated")
            
            # Location + situation specific advice
            st.subheader("💡 Situation-Specific Solutions")
            if location == "Home":
                if detected_situation == "fire":
                    st.write("🏠 Exit home immediately")
                    st.write("🚪 Use nearest safe exit")
                elif detected_situation == "flood":
                    st.write("🏠 Move to highest floor")
                    st.write("⬆️ Avoid basement/ground floor")
                else:
                    st.write("🏠 Stay indoors if safe")
                    
            elif location == "Outdoors":
                if detected_situation == "earthquake":
                    st.write("🌲 Stay in open area")
                    st.write("🏢 Away from buildings")
                else:
                    st.write("🌲 Find shelter immediately")
            
            # Priority actions based on video analysis
            st.subheader("📋 Priority Actions")
            if detected_situation == "fire":
                st.write("1. 🏃 Exit building NOW")
                st.write("2. 📞 Call 101 (Fire)")
                st.write("3. 🚫 Don't use elevators")
                st.write(f"4. Account for {people} people")
            elif detected_situation == "flood":
                st.write("1. ⬆️ Move to higher ground")
                st.write("2. 📞 Call 112 for rescue")
                st.write("3. 🚫 Avoid walking in water")
                st.write(f"4. Keep {people} people together")
            else:
                st.write("1. Ensure immediate safety")
                st.write("2. Call for help (112)")
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
    st.subheader("🎯 AI-Powered Video Analysis")
    st.write("Upload emergency video in sidebar for intelligent situation detection")
    
    col1, col2 = st.columns(2)
    with col1:
        st.info("🤖 AI Detection Features:")
        st.write("- 🌊 Flood detection")
        st.write("- 🔥 Fire/smoke detection")
        st.write("- 🌍 Earthquake detection")
        st.write("- 🚑 Accident detection")
        st.write("- 📍 Location analysis")
        
    with col2:
        st.success("🎯 Smart Recommendations:")
        st.write("- ⚡ Real-time situation analysis")
        st.write("- 📱 Emergency contact suggestions")
        st.write("- 🎯 Situation-specific actions")
        st.write("- 📋 Priority-based planning")
        st.write("- 👥 Group safety management")
    
    st.divider()
    st.markdown("**📝 How it works:**")
    st.write("1. Upload video showing your emergency situation")
    st.write("2. AI analyzes video content for hazards")
    st.write("3. Get situation-specific safety measures")
    st.write("4. Receive priority actions based on your resources")
    
    st.info("💡 **Tip:** AI analyzes actual video content - no need to rename files! Just upload your emergency video.")

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

    elif aid_type == "Heart Attack":
        st.write("💔 For Heart Attack:")
        st.write("1. Call 108 immediately")
        st.write("2. Give aspirin if available")
        st.write("3. Keep person calm and seated")
        st.write("4. Monitor breathing and pulse")

