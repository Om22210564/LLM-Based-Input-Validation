# LLM-Based User Profile Validator

This project uses a **Language Model (LLM)** to validate user profile JSON objects against real-world standards. It ensures fields like `name`, `email`, `age`, `country`, and `phone` are correctly formatted and provides warnings for soft validation issues.

The evaluation is automated using [Promptfoo](https://promptfoo.dev/), allowing deterministic test cases and assertions on LLM outputs.

---

## Features

- **Strict Validation:** Checks mandatory fields for correctness.  
- **Warnings:** Flags soft issues like unusually young age, short names, or disposable emails.  
- **JSON Output Contract:** Returns only valid JSON with `is_valid`, `errors`, and `warnings`.  
- **Python Script Support:** Run validation from `main.py`.  
- **Automated Testing:** Run test cases with Promptfoo.  

---

## Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd LLM-Based_Input_Validator
   ```
   
2. **Install Python dependencies**
   ```bash
   python -m venv venv          # optional but recommended
   source venv/bin/activate     # Linux/macOS
   venv\Scripts\activate        # Windows
   pip install -r requirements.txt
   ```

3. **Install Promptfoo globally**
   ```bash
   npm install -g promptfoo
   ```

4. **Set your GROQ API key using a `.env` file**
   ```bash
   GROQ_API_KEY="your_api_key_here"     
   ```
   

## How to Run the Python Script

The main.py script validates a JSON file and outputs the LLM-validated result.
```bash
python main.py input2.json
```
This command will evaluate all test cases defined in the tests section of promptfooconfig.yaml.

Example JSON input (input2.json):
```json
{
  "name": "Aarav Patel",
  "email": "aarav.patel@gmail.com",
  "age": 24,
  "country": "IN",
  "phone": "+919876543210"
}
```

Expected output:
```json
{
  "is_valid": true,
  "errors": [],
  "warnings": []
}
```

## How to Run Promptfoo Evals

Promptfoo evaluates the prompts against the test cases defined in promptfooconfig.yaml

Run all evals
```bash
npx promptfoo eval
```

View results
```bash
npx promptfoo view
```


## References

- [**Promptfoo Documentation**](https://www.promptfoo.dev/docs/intro/)
- [**Groq API Documentation**](https://console.groq.com/docs/overview).


This project is designed to be robust, deterministic, and easy to use, making it suitable for validating user data in real-world applications and automated testing pipelines.
