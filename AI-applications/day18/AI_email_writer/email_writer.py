import requests
def generate_email(sender_name,receiver_name,purpose,key_point,tone):
    prompt=f"""You are an AI Email Writer. Create a complete Email using the following information.
        Sender Name: {sender_name}
        Receipenet Name: {receiver_name}
        purpose: {purpose}
        Key points: {key_point}
        Tone: {tone}
        Instructions: Create a suitable subject.
        
        Include a greeting. Write a clear email.
        Use the provided key points. Do not invent information. 
        Keep the mail consize. Include a professional closing, Sign using the snder name. Return only the email"""
    
    url = "http://localhost:11434/api/generate"
    data ={
    "model": "llama3.2:3b",
    "prompt":prompt,
    "stream":False}
    response=requests.post(url,json=data)
    result=response.json()
    return result["response"]

print("=========================")
print("MADDY: AI EMAIL WRITER")
print("=========================")
sender_name=input("Your name:")
receiver_name=input("Receiver's name:")
purpose=input("Purpose:")
key_point=input("Key point:")
tone=input("Tone:")
email=generate_email(sender_name,receiver_name,purpose,key_point,tone)
print("==================")
print("Generated email")
print("==================")
print(email)
with open("generated_email.txt","w",encoding="UTF-8") as file:
    file.write(email)

print("\n Email generated saved to generated_email.txt")