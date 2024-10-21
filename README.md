---
license: unknown
task_categories:
- text-classification
- question-answering
- text-generation
- text2text-generation
language:
- de
tags:
- art
pretty_name: Structured Stern NEON Community Articles
size_categories:
- 10K<n<100K
---

# Structured Stern NEON Community Articles

This repository contains approximately 5k user written texts,
articles, and poetry pulled from archives of the Stern NEON website.

Stern NEON was a community platform where users could write and publish their own articles.
Many of the articles are personal stories, poems, or opinion pieces.

The articles are structured in a way that they can be used for further analysis.

## Dataset Details

### Dataset Description

- **Curated by:** [Lukas Wolfsteiner (lukas@wolfsteiner.media)](https://lukas.wolfsteiner.media/)
- **Language(s) (NLP):** German
- **License:** Unknown

## Uses

This dataset can be used for text classification, question answering, text generation, and text-to-text generation tasks.

### Direct Use

- **Text Classification**: The dataset can be used to train a model to classify articles into different categories.
- **Question Answering**: The dataset can be used to train a model to answer questions about the articles.
- **Text Generation**: The dataset can be used to train a model to generate new articles.
- **Text-to-Text Generation**: The dataset can be used to train a model to generate summaries of the articles.

### Out-of-Scope Use

- **Sentiment Analysis**: The dataset is not labeled for sentiment analysis tasks.
- **Named Entity Recognition**: The dataset is not labeled for named entity recognition tasks.
- **Machine Translation**: The dataset is not labeled for machine translation tasks.
- **Speech Recognition**: The dataset is not labeled for speech recognition tasks.
- **Image Recognition**: The dataset is not labeled for image recognition tasks.
- **Object Detection**: The dataset is not labeled for object detection tasks.

## Dataset Structure

The main structure of the dataset is as follows:

1. Articles are stored as line-separated JSON objects.
2. An article consists of the following properties:
    - `title`: The title of the article.
    - `subtitle`: An optional subtitle, null if no subtitle was provided
    - `text`: The actual text content of an article
    - `created`: Timestamp of the release date
    - `author`: Username of who wrote it
    - `profile_url`: URL to the author's profile
    - `url`: Original URL where this article can be found
    - `main_category`: Main article category
    - `sub_category`: Secondary article category
    - `id`: ID of the article

### Example Entry

```json
{
  "created":1190362560,
  "author":"Wortfechter",
  "profile_url":"http://www.neon.de/user/Wortfechter",
  "title":"Kopftuch im Flughafen",
  "subtitle":"In Teheran ist das Kopftuch gesetzlich vorgeschrieben. Auch im Flughafen.",
  "text":"Auf unserem Weg nach Kambodscha führte uns unser Flug über Teheran nach Bangkok. Das erste, was wir auf unserer Reise also zu sehen bekommen sollten, war der Sicherheitsbereich im Imam Khomeini Airport in Teheran. Alle Mädels waren bestens ausgerüstet mit langen Klamotten und Tüchern, die sie mehr oder weniger professionell um ihren Kopf zu wickeln versuchten. Da in Teheran das Kopftuch für Frauen gesetzlich vorgeschrieben ist, mussten auch wir auf dem Flughafen alles außer unserer Hände und Gesichter verdecken.\n   \n\n   Als ich nun also mehr schlecht als recht eingewickelt aus dem Flugzeug stolperte, wurde ich vom Passkontrolleur erstmal gefragt, ob ich denn Muslimin sei. Auf meine Verneinung hin wollte er wissen, warum ich denn dann ein Kopftuch trage. Sehr witzig, der Mann.\n   \n   Im Flughafen war es natürlich warm, unter den Kopftüchern war es natürlich noch wärmer und in langen Klamotten erst recht. Zunächst wurden wir mit riesigen Muffins und Kaffee/Cola/Wasser for free doch recht nett begrüßt, doch nach einigen Stunden wurde es verdammt nervig. Es würde mich nicht wundern, wenn einige der Mädels eine richtige Abneigung entwickeln würden gegen dieses Land, in dem man als Frau selbst auf dem Flughafen alles außer der Hände und dem Gesicht verdecken muss. Nicht, dass wir halbnackt durch den Flughafen hüpfen wollten, aber bei den Temperaturen wäre ein T-Shirt schon was Feines gewesen. Im Flugzeug wurden vorsorglich an alle Unwissenden Kittel verteilt, auf dem Rückflug gab es sogar Kopftücher, dafür aber auch deutsche Touris, die aussahen, als würden sie in Thailand einen ganz bestimmten Tourismus pflegen und unsere Mädels anpöbelten, weil sie \"zu lange\" am öffentlichen internetfähigen Rechner standen.\n   \n   Als wir die Kopftücher nach einiger Zeit lüfteten, wurden wir gleich dezent darauf hingewiesen, dass es Vorschrift sei, sie zu tragen. Keine Begründung. Einfach nur \"That's a rule\" - and that's it.\n   \n\n   Bei allem Verständnis für andere Kulturen und Sitten fühlte ich mich - unter meinem Kopftuch schwitzend - ein wenig in meiner persönlichen Freiheit eingeschränkt.",
  "url":"http://www.neon.de:80/artikel/kaufen/reise/kopftuch-im-flughafen/652640",
  "archive_url":"https://web.archive.org/web/20140815233601/http://www.neon.de:80/artikel/kaufen/reise/kopftuch-im-flughafen/652640",
  "main_category":"kaufen",
  "sub_category":"reise",
  "id":652640
}
```

## Dataset Creation

### Curation Rationale

The dataset was created to provide a structured dataset of user-written articles from the Stern NEON website.

### Source Data

#### Initial Data Collection and Normalization

The dataset was created by scraping multiple archives of the Stern NEON website, including the Wayback Machine.

The link to the original archived article is included in the dataset (`archive_url`).

#### Data Collection and Processing

The data was collected using the `waybackpy` Python package, which allows for easy access to the Wayback Machine API.

The data was then processed to extract the relevant information from the HTML pages.

#### Who are the source data producers?

Data was produced by users of the Stern NEON website.
The data was collected from the Wayback Machine archives.

#### Personal and Sensitive Information

The dataset contains personal stories, poems, and opinion pieces written by users of the Stern NEON website.

## Bias, Risks, and Limitations

The time range of the articles is from 2009 to 2016.

The dataset may not be representative of the current state of the Stern NEON website.

### Recommendations

When using this dataset, consider the following:

- The dataset may contain personal stories and opinions that may not be representative of the general population.
- The dataset may contain sensitive information that should be handled with care.
- The dataset may contain outdated information.
- The dataset may contain biased or offensive content.
- The dataset may contain errors or inaccuracies.
- The dataset may not be suitable for all audiences.
- The dataset may not be suitable for all research purposes.
- The dataset may not be suitable for all machine learning tasks.
- The dataset may not be suitable for all natural language processing tasks.

## More Information

- [Stern Neon website](https://www.stern.de/neon/)
- [waybackpy](https://github.com/akamhy/waybackpy)
- [waybackpy documentation](https://waybackpy.readthedocs.io/en/latest/)
- https://github.com/akamhy/waybackpy?tab=readme-ov-file#retrieve-archive-of-webpage
- https://peyanski.com/automatic-home-assistant-backup-to-github/
- https://huggingface.co/docs/datasets/share
- https://www.digitalocean.com/community/tutorials/python-multiprocessing-example
