import easyocr
from transformers import pipeline
import requests


def extract_text_from_image(image_path):
    reader = easyocr.Reader(['ch_sim','en']) # this needs to run only once to load the model into memory
    # ocr_result = reader.readtext('Screenshot from 2024-11-13 14-44-09.png')
    ocr_result = reader.readtext(image_path)
    
    # print(type(result[0][0]))
    # print(result)
    # print(result[4][1])

    texts = [item[1] for item in ocr_result]

    # print(texts)

    # Printing the result
    t=''
    for text in texts:
        t+=text
        # print(text)
    print(t)
    return t



def text_analysis(text):
    classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
    # text = "The local team won the championship!"
    # text = extract_text_from_image()
    labels = ["sports", "politics", "entertainment", "business", "technology"]
    result = classifier(text, candidate_labels=labels)
    # print(type(result))
    # print(result)
    # return result

    max_score_index = result['scores'].index(max(result['scores']))
    highest_label = result['labels'][max_score_index]
    highest_score = result['scores'][max_score_index]

    return highest_label



def get_recommendations(news_type):
    api_key = "28f8c73872bd4ad38b4937eed3159081"  # Replace with your actual API key
    url = f'https://newsapi.org/v2/everything?q={news_type}&language=en&sortBy=relevancy&apiKey={api_key}'

    response = requests.get(url)
    if response.status_code == 200:
        articles = response.json().get('articles', [])
        recommendations = [(article['title'], article['url']) for article in articles]
        return recommendations[:5]  # Return top 5 recommendations
    else:
        print("Error fetching recommendations:", response.status_code)
        return []





if __name__ == "__main__":
    text = extract_text_from_image('/home/intelgic/roddur/project/Screenshot from 2024-11-13 14-44-09.png')
    news_type = text_analysis(text)
    print("news_type ::: ",news_type)
    print(get_recommendations(news_type))
    # recomemendations=get_recommendations(news_type)

    # for i in recomemendations:
    #     print(i[0])
    
