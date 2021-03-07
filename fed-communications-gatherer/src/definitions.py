import os

# Root to the project
ROOT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir)
OUTPUT_DIR = os.path.join(ROOT_DIR, "output")
POLICY_STATEMENTS_OUTPUT_DIR = os.path.join(OUTPUT_DIR, "policy_statements")

FOMC_HOST_BASE_URL = "https://www.federalreserve.gov"
