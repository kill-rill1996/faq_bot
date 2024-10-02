import os
import dotenv

dotenv.load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMINS = [str(user_id) for user_id in os.getenv("ADMINS").split(",")]
# GROUP_ID = os.getenv("GROUP_ID")
SQL_URL = os.getenv("SQLITE_URL")

