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

This repository contains approximately 16k user written texts,
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

### Example text through API

```bash
$ curl -X GET "https://datasets-server.huggingface.co/rows?dataset=dotwee%2Fstructured-stern-neon-articles&config=default&split=train&offset=0&length=1" | jq -r '.rows[0].row.text' | awk NF
Ich
frage mich, ob das wirklich ich bin. Ob das hier das Ergebnis ist, der
Schlussstrich, die Summe all dessen, was in einem Leben eben passiert. Die im
Spiegel, ist die mein Endprodukt?
     Nein.
Ich weiß, dass sich noch vieles ändern kann. Ich werde studieren und Freunde
finden, haben und vergessen. Ich werde arbeiten und Dinge aufbauen und
abreißen. Kinder haben, Vernünftig sein, aber trotzdem manchmal barfuß durch
die Straßen schlendern und Sonntagnachts malen.
     Ich
bin auf dem Weg dahin, ich weiß auch, dass irgendwann alles so sein wird, weil
in meinem Leben bisher alles geklappt hat. Weil am Ende immer alle glücklich waren.
Sorgen hin oder her, am Ende war da eine gute Note, ein Lob, ein bescheidenes
Lächeln und genug Leute, die mich am Wochenende warm gehalten haben.
     Jetzt
fühlt sich alles an wie bergab-gehen. Und immer wieder gehe ich in die Welt
hinaus, um das Schicksal herauszufordern, mich im Moment zu drehen, bis die
Lichter verschwimmen, bis die Decke an mir vorbeizieht, bis die Sterne hell
genug sind, um zum Gesprächsthema zu werden.
     Ich
weiß doch, dass Feierei und Leben nicht das gleiche ist. Dass es mehr gibt. Dass
mich Alkohol und Zigaretten und Gras gar nicht zu mir selbst führen, eher von
mir weg. Warum mache ich mir nicht mal Gedanken, statt nächtelang wieder alles auszublenden?
     Keine
Ahnung. Ist mir auch egal. Ich lese von Menschen, die Abstürzen und später
reich werden. Ich habe Angst um meine Zukunft aber es hat ja sonst immer alles
geklappt, diesmal auch, ganz sicher. Ich weiß, dass mich ein bisschen Absturz
am Wochenende nicht zum Sünder macht, eine Party mehr macht keinen No-Future
aus mir. Ich weiß das doch.
     Und
wenn ich wieder morgens aufwache und ich erinnere mich an die Szenarien der
vergangenen Nacht. Kopf über der Klobrille, schon wieder, schon wieder, so wie
jede Woche: am Ende wird sich übergeben und ab ins Bett. Und meine Freunde
machen schon Witze und sie halten mir die Haare. Sie sagen, eine Party, an der
ich nicht kotze, ist keine Party. Und ich finde das peinlich und verdammt
traurig. Das will ich doch nicht sein. Ich will an meine Grenzen gehen, ohne
sie zu erreichen. Eigentlich will ich einfach gar keine Grenzen haben.
     Und
ich nehme mir vor, jetzt wird alles anders. Ich nehme mir vor, dass Musik und
Liebe und Tanzen doch genug ist. Aber ist es eben nicht. Ich will mehr sein,
ich will überall sein, gleichzeitig und ich kann mich nie entscheiden. Ich weiß
doch, dass das alles normal ist, nur eine weitere Teenager-Geschichte, die
tausendste Sinnsuche, nur ein anderes Mädchen mit Augenringen und zu viel
Altglas in der Küche.
     Ich
bin mir gar nicht sicher, ob ich hier wirklich raus will. Abenteuer und mit
fremden Menschen tanzen, das wolltest du doch. Das alles hast du dir gewünscht.
Ich meinte doch selber immer, dass ich Vernunft doof finde. Schlecht für die
Zähne, zu dünn, ungesund und tote Gehirnzellen. War mir doch egal. Ist es auch
immer noch.
     Sonst
würde ich nächste Freitag-Nacht nicht das gleiche wieder tun. Wieder am Ende
mit ausgekotztem Magen im nächsten Fastfood-Laden landen. Über die miese Musik
ablästern, nach Hause taumeln oder mich tragen lassen, von Freunden. Mit Tüte
in der Hand, nur für den Fall.
     Klingt
ja widerlich. Aber am nächsten Tag wird ja doch noch gelacht. So endet das doch
immer. Am Ende lachen alle und wieder nichts gelernt. Braucht man doch auch
nicht.
     Am
Ende werde ich doch in einem Reihenhaus leben und Apfelkuchen backen und
Arzttermine in meinen Kalender eintragen. Am Ende wird alles gut und
langweilig, dafür darf jetzt alles aufregend sein und beschissen.
     Die,
die ich jetzt bin, ist ja noch nicht das Endprodukt. Das wird alles noch. Macht
euch keine Sorgen, so will ich ja langfristig gar nicht bleiben. Irgendwann
wird doch alles besser und gut und dann werde ich auch gesünder aussehen.
Morgen fängt das schon an.
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
