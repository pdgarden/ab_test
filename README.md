# README

## Description

Web interface based on Streamlit used to estimate variability of AB test on binary outcome, leveraging bayesian statistics.

## Usage

### Installation


1. Install uv (v0.6.6):
   1. For macOS / Linux `curl -LsSf https://astral.sh/uv/0.6.6/install.sh | sh`
   2. For windows: `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/0.6.6/install.ps1 | iex"`
2. Create virtual environment: `uv sync`
3. To develop (Optional):
   1. Setup pre-commit: `uv run pre-commit install -t commit-msg -t pre-commit`


```shell
pip install -r requirements.txt
```

### Run

```shell
streamlit run app_ab_test.py.py
```


