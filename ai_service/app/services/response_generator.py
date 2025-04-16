import re
from app.models.request_models import AIRequest, FormField
from app.models.response_models import AIResponse, FieldResponse
from app.utils.ollama_client import get_ollama_response

async def generate_responses(request: AIRequest) -> AIResponse:
    """Generate responses for job application form fields"""
    prompt = create_response_generation_prompt(request)
    ai_response = await get_ollama_response(prompt)
    
    return parse_response_generation(ai_response, request.formFields)

def create_response_generation_prompt(request: AIRequest) -> str:
    """Create prompt for generating responses to form fields"""
    # Build resume context
    resume = request.resume
    resume_context = f"""
APPLICANT INFORMATION:
Full Name: {resume.fullName}
"""
    
    if resume.email:
        resume_context += f"Email: {resume.email}\n"
    if resume.phone:
        resume_context += f"Phone: {resume.phone}\n"
    if resume.summary:
        resume_context += f"\nSummary: {resume.summary}\n"
    
    if resume.skills and len(resume.skills) > 0:
        resume_context += f"\nSkills: {', '.join(resume.skills)}\n"
    
    if resume.workExperience and len(resume.workExperience) > 0:
        resume_context += "\nWORK EXPERIENCE:\n"
        for exp in resume.workExperience:
            duration = ""
            if exp.startDate:
                duration = f"({exp.startDate}"
                if exp.endDate:
                    duration += f" - {exp.endDate})"
                elif exp.currentPosition:
                    duration += " - Present)"
                else:
                    duration += ")"
            
            resume_context += f"- {exp.position} at {exp.company} {duration}\n"
            if exp.description:
                resume_context += f"  {exp.description}\n"
    
    if resume.education and len(resume.education) > 0:
        resume_context += "\nEDUCATION:\n"
        for edu in resume.education:
            duration = ""
            if edu.startDate:
                duration = f"({edu.startDate}"
                if edu.endDate:
                    duration += f" - {edu.endDate})"
                else:
                    duration += ")"
            
            edu_details = f"{edu.degree} in {edu.field}" if edu.field else edu.degree
            resume_context += f"- {edu_details} from {edu.institution} {duration}\n"
            if edu.gpa:
                resume_context += f"  GPA: {edu.gpa}\n"
    
    # Build job context
    job_context = ""
    if request.jobTitle or request.companyName:
        job_context = "JOB INFORMATION:\n"
        if request.jobTitle:
            job_context += f"Position: {request.jobTitle}\n"
        if request.companyName:
            job_context += f"Company: {request.companyName}\n"
    
    # Create the main prompt
    prompt = f"""You are an AI assistant that helps generate professional responses for job application forms.
I will provide you with information about a job applicant and the form fields they need to fill out.
Your task is to generate appropriate responses for each field based on the applicant's resume and the job details.

{job_context}

{resume_context}

Now, please generate responses for the following form fields. For each field:
1. Consider what would be an appropriate response based on the applicant's background and the field's purpose
2. If the field has specific options, ONLY choose from those options
3. Be professional, concise, and honest - don't fabricate experience that isn't in the resume
4. Format your responses as follows:

FIELD_ID: [id number]
RESPONSE: [your generated response]

Here are the fields:

"""

    for field in request.formFields:
        label = field.fieldLabel if field.fieldLabel else "Unlabeled Field"
        field_type = field.fieldType
        required = "Required" if field.required else "Optional"
        options = f", Options: {', '.join(field.options)}" if field.options else ""
        
        prompt += f"Field ID: {field.id}\n"
        prompt += f"Label: {label}\n"
        prompt += f"Type: {field_type}\n"
        prompt += f"{required}{options}\n\n"
    
    return prompt

def parse_response_generation(ai_response: str, form_fields: List[FormField]) -> AIResponse:
    """Parse the AI's response generation results"""
    field_responses = []
    
    # Use regex to extract field ID and response pairs
    pattern = r"FIELD_ID:\s*(\d+)\s*\nRESPONSE:\s*([\s\S]*?)(?=\n\s*FIELD_ID:|$)"
    matches = re.finditer(pattern, ai_response)
    
    for match in matches:
        try:
            field_id = int(match.group(1))
            response_text = match.group(2).strip()
            
            # Check if field_id exists in the form_fields
            if any(field.id == field_id for field in form_fields):
                field_responses.append(FieldResponse(
                    fieldId=field_id,
                    fieldValue=response_text
                ))
        except Exception as e:
            print(f"Error parsing field response: {e}")
    
    return AIResponse(
        fieldResponses=field_responses,
        buttonAction=None,
        isSubmissionComplete=False,
        message="Generated responses for form fields"
    )