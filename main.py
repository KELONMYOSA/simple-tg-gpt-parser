from src.analyzer.gpt import process_data
from src.parser.tg import get_raw_data

if __name__ == "__main__":
    get_raw_data()
    process_data()
