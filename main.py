import aiohttp
import asyncio
import random
import requests
import json
import time

async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()

async def check_item(session, webhook_url, item_id, start_id, end_id):
    try:
        start_time = time.time()
        results = []

        for user_id in range(start_id, end_id + 1):
            url = f'https://inventory.roblox.com/v1/users/{user_id}/items/0/{item_id}/is-owned'
            is_owned_str = await fetch(session, url)

            print(f'Sending API request for user ID: {user_id}')

            if is_owned_str == 'true':
                print(f'A user with the item found! User ID: {user_id}')
                results.append(str(user_id))

        if results:
            results_str = '\n'.join(results)

            
            with open('scrape.txt', 'w') as file:
                file.write(results_str)

            
            try:
                with open("webhook.txt", "r") as webhook_file:
                    webhook_url = webhook_file.read().strip()
            except FileNotFoundError:
                print("webhook.txt not found. Please create the file and add your webhook URL.")
                return
            except Exception as e:
                print(f'Error reading webhook.txt: {e}')
                return

            
            payload = {
                "content": "Results:",
                "file": ("scrape.txt", open('scrape.txt', 'rb'))
            }

            
            response = requests.post(webhook_url, files=payload)

            
            print(response.status_code, response.text)
            print("Option 1 completed. Results sent to Discord.")

            
            duration_message = f"Scrape took {time.time() - start_time:.2f} seconds."
            requests.post(webhook_url, data={"content": duration_message})

            
            with open('scrape.txt', 'w'):
                pass
        else:
            print("No users with the item found.")

    except Exception as e:
        print(f'Error sending to webhook: {e}')
    finally:
        end_time = time.time()
        print(f"Scrape took {end_time - start_time:.2f} seconds.")

async def perform_option_2(session, webhook_url, start_id, end_id):
    try:
        start_time = time.time()
        results = []

        for user_id in range(start_id, end_id + 1):
            url = f'https://users.roblox.com/v1/users/{user_id}'
            user_data_str = await fetch(session, url)

            print(f'Sending API request for user ID: {user_id}')

            try:
                user_data = json.loads(user_data_str)
                user_name = user_data.get("name", "")

                if "123" in user_name:
                    print(f'A user with "123" in the name found! User ID: {user_id}')
                    results.append(str(user_id))
            except Exception as e:
                print(f'Error processing user data for user ID {user_id}: {e}')

        if results:
            results_str = '\n'.join(results)

            
            with open('scrape_123.txt', 'w') as file:
                file.write(results_str)

            
            payload = {
                "content": "Results with '123' in the name:",
                "file": ("scrape_123.txt", open('scrape_123.txt', 'rb'))
            }

            
            response = requests.post(webhook_url, files=payload)

            
            print(response.status_code, response.text)
            print("Option 2 completed. Results sent to Discord.")

            
            duration_message = f"Scrape took {time.time() - start_time:.2f} seconds."
            requests.post(webhook_url, data={"content": duration_message})

            
            with open('scrape_123.txt', 'w'):
                pass
        else:
            print("No users with '123' in the name found.")

    except Exception as e:
        print(f'Error performing option 2: {e}')
    finally:
        end_time = time.time()
        print(f"Scrape took {end_time - start_time:.2f} seconds.")

async def perform_option_3(session, webhook_url, start_id, end_id):
    try:
        start_time = time.time()
        name_prefix = input("Enter the name prefix: ")
        results = []

        for user_id in range(start_id, end_id + 1):
            url = f'https://users.roblox.com/v1/users/{user_id}'
            user_data_str = await fetch(session, url)

            print(f'Sending API request for user ID: {user_id}')

            try:
                user_data = json.loads(user_data_str)
                user_name = user_data.get("name", "")

                if name_prefix.lower() in user_name.lower():
                    print(f'A user with "{name_prefix}" in the name found! User ID: {user_id}')
                    results.append(str(user_id))
            except Exception as e:
                print(f'Error processing user data for user ID {user_id}: {e}')

        if results:
            results_str = '\n'.join(results)

            
            with open(f'scrape_{name_prefix}.txt', 'w') as file:
                file.write(results_str)

            
            payload = {
                "content": f"Results with '{name_prefix}' in the name:",
                "file": (f"scrape_{name_prefix}.txt", open(f'scrape_{name_prefix}.txt', 'rb'))
            }

            
            response = requests.post(webhook_url, files=payload)

            
            print(response.status_code, response.text)
            print("Option 3 completed. Results sent to Discord.")

            
            duration_message = f"Scrape took {time.time() - start_time:.2f} seconds."
            requests.post(webhook_url, data={"content": duration_message})

            
            with open(f'scrape_{name_prefix}.txt', 'w'):
                pass
        else:
            print(f"No users with '{name_prefix}' in the name found.")

    except Exception as e:
        print(f'Error performing option 3: {e}')
    finally:
        end_time = time.time()
        print(f"Scrape took {end_time - start_time:.2f} seconds.")

async def main():
    try:
        print("[1] - Item scraper")
        print("[2] - 123 scraper")
        print("[3] - Name scraper")
        option = input("Select an option: ")

        if option == "1":
            item_id = input("Item ID: ")
            start_id = int(input("Start ID: "))
            end_id = int(input("Finish ID:"))

            
            try:
                with open("webhook.txt", "r") as webhook_file:
                    webhook_url = webhook_file.read().strip()
            except FileNotFoundError:
                print("webhook.txt not found. Please create the file and add your webhook URL.")
                return
            except Exception as e:
                print(f'Error reading webhook.txt: {e}')
                return

            async with aiohttp.ClientSession() as session:
                await check_item(session, webhook_url, item_id, start_id, end_id)

        elif option == "2":
            start_id = int(input("Start ID: "))
            end_id = int(input("Finish ID:"))

            
            try:
                with open("webhook.txt", "r") as webhook_file:
                    webhook_url = webhook_file.read().strip()
            except FileNotFoundError:
                print("webhook.txt not found. Please create the file and add your webhook URL.")
                return
            except Exception as e:
                print(f'Error reading webhook.txt: {e}')
                return

            async with aiohttp.ClientSession() as session:
                await perform_option_2(session, webhook_url, start_id, end_id)

        elif option == "3":
            start_id = int(input("Start ID: "))
            end_id = int(input("Finish ID:"))

            
            try:
                with open("webhook.txt", "r") as webhook_file:
                    webhook_url = webhook_file.read().strip()
            except FileNotFoundError:
                print("webhook.txt not found. Please create the file and add your webhook URL.")
                return
            except Exception as e:
                print(f'Error reading webhook.txt: {e}')
                return

            async with aiohttp.ClientSession() as session:
                await perform_option_3(session, webhook_url, start_id, end_id)

        else:
            print("Invalid option selected.")

    except Exception as e:
        print(f'Error: {e}')

asyncio.run(main())
