import requests
import os
sheety_users_put_get_endpoint = os.environ['sheety_users_put_get_endpoint']


print("Welcome to Melisa's Flight Club")
print("We find the best flight deals and email you.")

going_on = True
while going_on:
  user_name = input("What is your first name?\n").capitalize()
  user_lastname = input("What is your last name?\n").capitalize()
  user_email = input("What is your email?\n")
  check_email = input("Type your email again.\n")
  if user_email == check_email:
    response = requests.get(url=sheety_users_put_get_endpoint)
    response.raise_for_status
    data = response.json()
    data_len = int(len(data['users']))
    data_len += 2
    params = {
      "user": {
        "firstName": user_name,
        "lastName": user_lastname,
        "email": user_email,
      }
    }
    put_url = f"{sheety_users_put_get_endpoint}/{data_len}"
    put_response = requests.put(url=put_url, json=params)
    put_response.raise_for_status()
    going_on = False
  else:
    print("Your answers do not match please try again!")
print("Success! Your email has been added, look forwards")    
  
