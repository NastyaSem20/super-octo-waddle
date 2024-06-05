from django.shortcuts import render
from .forms import PhoneNumberForm
from telethon import TelegramClient
from telethon.errors.rpcerrorlist import PhoneNumberInvalidError
from telethon.tl.functions.contacts import ImportContactsRequest
from telethon.tl.types import InputPhoneContact
from asgiref.sync import async_to_sync
import os


api_id = ''
api_hash = ''


async def fetch_user_info(phone_number):
    client = TelegramClient('session_name', api_id, api_hash)
    await client.connect()

    try:
        result = await client(ImportContactsRequest(
            [InputPhoneContact(client_id=0, phone=phone_number, first_name="Temp", last_name="User")]))
        user = result.users[0] if result.users else None

        if user:
            user_info = {
                'user_id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'username': user.username,
                'phone': user.phone,
                'photos': []
            }

            if user.photo:
                photos = await client.get_profile_photos(user)
                if photos:
                    os.makedirs('media/profile_photos', exist_ok=True)
                    for i, photo in enumerate(photos):
                        path = f"media/profile_photos/{user.id}_photo_{i}.jpg"
                        print(path)
                        await client.download_media(photo, file=path)
                        user_info['photos'].append(path)

            return user_info
        else:
            return None

    except PhoneNumberInvalidError:
        return 'Invalid phone number'


def search_user(request):
    if request.method == 'POST':
        form = PhoneNumberForm(request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data['phone_number']
            user_info = async_to_sync(fetch_user_info)(phone_number)
            return render(request, 'result.html', {'user_info': user_info})
    else:
        form = PhoneNumberForm()

    return render(request, 'search.html', {'form': form})