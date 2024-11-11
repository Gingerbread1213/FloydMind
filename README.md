# FloydMind

# Table of Contents

- [Introduction](#introduction)
- [Background](#background)
- [Features](#features)
- [Frameworks and Technologies Used](#frameworks-and-technologies-used)
- [Detailed Implementation](#detailed-implementation)
  - [UI Implementation](#ui-implementation)
  - [Program Loop](#program-loop)
  - [AI Training](#ai-training)
  - [Model Usage](#model-usage)
  - [Data Sources and Manipulation](#data-sources-and-manipulation)
  - [Feature Vector Design](#feature-vector-design)
- [Code Structure](#code-structure)
  - [AI Model Training (`model_train.py`)](#ai-model-training-model_trainpy)
  - [Chatbot Model (`chatbot_model.py`)](#chatbot-model-chatbot_modelpy)
  - [User Interface](#user-interface)
    - [Base Window (`ui/base_window.py`)](#base-window-uibase_windowpy)
    - [Start Window (`ui/start_window.py`)](#start-window-uistart_windowpy)
    - [Chat Interface (`ui/chat_interface.py`)](#chat-interface-uichat_interfacepy)
    - [Game Menu (`ui/game_menu_window.py`)](#game-menu-uigame_menu_windowpy)
- [Installation](#installation)
  - [Prerequisites](#prerequisites)
  - [Steps](#steps)
- [Usage](#usage)
  - [Running the Application](#running-the-application)
- [Data Files](#data-files)
- [Data Sources and Manipulation](#data-sources-and-manipulation)
  - [Data Sources](#data-sources)
  - [Data Manipulation](#data-manipulation)


## Introduction

FloydMind is a sophisticated mental health assistant application designed to provide users with an empathetic conversational AI and a suite of classic games for relaxation and cognitive engagement. The application aims to support mental well-being by combining state-of-the-art AI technologies with interactive recreational activities.

<div align="center">
  <img src="/assets/markdown/demo.gif" alt="App Preview" width="300">
</div>

## Background

In today's fast-paced world, mental health has become a crucial aspect of overall well-being. However, access to mental health resources is often limited due to barriers such as stigma, cost, and availability. FloydMind addresses this gap by offering an accessible platform that empowers users to:

- **Engage in Supportive Conversations:** Our AI chatbot is meticulously trained on diverse mental health dialogues to provide compassionate and helpful interactions.
- **Enjoy Recreational Activities:** A selection of classic games is included to offer stress relief and promote cognitive function, contributing positively to mental health.

By integrating conversational AI with interactive gaming, FloydMind delivers a holistic approach to mental wellness, grounded in expert methodologies and data-driven practices.

## Features

- **Advanced Conversational AI Chatbot:** Trained on extensive mental health datasets to deliver empathetic and contextually appropriate responses.
- **Classic Games Suite:** Includes Tic-Tac-Toe, Memory Matching, Hangman, Snake, and Tetris, implemented with engaging graphics and smooth gameplay.
- **Intuitive GUI:** Built with PyQt5 to ensure a seamless and user-friendly interface.
- **Enhanced User Engagement:** Incorporates background music and animations to create an immersive experience.
- **Customizable Settings:** Offers adjustable music volume and other preferences to tailor the experience to individual needs.

## Frameworks and Technologies Used

- **Python 3.12**
- **PyQt5:** For building the graphical user interface (GUI).
- **PyTorch:** For model training and inference.
- **Hugging Face Transformers:** For leveraging pre-trained models and tokenizers.
- **Pandas and NumPy:** For data manipulation and preprocessing.
- **Scikit-learn:** For data splitting and preprocessing.
- **QtMultimedia:** For handling multimedia content like background music.

## Detailed Implementation

### UI Implementation

The user interface is implemented using **PyQt5**, a comprehensive set of Python bindings for Qt application development. The application's UI consists of multiple windows and components, each encapsulated in its own module for modularity and clarity.

- **Base Window (`ui/base_window.py`):** A foundational class `BaseWindow` that other UI windows inherit from. It sets up the basic window properties, such as size, style, and layout.

- **Start Window (`ui/start_window.py`):** The entry point of the application. It displays a background animation (`background.gif`) and provides navigation buttons to the chat interface, game menu, and settings.

- **Chat Interface (`ui/chat_interface.py`):** Implements the chat window where users interact with the AI assistant. It uses `QTextEdit` for displaying conversation history and `QLineEdit` for user input. The class `ChatInterface` handles message sending and receiving, and includes typing animations for a more interactive experience.

- **Game Menu (`ui/game_menu_window.py`):** Presents the list of available games. Each game can be launched from this menu.

- **Settings Window (`ui/settings_window.py`):** Allows users to adjust settings such as background music volume.

- **Game Windows (`games/*.py`):** Each game is implemented in its own module:

  - **Hangman (`games/hangman.py`):** Classic word-guessing game with a PyQt5 interface.
  - **Memory Matching Game (`games/memory_game.py`):** A card-matching game that challenges memory.
  - **Snake Game (`games/snake_game.py`):** The traditional snake game, implemented with custom drawing using `QPainter`.
  - **Tic-Tac-Toe (`games/tic_tac_toe.py`):** A simple implementation where the player competes against a basic AI.
  - **Tetris (`games/tetris_game.py`):** The block-stacking game, featuring piece movement and rotation.

- **Game Base Class (`games/game.py`):** Provides a base class `GameWindow` that game windows inherit from, encapsulating common functionality like centering the window and handling the back button.

### Program Loop

The application leverages the event-driven programming model of PyQt5. The main program loop is managed by PyQt5's `QApplication`, which listens for events such as button clicks, text input, and timer expirations.

- **Event Handling:** User interactions trigger signals (events) that are connected to slots (handler functions). For instance, clicking the "Send" button in the chat interface calls the `start_typing_user_message` method.

- **Timers:** Games like Snake and Tetris use `QTimer` to create game loops that update the game state at regular intervals.

  - **Snake Game (`games/snake_game.py`):** Uses `QTimer` to move the snake and refresh the game area, mimicking a traditional game loop.
  - **Tetris Game (`games/tetris_game.py`):** Utilizes `QBasicTimer` for dropping pieces over time.

### AI Training

The AI chatbot is trained using **PyTorch** and the **Hugging Face Transformers** library. The training process is defined in `model_train.py` and involves several key steps:

1. **Data Loading and Preprocessing:**

   - **Datasets Used:**
     - **Mental Health FAQ Dataset (`Mental_Health_FAQ.csv`):** Frequently asked questions and answers on mental health topics.
     - **Empathetic Dialogues Dataset:** Over 24,000 conversations grounded in emotional contexts.
     - **Mental Health Chatbot Dataset:** Contains human-assistant dialogues focused on mental health.
     - **MentalLLaMA Dataset:** Local dataset comprising instruction and complete data.

   - **Data Cleaning:** Removal of HTML tags, normalization of text, and structuring into question-response pairs.

   - **Data Augmentation:** Politeness templates are applied to assistant responses to enhance empathy and engagement.

2. **Model Selection and Tokenization:**

   - **Pre-trained Model:** Utilizes `microsoft/DialoGPT-medium` as the base model.
   - **Tokenizer:** `AutoTokenizer` from Hugging Face, with special tokens added for start and end of text.

3. **Training Configuration:**

   - **Training Arguments:** Defined using `TrainingArguments` from Hugging Face, specifying parameters like learning rate, batch size, and number of epochs.
   - **Trainer Initialization:** Uses the `Trainer` class to handle the training loop, evaluation, and saving of checkpoints.

4. **Model Training:**

   - **Data Collation:** Custom collator function ensures inputs and labels are correctly formatted.
   - **Training Loop:** The model is fine-tuned on the preprocessed data, optimizing to generate appropriate responses.

5. **Model Saving:**

   - **Output Directory:** The trained model and tokenizer are saved to `./trained_polite_model`.

### Model Usage

The trained model is utilized in `chatbot_model.py`:

- **Model Loading:**

  - **Model and Tokenizer:** Loaded from the saved directory `trained_polite_model`.
  - **Device Configuration:** The model is moved to GPU if available for faster inference.

- **Response Generation:**

  - **Function `generate_response(question, max_length=150)`:** Accepts a user question and generates a response.
  - **Context Handling:** Maintains recent inputs to provide context in the conversation.
  - **Text Encoding:** The input is tokenized and converted into input IDs for the model.
  - **Model Inference:** Generates a response using the model's `generate` method with parameters like `top_p`, `top_k`, and `temperature` to control randomness.
  - **Response Decoding:** The generated tokens are decoded back into text, and the assistant's response is extracted.

### Data Sources and Manipulation

Detailed in `model_train.py`, data manipulation involves:

- **Data Cleaning Functions:**

  - **`remove_html_tags(text)`:** Removes HTML tags using regular expressions.
  - **`split_human_assistant(text)`:** Extracts human and assistant parts from combined text fields.

- **Data Structuring:**

  - **Question-Response Pairing:** Ensures all data conforms to a consistent format.
  - **Politeness Augmentation:**

    - **Templates:** A set of polite phrases is defined.
    - **Function `add_random_politeness(row)`:** Randomly adds polite starters and enders to assistant responses.

- **Data Integration:**

  - **Concatenation:** Combines all datasets into a unified DataFrame.
  - **Deduplication and Normalization:** Removes duplicates and normalizes text to enhance data quality.

### Feature Vector Design

- **Tokenization:** Text data is converted into numerical format using the tokenizer. Special tokens (`<|startoftext|>`, `<|endoftext|>`) are added to denote the start and end of sequences.

- **Input IDs and Attention Masks:** The tokenizer outputs input IDs and attention masks, which are used by the model to process the input text.

- **Padding and Truncation:** Ensures all input sequences are of uniform length for batch processing.

## Code Structure

The project is organized into several modules, each responsible for different aspects of the application.

### AI Model Training (`model_train.py`)

- **Data Loading:** Uses functions like `load_dataset` and Pandas `read_csv` to import datasets.

- **Data Preprocessing Functions:**

  - **`remove_html_tags(text)`:** Cleans text data.
  - **`create_question_response_pairs(df)`:** Structures the empathetic dialogues dataset.
  - **`add_random_politeness(row)`:** Augments responses.

- **Model Training:**

  - **Tokenizer and Model Initialization:** Sets up the tokenizer and model with special tokens.
  - **Training Arguments:** Configured using `TrainingArguments`.
  - **Trainer Setup:** Initialized with model, data, and training arguments.
  - **Training Execution:** `trainer.train()` runs the training loop.
  - **Model Saving:** The trained model is saved for later use.

### Chatbot Model (`chatbot_model.py`)

- **Model Loading:**

  - **`model` and `tokenizer`:** Loaded from the saved directory.
  - **Device Configuration:** Ensures compatibility with available hardware.

- **Response Generation Function:**

  - **`generate_response(question, max_length=150)`:** Generates responses to user input.
  - **Context Management:** Keeps track of recent user inputs for contextual responses.

### User Interface

#### Base Window (`ui/base_window.py`)

- **`BaseWindow` Class:** A reusable window class that sets up common UI elements like the back button and header.

#### Start Window (`ui/start_window.py`)

- **Background Animation:** Uses `QMovie` to display a GIF animation.
- **Navigation Buttons:** Provides access to the chat interface, game menu, and settings.

#### Chat Interface (`ui/chat_interface.py`)

- **Chat Display:** Uses `QTextEdit` to show the conversation history.
- **User Input:** `QLineEdit` for typing messages.
- **Typing Animation:** Simulates typing effects using `QTimer`.

#### Game Menu (`ui/game_menu_window.py`)

- **Game Selection:** Lists available games with buttons to launch them.

### Games

Each game is contained within its own module in the `games` directory and inherits from `GameWindow`.

- **Common Game Features:**

  - **Pause Functionality:** Allows pausing and resuming the game.
  - **Back Button:** Returns to the game menu.
  - **Game Logic:** Implemented within each game's class.

- **Specific Games:**

  - **Hangman (`games/hangman.py`):** Word guessing with hints.
  - **Memory Matching (`games/memory_game.py`):** Card matching with difficulty levels.
  - **Snake (`games/snake_game.py`):** Classic snake gameplay with adjustable speed.
  - **Tic-Tac-Toe (`games/tic_tac_toe.py`):** Player vs. computer with basic AI.
  - **Tetris (`games/tetris_game.py`):** Falling blocks game with piece rotation.

## Installation

### Prerequisites

+ Anaconda: Recommended for managing Python environments.
+ Python: Version 3.7 or higher.

### Steps
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

2. **Empathetic Dialogues Dataset**

   - **Source**: Hugging Face's [EmpatheticDialogues](https://huggingface.co/datasets/empathetic_dialogues).
   - **Description**: Consists of over 24,000 one-on-one conversations grounded in emotional contexts.
   - **Processing**: Structured into question-response pairs to maintain conversational coherence.

3. **Mental Health Chatbot Dataset**

   - **Source**: Hugging Face datasets (`heliosbrahma/mental_health_chatbot_dataset`).
   - **Processing**: Parsed combined texts to extract human and assistant dialogues using custom regular expressions.

4. **MentalLLaMA Dataset**

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



By meticulously manipulating the data, the model was primed to deliver high-quality, empathetic responses, adhering to expert standards in natural language processing.










