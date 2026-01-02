import streamlit as st
import numpy as np
from streamlit_drawable_canvas import st_canvas

# ---------------------------------
# Page Configuration (MUST BE FIRST)
# ---------------------------------
st.set_page_config(
    page_title="You Are the Shape Recogniser",
    page_icon="🧠",
    layout="centered"
)

# ---------------------------------
# Session State
# ---------------------------------
if "canvas_key" not in st.session_state:
    st.session_state.canvas_key = 0

# ---------------------------------
# Title & Introduction
# ---------------------------------
st.title("🧠 You Are the Shape Recogniser")
#st.info(
    #"You will act as an **AI system**. Imagine a shape, draw it, and observe how the AI interprets your drawing."
#)

# ---------------------------------
# Learning Objective
# ---------------------------------

st.markdown("### 🎯 Learning Objective")

st.markdown("""
<div style="
    font-size:16.5px;
    line-height:1.7;
    background-color:#f4f8ff;
    padding:14px;
    border-left:5px solid #4a90e2;
    border-radius:6px;
">
<b>By the end of this activity, you will be able to:</b><br><br>
• Recognise how AI analyses drawings as pixel patterns<br>
• Experience rule-based visual classification<br>
• Build intuition about AI decision-making and limitations
</div>
""", unsafe_allow_html=True)

# ---------------------------------
# Task Selection
# ---------------------------------
st.markdown("---")
st.markdown("### 🧠 Imagine and draw")
task = st.selectbox(
    "Choose and draw one of the following:",
    ["Simple Shape", "Complex Shape"]
)

# ---------------------------------
# Adaptive Hint System
# ---------------------------------
if task == "Simple Shape":
    st.info("💡 Hint: Use smooth lines and keep the drawing compact.")
else:
    st.info("💡 Hint: Use crossings, sharp turns, or spread-out strokes.")

# ---------------------------------
# Fun Controls
# ---------------------------------
st.markdown("### 🎨 Drawing Controls")
stroke_color = st.color_picker("Choose drawing colour", "#000000")
stroke_width = st.slider("Stroke thickness", 1, 8, 3)

challenge_mode = st.checkbox("🎯 Challenge Mode: Try to trick the AI")

st.markdown("---")

# ---------------------------------
# Canvas Section
# ---------------------------------
st.subheader("✏️ Draw Here")

canvas = st_canvas(
    stroke_width=stroke_width,
    stroke_color=stroke_color,
    background_color="#ffffff",
    height=300,
    width=700,
    drawing_mode="freedraw",
    key=f"canvas_{st.session_state.canvas_key}"
)

st.caption("Try changing colours or stroke thickness. Notice how the AI decision stays the same.")

# ---------------------------------
# Shape Recognition Logic (FINAL)
# ---------------------------------
def recognise_drawing(image):
    if image is None:
        return "No drawing detected", 0, 0

    gray = image[:, :, 0]
    non_white_pixels = np.sum(gray < 250)

    ys, xs = np.where(gray < 250)

    if len(xs) == 0:
        return "No drawing detected", 0, 0

    # Measure drawing spread (complexity proxy)
    spread = np.std(xs) + np.std(ys)

    if non_white_pixels < 500:
        return "Very little drawing detected", non_white_pixels, spread

    if spread < 120:
        return "Likely Simple Shape", non_white_pixels, spread
    else:
        return "Likely Complex Shape", non_white_pixels, spread


# ---------------------------------
# Analyse Button
# ---------------------------------
if st.button("🔍 Analyse Drawing"):
    prediction, pixel_count, spread = recognise_drawing(canvas.image_data)

    st.markdown("---")
    st.subheader("🤖 System Feedback")

    st.markdown(f"""
    <div style="
        font-size:16.5px;
        line-height:1.7;
        background-color:#f4f8ff;
        padding:14px;
        border-left:5px solid #4a90e2;
        border-radius:6px;
        margin-bottom:12px;
    ">
    <b>🤖 AI Observation</b><br><br>
    {prediction}<br>
    <b>Drawing Density:</b> {pixel_count} pixels
    </div>
    """, unsafe_allow_html=True)

    # Confidence estimation
    confidence = min((pixel_count / 8000 + spread / 200) / 2, 1.0)
    st.progress(confidence)
    st.write(f"AI confidence: {int(confidence * 100)}%")

    if task.lower() in prediction.lower():
        st.success("✅ The AI recognises your drawing as the selected shape.")
        st.balloons()
    else:
        if challenge_mode:
            st.success("🎉 You tricked the AI! This shows the limitations of rule-based systems.")
        else:
            st.warning(
                "⚠ The AI interpretation does not match your intended shape.\n\n"
                "This shows how simple AI systems can misinterpret drawings."
            )

    st.caption(
        "Note: This AI uses simple rules (pixel density and spread). "
        "It does not truly understand shapes like humans do."
    )

    # ---------------------------------
    # Reflection Section
    # ---------------------------------
    with st.expander("🤔 Think About It"):
        st.write("""
        - Did the AI interpret your drawing as you expected?  
        - Which features do you think influenced the AI decision?  
        - What information is missing that humans usually rely on?  
        """)

# ---------------------------------
# Reset Canvas
# ---------------------------------
if st.button("🔁 Reset Canvas"):
    st.session_state.canvas_key += 1
    st.rerun()

# ---------------------------------
# Footer
# ---------------------------------
st.markdown(
    """
    <div style="text-align:center; font-size:13px; margin-top:40px;">
        <b>AI Shape Recogniser</b><br>
        Fundamentals of AI – Visual Pattern Recognition<br>
        Developed by Ts. Ainie Hayati Noruzman © 2026
    </div>
    """,
    unsafe_allow_html=True
)
