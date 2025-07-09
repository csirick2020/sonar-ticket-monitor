# Sonar API Tool - Ticket Monitor

# IMPORTANT: TO SET NECESSARY .ENV VARIABLES...
''' First, log into your Sonar account and get the API key by clicking the icon
that contains the first letter of your login name (in the top right corner)
and then navigating to Personal Access Tokens. (Be sure to paste the token
into a text file and save it as Sonar will only show it once).

Then, add the Sonar API key to a .env file as SONAR_API_KEY
Finally, add the GraphQL URL to your .env file as GRAPHQL_URL
The GraphQL URL will likely be in the following format:
https://YourOrganizationName.sonar.software/api/graphql '''

import requests
import os
import time
from datetime import datetime
from dotenv import load_dotenv
from win10toast import ToastNotifier

load_dotenv()  # This loads variables from .env into the environment

# Set local variables from .env file
API_KEY = os.getenv("SONAR_API_KEY")
GRAPHQL_URL = os.getenv("GRAPHQL_URL")

# Make sure keys were loaded correctly
if API_KEY is None or GRAPHQL_URL is None:
    raise ValueError("API_KEY or GRAPHQL_URL environment variable is not set")

# Set request headers
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# Define the GraphQL queries

'''NOTE: ticket_group_id will be found in Sonar settings and will be an integer. Each
ticket group (created by your organization) is assigned its own integer value by Sonar.

In this source code, we are only monitoring tickets from a ticket group called Helpdesk
(which has the integer value of 1 assigned to it). And we are only monitoring tickets with
a status equal to 'OPEN' or 'PENDING_INTERNAL' '''

query_open = """
{
  tickets(ticket_group_id: 1, status: OPEN) {
    entities {
      id
      subject
      status
      created_at
      updated_at
    }
  }
}
"""

query_pending_internal = """
{
  tickets(ticket_group_id: 1, status: PENDING_INTERNAL) {
    entities {
      id
      subject
      status
      created_at
      updated_at
    }
  }
}
"""


# Set to keep track of previously seen tickets
seen_ticket_ids = set()
''' NOTE: These do not persist across sessions
of using this program. This is only to tell
the program which tickets exist already
upon initialization, so that you don't get
X amount of notifications back to back when
you first start up the program. '''


# Function to fetch tickets
def get_tickets(query):
    response = requests.post(GRAPHQL_URL, headers=headers, json={'query': query})
    if response.status_code == 200:
        return response.json()['data']['tickets']['entities']
    else:
        print(f"Query failed to run with a {response.status_code}.")
        return []


# Function to notify about new tickets
def notify_new_tickets(new_tickets):
    current_time = datetime.now().strftime("%I:%M %p")
    print(f"New ticket found at {current_time} - Notification sent")
    # TODO: Figure out what the Error Message that comes up below
    # this print message is and (ideally) get rid of it.
    print("Error message: (Ignore)")  # Some strange WNDPROC return value and a TypeError...?
    toaster = ToastNotifier()
    for ticket in new_tickets:
        toaster.show_toast("New Ticket Notification",
                           f"Ticket ID: {ticket['id']}, Subject: {ticket['subject']}, Status: {ticket['status']}",
                           duration=10)  # duration = how many secs. toast notification stays visible
    print("Scanning for new tickets...")
    print()


# Initial fetch to populate seen_ticket_ids with existing tickets
def initialize_seen_tickets():
    tickets_open = get_tickets(query_open)
    tickets_pending_internal = get_tickets(query_pending_internal)
    all_tickets = tickets_open + tickets_pending_internal
    len_all_tickets_wrong = len(all_tickets)
    # For off by one error...(Not sure why we have to subtract 2, but subtract by 1 does not fix)
    len_all_tickets = len(all_tickets) - 2
    for ticket in all_tickets:
        seen_ticket_ids.add(ticket['id'])
    print()
    print(f"Initialization complete: {len_all_tickets} tickets currently in 'Helpdesk'")


# Main loop to check for new tickets
def main():

    initialize_seen_tickets()  # Populate seen_ticket_ids initially
    print()
    print("Scanning for new tickets...")
    print()

    while True:
        tickets_open = get_tickets(query_open)
        tickets_pending_internal = get_tickets(query_pending_internal)

        all_tickets = tickets_open + tickets_pending_internal

        new_tickets = [ticket for ticket in all_tickets if ticket['id'] not in seen_ticket_ids]

        if new_tickets:
            notify_new_tickets(new_tickets)
            seen_ticket_ids.update(ticket['id'] for ticket in new_tickets)

        time.sleep(30)  # Check every 30 seconds


if __name__ == "__main__":
    main()
