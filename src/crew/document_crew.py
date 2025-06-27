from crewai import Crew, Process
from src.agents.document_agents import DocumentAgents
from src.tasks.document_tasks import DocumentTasks
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DocumentCrewOrchestrator:
    def __init__(self, text):
        self.text = text
        self.agents = DocumentAgents()
        self.tasks = DocumentTasks()
    
    def summarize(self, summary_type='general'):
        try:
            summarize_task = self.tasks.summarize(self.text, summary_type)
            summarize_task.agent = self.agents.summarizer

            quality_task = self.tasks.quality_review(
                self.text, 
                summarize_task, 
                f"Summary type: {summary_type}"
            )
            quality_task.agent = self.agents.quality_analyst
            
            crew = Crew(
                agents=[self.agents.summarizer, self.agents.quality_analyst],
                tasks=[summarize_task, quality_task],
                process=Process.sequential,
                verbose=True
            )
            result = crew.kickoff()
            logger.info(f"Summarization completed: {summary_type}")
            # Ensure result is JSON serializable
            if not isinstance(result, str):
                result = str(result)
            return result
        except Exception as e:
            logger.error(f"Summarization error: {str(e)}")
            return f"Error during summarization: {str(e)}"
    
    def improve(self, improvement_type='general'):
        try:
            improve_task = self.tasks.improve(self.text, improvement_type)
            improve_task.agent = self.agents.editor

            quality_task = self.tasks.quality_review(
                self.text, 
                improve_task, 
                f"Improvement type: {improvement_type}"
            )
            quality_task.agent = self.agents.quality_analyst
            
            crew = Crew(
                agents=[self.agents.editor, self.agents.quality_analyst],
                tasks=[improve_task, quality_task],
                process=Process.sequential,
                verbose=True
            )
            result = crew.kickoff()
            logger.info(f"Improvement completed: {improvement_type}")
            # Ensure result is JSON serializable
            if not isinstance(result, str):
                result = str(result)
            return result
        except Exception as e:
            logger.error(f"Improvement error: {str(e)}")
            return f"Error during improvement: {str(e)}"
    
    def generate_addons(self, addon_type='headlines'):
        try:
            addon_task = self.tasks.generate_addons(self.text, addon_type)
            addon_task.agent = self.agents.addon_generator

            quality_task = self.tasks.quality_review(
                self.text, 
                addon_task, 
                f"Addon type: {addon_type}"
            )
            quality_task.agent = self.agents.quality_analyst
            
            crew = Crew(
                agents=[self.agents.addon_generator, self.agents.quality_analyst],
                tasks=[addon_task, quality_task],
                process=Process.sequential,
                verbose=True
            )
            result = crew.kickoff()
            logger.info(f"Addon generation completed: {addon_type}")
            # Ensure result is JSON serializable
            if not isinstance(result, str):
                result = str(result)
            return result
        except Exception as e:
            logger.error(f"Addon generation error: {str(e)}")
            return f"Error during addon generation: {str(e)}"