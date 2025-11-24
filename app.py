# ai_health_coach_crewai.py
"""
Streamlit demo: AI Personal Health & Fitness Coach using Gemini + CrewAI.
- Requires: pip install streamlit google-genai crewai crewai-tools
- Pre-filled Gemini API key for testing
"""

import os
import streamlit as st
from crewai import Agent, Crew
from google import genai

# ---------- Gemini wrapper ----------
DEFAULT_GEMINI_API_KEY = "AIzaSyDtUjFxmrDrS4UwrCTM2IQ3SMDNAAmNCds"

def call_gemini(api_key: str, prompt: str, model: str = "gemini-2.5-flash") -> str:
    if not api_key:
        return (
            "No Gemini API key provided — using simulated plan.\n\n"
            "Sample daily plan:\n"
            "- Morning: 20 min jogging, stretches\n"
            "- Breakfast: Oatmeal with fruits\n"
            "- Afternoon: Strength training 45 min\n"
            "- Lunch: Protein-rich meal\n"
            "- Evening: Yoga 30 min\n"
            "- Dinner: Light salad + protein\n"
            "- Hydration: Drink 2-3L water\n"
        )
    try:
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(model=model, contents=prompt)
        if hasattr(response, "text"):
            return response.text
        return str(response)
    except Exception as e:
        return f"Gemini call failed: {e}"

# ---------- Streamlit UI ----------
st.set_page_config(page_title="AI Health Coach (CrewAI)", layout="centered")
st.title("💪 AI Health & Fitness Coach — CrewAI + Gemini")

st.markdown("""
This demo generates a **personalized health & fitness plan** using AI:
1. Researcher → gathers health tips
2. Planner → creates a day-by-day plan
""")

# Gemini credentials
gemini_key_input = st.text_input(
    "Gemini API key (leave blank to use default/demo)",
    value=DEFAULT_GEMINI_API_KEY,
    type="password"
)
gemini_key = gemini_key_input.strip() or DEFAULT_GEMINI_API_KEY
model_choice = st.selectbox("Gemini model", ["gemini-2.5-flash", "gemini-1.5-mini", "gemini-2.1"], index=0)

# User profile inputs
age = st.number_input("Age", min_value=10, max_value=100, value=25)
weight = st.number_input("Weight (kg)", min_value=30, max_value=200, value=70)
goals = st.text_input("Fitness goals", value="build muscle, lose fat")
interests = st.text_input("Interests (e.g. yoga, running, diet)", value="running, strength training")
days = st.number_input("Plan length (days)", min_value=1, max_value=30, value=7)

st.write("")
generate_button = st.button("Generate plan")

if generate_button:
    if not gemini_key:
        st.warning("No Gemini API key provided — using simulated plan.")
    st.info("Running AI agents...")

    # ---------- Step 1: Researcher gathers health tips ----------
    research_prompt = (
        f"You are a health researcher.\n"
        f"Profile: Age {age}, Weight {weight}, Goals: {goals}, Interests: {interests}.\n"
        "Suggest exercises, nutrition tips, hydration advice, and wellness recommendations."
    )
    research_output = call_gemini(gemini_key, research_prompt, model=model_choice)

    # ---------- Step 2: Planner generates day-by-day plan ----------
    planner_prompt = (
        f"You are a personal fitness planner.\n"
        f"Using the following research, create a {days}-day personalized health & fitness plan:\n"
        f"{research_output}\n\n"
        "Include workouts, meals, hydration, rest, and optional supplements. Format in markdown."
    )
    plan_output = call_gemini(gemini_key, planner_prompt, model=model_choice)

    # ---------- Display outputs ----------
    st.markdown("### Researcher output")
    st.text_area("ResearcherAgent", value=research_output, height=300)

    st.markdown("### Planner output")
    st.text_area("PlannerAgent", value=plan_output, height=400)

    st.success("Done! Review your personalized health & fitness plan above.")
