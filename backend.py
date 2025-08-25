from fastapi import FastAPI
from pydantic import BaseModel
import httpx
import json

app = FastAPI()

API_URL = "http://localhost:11434/api/generate"

class EmailRequest(BaseModel):
    category: str
    sender_name: str
    receiver_name: str
    subject: str
    details: str


async def query_ollama(prompt: str) -> str:
    """
    Send a prompt to Ollama and return the response
    :param prompt: prompt
    :return: response from Ollama
    """

    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(
            API_URL,
            json={
                "model": "llama3",
                "prompt": prompt,
                "stream": False
            },
            timeout=90
        )
        try:
            data = json.loads(response.text)
            return data["response"]
        except json.JSONDecodeError as e:
            return f"Error decoding JSON: {str(e)}\nRaw response: {response.text}"


async def define_prompt_send(email: EmailRequest) -> str:
    """
    Define the prompt dependent on the category.
    :param email: information the mail should contain
    :return: defined prompt.
    """

    prompt = (f"ONLY GIVE THE EMAIL CONTENT BACK WITHOUT ANY OTHER TEXT."
              f"Here are things you need to know about the receiver's name. If it starts with Dr. ,Prof. ,Lect. ,Mr. or Mrs. the email should be written in the form of a formal letter, "
              f"otherwise it should be written in the form of a casual letter."
              f"Based on this subject: {email.subject},")

    if email.category == "Inquiry":
        prompt += f"generate an inquiry email from {email.sender_name} to {email.receiver_name} based on the following information: {email.details}"
    elif email.category == "Request":
        prompt += f"generate a request email from {email.sender_name} to {email.receiver_name} based on the following information: {email.details}"
    elif email.category == "Complaint":
        prompt += f"generate a complaint email from {email.sender_name} to {email.receiver_name} based on the following information: {email.details}"
    elif email.category == "Thank you":
        prompt += f"generate a thank you email from {email.sender_name} to {email.receiver_name} based on the following information: {email.details}"
    elif email.category == "Information":
        prompt += f"generate an information email from {email.sender_name} to {email.receiver_name} based on the following information: {email.details}"
    elif email.category == "Confirmation":
        prompt += f"generate a confirmation email from {email.sender_name} to {email.receiver_name} based on the following information: {email.details}"
    elif email.category == "Apology":
        prompt += f"generate an apology email from {email.sender_name} to {email.receiver_name} based on the following information: {email.details}"
    elif email.category == "Reminder":
        prompt += f"generate a reminder email from {email.sender_name} to {email.receiver_name} based on the following information: {email.details}"
    elif email.category == "Invitation":
        prompt += f"generate an invitation email from {email.sender_name} to {email.receiver_name} based on the following information: {email.details}"
    else:
        prompt += f"generate an email from {email.sender_name} to {email.receiver_name} based on the following information: {email.details}"

    return prompt


async def assist_report(email: EmailRequest) -> str:
    """
    Get the generated email from Ollama
    :param email: request object containing the email details
    :return: generated email
    """
    prompt = await define_prompt_send(email)
    generated_mail = await query_ollama(prompt)
    return generated_mail


@app.post("/generate_email")
async def generate_email(email: EmailRequest):
    """
    API endpoint for the generated email
    :param email: request object containing the email details
    :return: generated email
    """
    generated_email = await assist_report(email)
    return {"generated_email": generated_email}



