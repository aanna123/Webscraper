# Webscraper
This project automates the extraction of real estate project details from the Odisha RERA website using Selenium WebDriver in Python. It navigates through the list of registered projects, accesses their detailed pages, extracts information like project name, registration number, promoter details,

# 🏗 Odisha RERA Project Scraper

This Python script scrapes registered real estate project details from the [Odisha RERA portal](https://rera.odisha.gov.in/projects/project-list) using Selenium and saves the results into a CSV file.

## 📌 Features

- Navigates through each project listing
- Extracts:
  - RERA Registration Number
  - Project Name
  - Promoter Name
  - Promoter Address
  - Promoter GST Number
- Handles tabbed interfaces and popups
- Stores results in `rera_projects.csv`

## 🧰 Requirements

- Python 3.7+
- Google Chrome installed
- ChromeDriver (matching your browser version)

## 📦 Install Dependencies

```bash
pip install selenium

