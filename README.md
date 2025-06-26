# 🧠 Automatic Tool for Article Screening (PRISMA 2020)

![Build Status](https://github.com/ton_nom_dutilisateur/ton_projet/actions/workflows/main.yml/badge.svg)
![Python](https://img.shields.io/badge/python-3.10-blue)
![License](https://img.shields.io/github/license/ton_nom_dutilisateur/ton_projet)
![Coverage](https://img.shields.io/codecov/c/github/ton_nom_dutilisateur/ton_projet)

**Tired of reading hundreds of irrelevant articles for your thesis?**  
This AI-powered tool analyzes article abstracts and selects only the most relevant ones — helping you save time and focus on quality research.

---

## 🚀 Features

- Uses a powerful LLM (Mistral) to analyze abstracts
- Supports `.bib` and `.csv` files from major databases (IEEE, ACM, etc.)
- Automatically generates PRISMA-like structured outputs
- Customizable prompts for targeted selection

---

## ⚙️ Setup

First, install the required Python libraries:

```bash
pip install mistralai
pip install bibtexparser
```

Then, ensure the following files are located in the same directory:

- The 6 Python scripts:
  - `make_prisma_diagram.py` – Main entry point
  - `article.py`, `manage_articles.py`
  - `bib_to_json.py`, `csv_to_json.py`, `ask_to_mistral.py`
- A `prompt.txt` file describing your research topic
- An `API_key.txt` file containing your Mistral API key

---

## 📖 User Guide

This tool is designed for researchers conducting systematic reviews, especially those following the [PRISMA 2020 guidelines](https://www.prisma-statement.org/prisma-2020). However, it can also be used for any article selection task requiring automated screening.

> **Note:** Output file names follow the PRISMA 2020 diagram structure, as the tool is tailored for that methodology.

### 🔍 Before You Start

1. **Prepare your data:**  
   Download your article search results from academic databases (IEEE, ACM, etc.) in `.bib` and/or `.csv` formats.

2. **API Key:**  
   To use Mistral, you need an API key saved in the file `API_key.txt`.  
   You can rename this file using the [`--api`](#parameters) parameter.

   ➤ Get your API key from [Mistral’s documentation](https://docs.mistral.ai/getting-started/quickstart/).

   > ⚠️ A sample API key is already provided in `API_key.txt`. Try using it, but if it doesn’t work, please create your own.

3. **Prompt file:**  
   The `prompt.txt` file is essential. It must clearly describe:
   - Your research domain
   - The kind of articles you're looking for  

   This is the first instruction the LLM will use, so be as precise as possible.  
   You’ll find an example prompt in the repository. See [Mistral's prompting guide](https://docs.mistral.ai/guides/prompting_capabilities/) for more help.

---

### ▶️ Execution

Assuming your article files are `file1.csv` and `file2.bib`, run:

```bash
python3 make_prisma_diagram.py --input file1.csv file2.bib --api API_key.txt --prompt prompt.txt --min_pages 5 --save_dir ./results
```

---

### ⚙️ Parameters <a name="parameters"> </a>

- `--input file1 ... filen` : Input files to analyze (`.csv` or `.bib` only).  
  **⚠️** Other extensions will raise an error.

- `--save_dir dir_name` *(optional)* : Directory to store results.  
  *Default*: `.`

- `--min_pages m` *(optional)* : Minimum number of pages required for an article to be considered.  
  *Default*: `0`

- `--api api_addr` *(optional)* : Path to the file containing the Mistral API key.  
  *Default*: `API_key.txt`

- `--prompt prompt_addr` *(optional)* : Path to the file containing the prompt.  
  *Default*: `prompt.txt`

The program will create a dated folder inside `save_dir` containing all outputs.

---

## 📦 Output Files

- `file1.json`, ..., `filen.json` : Converted input files, listing all articles in JSON format.
- `duplicates_k.json` : Duplicate articles detected across input files.  
- `not_enough_pages_k.json` : Articles removed due to insufficient page count.
- `ineligible_by_mistral_k.json` : Articles deemed irrelevant by the LLM.
- `records_screened_k.json` : Final selection — the articles matching your prompt.

> ℹ️ *In all file names, `k` refers to the number of articles in the file.*
