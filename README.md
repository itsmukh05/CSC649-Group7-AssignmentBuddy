# Assignment Buddy
## Building a Domain-Specific Chatbot Using a Custom Dataset and a Large Language Model (LLM)

---

## 1. Project Title

**Assignment Buddy: An AI-Powered Academic Assignment Assistant**

Assignment Buddy is a domain-specific chatbot developed for the CSC649 group assignment. It uses a custom academic Question-and-Answer (Q&A) dataset and a Large Language Model (LLM) to provide university students with helpful guidance on academic assignments.

## 2. Project Domain

**Domain: Education – Academic Assignment Assistance**

Assignment Buddy focuses on supporting university students in understanding and completing academic assignments.

The chatbot covers the following areas:

- Academic writing and assignment structure.
- Introduction and conclusion writing.
- Research skills and information gathering.
- Critical thinking and analysis.
- Academic referencing (APA, Harvard and IEEE).
- Paraphrasing and plagiarism awareness.
- Group assignment management.
- Time management and study strategies.
- Responsible use of Artificial Intelligence in education.

The purpose is to provide students with accessible academic guidance while encouraging independent learning and academic integrity.

## 3. Team Members

This project is developed collaboratively by four CSC649 group members.

| No. | Name | GitHub Username | Role |
|---|---|---|---|
| 1 | MOHAMAD IMRAN BIN MOHAMAD ASTURA | GitHub Username | Project Leader & System Integration |
| 2 | MUHAMMAD AMMAR MUKHRIZ BIN BASRUL HISHAM | itsmukh05 | Dataset Development & Research |
| 3 | MUHAMMAD FARHAN DANISH BIN MOHD FAIZAL | GitHub Username | AI Model & Backend Development |
| 4 | Member 4 Name | GitHub Username | Frontend, Testing & Documentation |

All members are expected to contribute to technical development, testing, documentation and GitHub collaboration.

## 4. How to Run the Project

### 4.1 Prerequisites

Before running Assignment Buddy, ensure that the following are installed:

- Python 3.10 or later.
- Visual Studio Code or another Python IDE.
- Git.
- A Google Gemini API key.

### 4.2 Clone the Repository

Open a terminal and run:

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

Navigate to the project directory:

```bash
cd Assignment-Buddy
```

### 4.3 Install Dependencies

Install the required Python packages:

```bash
pip install -r requirements.txt
```

The project dependencies include:

```text
streamlit
google-genai
python-dotenv
```

### 4.4 Configure the API Key

Create a `.env` file in the root project directory.

Add the following configuration:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

Replace the placeholder with a valid Google Gemini API key.

**Important:** Never upload the `.env` file or actual API key to GitHub. The `.env` file must be included in `.gitignore`.

### 4.5 Run the Application

Start the Streamlit application:

```bash
python -m streamlit run app/app.py
```

Open a web browser and navigate to:

```text
http://localhost:8501
```

Assignment Buddy will be available through the local web interface.

## 5. System Architecture

Assignment Buddy follows a dataset-assisted LLM architecture.

The system combines custom dataset retrieval with Gemini to generate academic assistance responses.

### 5.1 Architecture Diagram

```text
+-----------------------------+
|       University Student    |
+-----------------------------+
              |
              v
+-----------------------------+
|     Streamlit Frontend      |
|       (User Interface)      |
+-----------------------------+
              |
              v
+-----------------------------+
|       User Question         |
+-----------------------------+
              |
              v
+-----------------------------+
|      Dataset Retrieval      |
|   (CSV Question Matching)   |
+-----------------------------+
              |
              v
+-----------------------------+
|   Relevant Dataset Answers  |
+-----------------------------+
              |
              v
+-----------------------------+
|       Google Gemini API     |
|     (LLM Response)          |
+-----------------------------+
              |
              v
+-----------------------------+
|     Generated Response      |
+-----------------------------+
              |
              v
+-----------------------------+
|      Student Interface      |
+-----------------------------+
```

### 5.2 System Workflow

1. The student enters a question through the Streamlit interface.
2. The system searches the custom CSV dataset for relevant questions and answers.
3. The most relevant dataset information is retrieved.
4. The retrieved information and student's question are provided to Google Gemini.
5. Gemini generates a natural-language response using the supplied context.
6. The response is displayed to the student through the chatbot interface.

## 6. Dataset Description

### 6.1 Dataset Overview

The project uses a custom dataset containing at least 30 Question-and-Answer pairs related to university academic assignments.

**Dataset filename:** `assignment_buddy_dataset.csv`

**Dataset format:** CSV (Comma-Separated Values)

**Dataset location:** `data/`

**Dataset columns:**

| Column | Description |
|---|---|
| Question | Academic-related question entered by a student |
| Answer | Suggested answer or guidance for the question |

### 6.2 Dataset Categories

The dataset covers several academic topics:

| Category | Example Topic |
|---|---|
| Assignment Writing | How to structure an assignment |
| Academic Writing | Writing introductions and conclusions |
| Research Skills | Finding and evaluating information |
| Critical Thinking | Analysing arguments and evidence |
| Referencing | APA, Harvard and IEEE citation styles |
| Academic Integrity | Plagiarism and paraphrasing |
| Group Work | Managing group assignments |
| Time Management | Planning assignment deadlines |
| AI in Education | Responsible use of AI tools |

### 6.3 Dataset Example

| Question | Answer |
|---|---|
| How do I write an introduction? | Introduce the topic, provide background information and explain the purpose of the assignment. |
| What is plagiarism? | Plagiarism is presenting another person's work or ideas as your own without proper acknowledgement. |
| What is critical thinking? | Critical thinking involves analysing information, evaluating evidence and developing logical conclusions. |

The dataset is stored locally and used as the chatbot's knowledge source during question retrieval.

## 7. Model Details

### 7.1 Large Language Model

Assignment Buddy uses Google's Gemini API to access a Large Language Model.

| Component | Details |
|---|---|
| AI Provider | Google |
| Model Family | Gemini |
| Model Name | [Insert the exact Gemini model ID used in the code] |
| API Integration | Google Gen AI SDK (`google-genai`) |
| Programming Language | Python |
| Application Framework | Streamlit |

The exact model ID should be confirmed from the `model` parameter in the final source code.

### 7.2 Model Functionality

The Gemini model is responsible for:

- Understanding students' questions.
- Processing relevant information retrieved from the custom dataset.
- Generating natural-language answers.
- Explaining academic concepts in simple language.
- Providing context-aware academic guidance.

### 7.3 Dataset and LLM Integration

The custom dataset provides domain-specific information, while Gemini uses its language-generation capabilities to produce understandable responses.

This approach helps make the chatbot more relevant to academic assignment assistance than relying on a general-purpose LLM without domain-specific context.

## 8. Limitations

Although Assignment Buddy provides academic assistance, it has several limitations:

1. **Dataset Dependency:** The quality of retrieved information depends on the accuracy and coverage of the custom dataset.
2. **AI-generated Errors:** Gemini may occasionally generate inaccurate or misleading information.
3. **API Dependency:** The chatbot requires an internet connection and access to the Gemini API.
4. **API Usage Limits:** API availability and usage are subject to Google's applicable rate limits and pricing policies.
5. **Limited Domain Coverage:** The chatbot primarily focuses on academic assignments and may not provide reliable answers outside this domain.
6. **Referencing Accuracy:** Students should independently verify citations and referencing details.
7. **Retrieval Limitations:** The dataset matching method may fail to identify the most relevant entry for some differently worded questions.

Future improvements may include semantic search, larger datasets, improved retrieval methods and more comprehensive response evaluation.

## 9. Generative AI (GenAI) Usage

Generative AI tools are used in the development of Assignment Buddy as part of the project's development process.

### 9.1 Purpose of GenAI Usage

GenAI tools assist the development team with:

- Brainstorming chatbot features and project ideas.
- Generating and refining sample academic Q&A content.
- Supporting Python programming and debugging.
- Assisting with Gemini API integration.
- Improving documentation and project explanations.
- Suggesting testing scenarios and improvements.

### 9.2 Human Contribution

All AI-assisted outputs are reviewed, checked and modified by the group members.

The group is responsible for:

- Verifying dataset accuracy and relevance.
- Reviewing generated code before implementation.
- Testing chatbot functionality.
- Evaluating AI-generated responses.
- Making final project decisions.

### 9.3 Responsible AI Use

The group aims to use Generative AI responsibly and transparently.

AI-generated information is treated as supporting material rather than automatically accepted as fact. The project also encourages students to use Assignment Buddy as a learning assistant rather than a replacement for independent academic work.

The team's use of GenAI will be documented in accordance with the CSC649 assignment requirements and the required GenAI declaration.

## 10. Project Folder Structure

```text
Assignment-Buddy/
│
├── README.md
├── requirements.txt
├── .gitignore
├── .env.example
│
├── data/
│   └── assignment_buddy_dataset.csv
│
├── app/
│   └── app.py
│
├── src/
│   └── chatbot.py
│
├── tests/
│   └── test_chatbot.py
│
└── docs/
    └── project_documentation.md
```

## 11. Project Information

| Item | Details |
|---|---|
| Course Code | CSC649 |
| Project Name | Assignment Buddy |
| Project Type | Domain-Specific AI Chatbot |
| Domain | Education – Academic Assignment Assistance |
| Programming Language | Python |
| Frontend Framework | Streamlit |
| LLM Provider | Google Gemini |
| Dataset Format | CSV |
| Version Control | GitHub |

---

**Assignment Buddy – Supporting Students Through AI-Powered Academic Guidance.**

Developed as part of the CSC649 Group Assignment.
