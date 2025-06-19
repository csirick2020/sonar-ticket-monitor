# Test Sonar (GraphQL) API Endpoint

''' Use this module to simply test whether or not your API endpoint is
responding before having to customize your ticket monitor section '''

import requests
import os
from dotenv import load_dotenv

def test_endpoint():
    load_dotenv()  # This loads variables from .env into the environment

    # Set local variables from .env file
    API_KEY = os.getenv("SONAR_API_KEY")
    GRAPHQL_URL = os.getenv("GRAPHQL_URL")

    # Make sure keys were loaded correctly
    if API_KEY is None or GRAPHQL_URL is None:
        raise ValueError("API_KEY or GRAPHQL_URL environment variable is not set")

    # Simple GraphQL query to test the endpoint
    query = """
    {
      __schema {
        queryType {
          name
        }
      }
    }
    """

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(GRAPHQL_URL, json={'query': query}, headers=headers)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)

        # Print the status code and response
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"Other error occurred: {err}")


if __name__ == "__main__":
    test_endpoint()
