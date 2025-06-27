from crewai import Agent
import os

# Set the Gemini model string for LiteLLM/CrewAI
# Make sure to set LITELLM_PROVIDER=google and GEMINI_API_KEY=your_actual_key in your environment or .env file

gemini_model = "gemini/gemini-2.0-flash"

class DocumentAgents:
    def __init__(self):
        self.summarizer = Agent(
            role='Senior Document Summarizer',
            goal='Create concise and meaningful summaries of documents',
            backstory=(
                'Expert in analyzing and condensing complex documents into key points. '
                'Skilled in identifying main arguments, conclusions, and essential information.'
            ),
            llm=gemini_model,
            verbose=True
        )
        
        self.editor = Agent(
            role='Document Enhancement Specialist',
            goal='Improve clarity, structure, and language of documents',
            backstory=(
                'Professional editor with 10+ years experience in technical and business writing. '
                'Specializes in transforming rough drafts into polished, professional documents.'
            ),
            llm=gemini_model,
            verbose=True
        )
        
        self.addon_generator = Agent(
            role='Content Add-on Creator',
            goal='Generate supplementary materials for documents',
            backstory=(
                'Creative content creator skilled at extracting key insights and transforming them '
                'into various formats like emails, presentations,action Items, key questions.'
            ),
            llm=gemini_model,
            verbose=True
        )
        
        self.quality_analyst = Agent(
            role='Quality Control Analyst',
            goal='Ensure output meets quality standards',
            backstory=(
                'Detail-oriented reviewer with exceptional standards for accuracy, clarity, '
                'and professionalism. Ensures all outputs maintain original intent while '
                'improving presentation.'
            ),
            llm=gemini_model,
            verbose=True
        )