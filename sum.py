from groq import Groq
from dotenv import load_dotenv
import re


def summarize_text(promt):
    completion = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {
                "role": "system",
                # "content": "Australian chief selectorGeorge Bailey has responded tocriticisni fromi former Test opener Ed Cawan, who questionedthe selection ofNathan McSweeney35 ADOpener for theucoming Border-Gavaskar Trophy apener against India。Cowan labeled McSweeney's promotion asguessdue t0 hislimited experience opening the batting:Last week; Clicket Australia revealed the I3-nafor theseries opener i Perth, stalting November 22ndTheannouncement confirmed McSweeney would open the battingWith usman khawaja.\n\n\nthis is my text. give me some keywords which i can use for my recommendation system"
                "content": promt,
            },
            # {
            #     "role": "user",
            #     "content": "summarize the content and give me some keywords which i can use for my recommendation system\n"
            # }
        ],
        temperature=1,
        max_tokens=1024,
        top_p=1,
        stream=True,
        stop=None,
    )
    summary = ""
    for chunk in completion:
        # print(chunk.choices[0].delta.content)
        # print("================")
        # print(chunk.choices[0].delta.content or "", end="")
        # print("\n")
        summary += chunk.choices[0].delta.content or ""
    # print(summary)
    return summary


def get_keywords(summary):
    keyword_completion = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {
                "role": "system",
                # "content": "Australian chief selectorGeorge Bailey has responded tocriticisni fromi former Test opener Ed Cawan, who questionedthe selection ofNathan McSweeney35 ADOpener for theucoming Border-Gavaskar Trophy apener against India。Cowan labeled McSweeney's promotion asguessdue t0 hislimited experience opening the batting:Last week; Clicket Australia revealed the I3-nafor theseries opener i Perth, stalting November 22ndTheannouncement confirmed McSweeney would open the battingWith usman khawaja.\n\n\nthis is my text. give me some keywords which i can use for my recommendation system"
                "content": summary,
            },
            {
                "role": "user",
                "content": f" give me some keywords, based on {summary} which i can use for my recommendation system,also add the main topic name in front of every keywords\n",
            },
        ],
        temperature=1,
        max_tokens=1024,
        top_p=1,
        stream=True,
        stop=None,
    )

    keyword = ""
    for chunk in keyword_completion:
        # print(chunk.choices[0].delta.content)
        # print("================")
        # print(chunk.choices[0].delta.content or "", end="")
        # print("\n")
        keyword += chunk.choices[0].delta.content or ""

    print("-------------------------------------------")
    # print(keyword)

    keywords = re.findall(r"\d+\.\s+(.+)", keyword)
    cleaned_keywords = [keyword.lstrip("*").strip() for keyword in keywords]

    # Print the list of keywords
    print(cleaned_keywords)


if __name__ == "__main__":
    load_dotenv()
    client = Groq()
    promt = input("Enter a prompt: ")
    summary = summarize_text(promt)
    get_keywords(summary)
