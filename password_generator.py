import asyncio
import random
import string


# Asynchronous password generation function
async def generate_password(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for _ in range(length))

async def generate_multiple_passwords(n, length, log_text):
    try:
        tasks = [generate_password(length) for _ in range(n)]
        passwords = await asyncio.gather(*tasks)
        log_text.insert("end", "Generated Passwords:\n")
        for idx, password in enumerate(passwords, start=1):
            log_text.insert("end", f"{idx}: {password}\n")
        log_text.insert("end", "Password generation completed!\n")
    except Exception as e:
        log_text.insert("end", f"Error: {e}\n")