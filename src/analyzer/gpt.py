import pandas as pd
from openai import OpenAI

from src.config import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)


def process_data():
    raw_df = pd.read_csv("data/raw_data.csv")
    total_rows = raw_df.shape[0]
    processed_data = []

    for i, row in raw_df.iterrows():
        prompt = (
            "Анализируйте следующий текст и извлеките из него следующую информацию:\n\n"
            f"Текст: {row['text']}\n\n"
            "1. Ключевые слова/теги\n"
            "2. Краткое описание идеи/продукта\n"
            "3. Длинное описание\n"
            "4. Название компании\n"
            "5. Личности, упоминаемые в тексте\n"
            "6. Потенциал проекта, его применимость и польза\n\n"
            "Пожалуйста, предоставьте ответы в следующем формате:\n"
            "1. tags: ...\n"
            "2. long_desc: ...\n"
            "3. short_desc: ...\n"
            "4. company_name: ...\n"
            "5. personalities: ...\n"
            "6. potential: ..."
        )

        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="gpt-3.5-turbo",
            max_tokens=1000,
            n=1,
        )

        gpt_text = chat_completion.choices[0].message.content.strip()
        parsed_response = parse_gpt_response(gpt_text)
        parsed_response["source_type"] = "tg"
        parsed_response["source_link"] = row["source"]
        processed_data.append(parsed_response)
        print(f"GPT Analyzer: {int(str(i)) + 1}/{total_rows}")

    processed_df = pd.DataFrame(processed_data)
    processed_df.to_csv("data/processed_data.csv", index=False)


def parse_gpt_response(response: str) -> dict:
    lines = response.split("\n")
    result = {}

    for line in lines:
        parts = line.split(":", 1)
        if len(parts) == 2:  # noqa: PLR2004
            key, value = parts
            key = key.strip()
            value = value.strip()
            if ". " in key:
                key = key.split(". ")[1]
            result[key] = value

    return result
