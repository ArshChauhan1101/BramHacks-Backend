from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import os

load_dotenv()

groq_api_key = os.environ.get("GROQ_API_KEY")

categories = {
    "Public Transit": ["Delays", "Crowding", "Fare", "Accessibility", "Cleanliness"],
    "Parking":["Availability", "Pricing", "Illegal Parking", "Special Parking Needs"],
    "Road Safety": ["Street Lighting", "Pedestrian Crossings", "Traffic Signs", "Accident Hotspots", "Speeding Zones"]
}

prompt_template = PromptTemplate(
    input_variables=["categories", "subcategories", "complaint"],
    template="""
        Classify the following complaint into a category and subcategory. Categories include: {categories}. Subcategories include: {subcategories}.

        Complaint: "{complaint}"

        Guidelines:
        If the complaint is unrelated to {subcategories}, respond with: "Your complaint is not regarding transportation, parking and road safety. Please contact the respective authority."
        
        Output Format:
        - 'Category: [Category], \nSubcategory: [Subcategory]'
        
     """
)
#- If category is "Suggestions": 'We will consider your feedback and improve our services.'

llm_groq = ChatGroq(groq_api_key=groq_api_key, model_name="mixtral-8x7b-32768")

def classify_complaint(complaint):
    categories_str = ", ".join(categories.keys())
    subcategories_str = ", ".join([item for sublist in categories.values() for item in sublist])

    prompt = prompt_template.format(
        categories=categories_str,
        subcategories=subcategories_str,
        complaint=complaint
    )

    result = llm_groq.invoke(prompt)

    return result.content

if __name__ == "__main__":
    complaint = "What will the traffic be like tomorrow morning?"
    classification = classify_complaint(complaint)
    print(f"Complaint: {complaint}\n{classification}")
