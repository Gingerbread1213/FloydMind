## FloydMind

### Introduction

FloydMind is a sophisticated mental health assistant application designed to provide users with an empathetic conversational AI and a suite of classic games for relaxation and cognitive engagement. The application aims to support mental well-being by combining state-of-the-art AI technologies with interactive recreational activities.

<div align="center">
  <img src="/assets/markdown/demo.gif" alt="App Preview" width="300">
</div>


### Background

In today's fast-paced world, mental health has become a crucial aspect of overall well-being. However, access to mental health resources is often limited due to barriers such as stigma, cost, and availability. FloydMind addresses this gap by offering an accessible platform that empowers users to:
+ **Engage in Supportive Conversations:** Our AI chatbot is meticulously trained on diverse mental health dialogues to provide compassionate and helpful interactions.
+ **Enjoy Recreational Activities:** A selection of classic games is included to offer stress relief and promote cognitive function, contributing positively to mental health.
By integrating conversational AI with interactive gaming, FloydMind delivers a holistic approach to mental wellness, grounded in expert methodologies and data-driven practices.

### Features

+ **Advanced Conversational AI Chatbot:** Trained on extensive mental health datasets to deliver empathetic and contextually appropriate responses.
+ **Classic Games Suite:** Includes Tic-Tac-Toe, Memory Matching, Hangman, Snake, and Tetris, implemented with engaging graphics and smooth gameplay.
+ **Intuitive GUI:** Built with PyQt5 to ensure a seamless and user-friendly interface.
+ **Enhanced User Engagement:** Incorporates background music and animations to create an immersive experience.
+ **Customizable Settings:** Offers adjustable music volume and other preferences to tailor the experience to individual needs.

### Installation

#### Prerequisites

+ Anaconda: Recommended for managing Python environments.
+ Python: Version 3.7 or higher.

#### Steps
1. Clone the Repository
```
git clone https://github.com/Gingerbread1213/FloydMind.git
cd path_to/FloydMind
```

2. Install Dependencies
Create and activate a new conda environment (optional but recommended):

```
conda create -n floydmind_env python=3.12
conda activate floydmind_env
```

Install PyQt5 using conda:
```
conda install pyqt
```

Install the remaining dependencies using pip:
```
pip install .
```
This will install all the required Python packages specified in setup.py or requirements.txt.

## Usage

### Running the Application

```bash
python main.py
```

## Data Files

Ensure that all necessary data files are placed in their respective directories(optional: only if you like to make a further training to the model):

- **`Mental_Health_FAQ.csv`** and **`oneHotData.csv`**: Place these files in the project root directory.
- **MentalLLaMA Data**: Place the datasets in the `MentalLLaMA/train_data/` directory.
- **Background Media**:
  - `bgm.mp3`: Background music file, placed in the project root.
  - `background.gif`: Background animation, placed in the project root.

## Data Sources and Manipulation

### Data Sources

The AI chatbot was trained on a comprehensive collection of datasets to ensure a wide-ranging and nuanced understanding of mental health conversations:

1. **Mental Health FAQ Dataset (`Mental_Health_FAQ.csv`)**

   - **Description**: Contains frequently asked questions and answers on mental health topics.
   - **Usage**: Provides foundational knowledge for common mental health inquiries.

2. **Custom Local Dataset (`oneHotData.csv`)**

   - **Description**: A bespoke dataset with additional question-answer pairs.
   - **Preprocessing**: Cleaned by removing HTML tags and special characters to ensure data quality.

3. **Empathetic Dialogues Dataset**

   - **Source**: Hugging Face's [EmpatheticDialogues](https://huggingface.co/datasets/empathetic_dialogues).
   - **Description**: Consists of over 24,000 one-on-one conversations grounded in emotional contexts.
   - **Processing**: Structured into question-response pairs to maintain conversational coherence.

4. **Mental Health Chatbot Dataset**

   - **Source**: Hugging Face datasets (`heliosbrahma/mental_health_chatbot_dataset`).
   - **Processing**: Parsed combined texts to extract human and assistant dialogues using custom regular expressions.

5. **MentalLLaMA Dataset**

   - **Description**: A local dataset comprising instruction and complete data.
   - **Processing**: Merged relevant columns and handled missing data to create a consistent dataset.

### Data Manipulation

To prepare the datasets for training, rigorous data manipulation techniques were employed:

1. **Data Cleaning**

   - **HTML Tag Removal**: Utilized regular expressions to strip HTML tags.
   - **Normalization**: Removed extraneous whitespace and special tokens.

2. **Data Structuring**

   - **Question-Response Pairing**: Ensured all data conformed to a consistent question and response format.
   - **Tag Parsing**: Employed advanced parsing methods to accurately split combined texts.

3. **Data Integration**

   - **Merging Datasets**: Concatenated all datasets into a unified DataFrame, ensuring alignment of columns and data types.
   - **Deduplication**: Removed duplicate entries to enhance dataset integrity.

4. **Politeness Augmentation**

   - **Custom Politeness Templates**: Crafted a set of polite phrases to enhance the assistant's responses.
   - **Application Logic**: Implemented probabilistic insertion of polite starters and enders to simulate natural language patterns.

5. **Formatting for Training**

   - **Special Token Insertion**: Incorporated special tokens to delineate the start and end of texts.
   - **Contextual Formatting**: Structured the data to include conversation history, improving model context awareness.

6. **Dataset Splitting**

   - **Training and Validation Sets**: Used `train_test_split` to create robust training and evaluation datasets.

7. **Tokenization and Encoding**

   - **Tokenizer Customization**: Added special tokens to the tokenizer and resized the model's embedding layer accordingly.
   - **Efficient Encoding**: Tokenized texts with truncation and padding to standardize input lengths.

8. **Data Collation**

   - **Custom Data Collator**: Developed a collator to correctly format tensors for the training loop, ensuring optimal performance.

By meticulously manipulating the data, the model was primed to deliver high-quality, empathetic responses, adhering to expert standards in natural language processing.










