import asyncio
from telethon import TelegramClient

api_id = ''
api_hash = ''
login_phone_number = ''


async def main():
    client = TelegramClient('session_name', api_id, api_hash)

    await client.start()

    if not await client.is_user_authorized():
        await client.send_code_request(login_phone_number)
        code = input('Enter the code you received: ')
        await client.sign_in(login_phone_number, code)

    print("Login successful!")


if __name__ == '__main__':
    asyncio.run(main())