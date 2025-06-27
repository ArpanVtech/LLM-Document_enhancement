from crewai import Task

class DocumentTasks:
    @staticmethod
    def summarize(text, summary_type):
        prompt = {
            'general': "Provide a comprehensive yet concise summary highlighting main points and key information",
            'executive': "Create an executive summary for senior management focusing on decisions and action items",
            'bullet_points': "Summarize in 5-7 bullet points capturing essential information",
            'abstract': "Write an academic-style abstract including purpose, methods, findings, and conclusions"
        }.get(summary_type, "Provide a comprehensive summary")
        
        return Task(
            description=f"{prompt} for the following document:\n\n{text[:5000]}... [truncated]",
            expected_output=(
                "A well-structured summary that captures the main points, key arguments, "
                "and essential information from the document. Should be concise and "
                "tailored to the requested summary type."
            )
        )
    
    @staticmethod
    def improve(text, improvement_type):
        prompt = {
            'general': "Improve clarity, flow, and overall quality while maintaining original meaning",
            'formal': "Rewrite to be more formal and professional for business communication",
            'concise': "Make more concise and impactful while preserving key information",
            'clarity': "Improve clarity and readability for better understanding",
            'structure': "Improve structure and organization ensuring logical flow"
        }.get(improvement_type, "Improve clarity, flow, and overall quality")
        
        return Task(
            description=f"{prompt} for the following text:\n\n{text[:5000]}... [truncated]",
            expected_output=(
                "An enhanced version of the document that maintains the original meaning "
                "but improves language, structure, and clarity according to the requested "
                "improvement type."
            )
        )
    
    @staticmethod
    def generate_addons(text, addon_type):
        prompt = {
            'headlines': "Generate 5 compelling headlines suitable for articles or presentations",
            'follow_up_email': "Write a professional follow-up email summarizing key points and next steps",
            'slide_content': "Create bullet points for 3-4 presentation slides",
            'action_items': "Extract and list specific action items or next steps",
            'key_questions': "Generate 5-7 important questions addressed by the document",
            'social_media': "Create 3 social media posts highlighting key insights"
        }.get(addon_type, "Generate 5 compelling headlines")
        
        return Task(
            description=f"{prompt} based on the following content:\n\n{text[:5000]}... [truncated]",
            expected_output=(
                "Relevant and useful supplementary content that adds value to the original "
                "document, formatted appropriately for the requested addon type."
            )
        )
    
    @staticmethod
    def quality_review(original_text, processed_output, context):
        return Task(
            description=(
                "Review the processed output against the original document to ensure quality and consistency:\n\n"
                f"Original Document (excerpt): {original_text[:2000]}...\n\n"
                f"Processed Output: {processed_output}\n\n"
                f"Context: {context}"
            ),
            expected_output=(
                "A quality assessment report that includes:\n"
                "1. Accuracy of content compared to original\n"
                "2. Clarity and coherence of output\n"
                "3. Adherence to requested format/style\n"
                "4. Suggestions for improvement if needed\n"
                "5. Final approval status"
            )
        )