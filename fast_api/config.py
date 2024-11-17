from dotenv import load_dotenv
import os

# load the environment variables
load_dotenv()


FRAPPE_URL = os.getenv("FRAPPE_URL")
FRAPPE_USERNAME = os.getenv("FRAPPE_USERNAME")
FRAPPE_PASSWORD = os.getenv("FRAPPE_PASSWORD")
