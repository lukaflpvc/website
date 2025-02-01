---
authors:
    - luka
categories:
    - Data Analysis
    - Startups
comments: true
date:
    created: 2024-10-12
    updated: 2024-11-02
description: Explore the data behind Y Combinator's startup directory and the important
    trends affecting the startup industry.
draft: false
tags:
    - Open Source
    - Projects
---

# Analysing Every Y Combinator Batch Ever

<p align="center">
<img src="https://github.com/lukafilipxvic/YC-Vault/blob/main/images/YC-Vault.png?raw=true", width="80%">
</p>

!!! abstract "**TL:DR**"
    Y Combinator (YC) is betting on more founders than ever. New YC startups are showing signs of efficiency, requiring smaller teams to run.
    [Source Code](https://github.com/lukafilipxvic/YC-Vault 'YC Analyzed Source Code')


## Why Scrape YC?
Y Combinator's [company directory](https://www.ycombinator.com/companies 'YC Company Directory') is a gold mine of data.

With over 4,933 startups and counting, there is an opportunity to uncover valuable insights and trends. The growing list of companies allows us to extract crucial patterns into technical-founder-driven venture capital (VC). 

Each company has a unique story.

But they all have a beginning, involving the initial plot, characters, and conflict. For YC startups, it's where purpose-driven founders receive the resources and mentorship to rapidly solve customer problems.

Then comes the journey.

Founders venture into the unknown, not knowing the road ahead. No one knows how it will end. And yet, with the uncertainty, all stories end in one of three ways: Acquired, Active or Inactive. 

The YC Directory holds the story of every startup they have ever funded. Each has a unique set of moments, creating one of the most beautiful movements of purpose-driven technical founders.

That's why I want to find out how these stories are shaping over time.

## The Method
The idea for this project came from (YC W24) Gumloop's [Scrape YC Directory example](https://www.gumloop.com/templates/web_scraping/scrape_yc_directory). I tried to run it, but the process felt too inefficient given the excessive number of tokens required to run for a small YC batch.

Using Python only, I wanted to extract the information of every startup in YC's public directory.  

### Python Stack
The following Python packages made this possible:

* Language Model - Useful for data extraction. GPT-4o mini works best.
* Selenium - Web driver for extracting raw text body and links.
* Instructor/Pydantic - Structured outputs powered by language models.

### Scraping Tactic
1. For each YC batch, load the whole company directory by scrolling to the page end. Extract all Company YC URLs to a CSV file *YC_URLs.csv*. Exclude irrelevant URLs.

2. For each YC company URL, scrape the page content and links

3. Using Instructor and Pydantic, parse the data into the defined pydantic ```Founders``` and ```YC_Company``` model.

3. Save the scraped data to a CSV file *YC_Directory.csv*.

### The Collected Data
As a start, I gathered every YC company's high-level information...

* Name
* YC Batch
* Status
* Team Size
* URL

...and use it to discover secrets behind technical-founder-driven VC.

I can easily expand this to cover founder count, HQ location, industry and so on. But that's for the future.

## The Results
The dataset contains [4,933 companies](#the-results 'as of October 12 2024') broken down into four status categories:

* **Active**: 3,537  companies (71.7%)
* **Inactive**: 815 companies (16.5%)
* **Acquired**: 564 companies (11.4%)
* **Public**: 17 companies (0.3%)

!!! info "An observation..."
    Peter Thiel was right. Over a long period of time, startups follow a *Power Law distribution*. VC is all about making a lot of small bets. But how can founders do the same thing for themselves?

### YC Batch Size Trend
<p align="center">
<img src="https://github.com/lukafilipxvic/YC-Vault/blob/main/images/1%20batch-size-over-time.png?raw=true">
</p>
The increasing batch size shows that YC is succeeding in achieving its mission: helping startups grow.

2021 was the largest cohort with 728 companies in Batches W21 and S21.
But YC then limited batch sizes to around 250 companies. This could be the optimal size for startup accelerators.

### Survival Rate by Batch
<p align="center">
<img src="https://github.com/lukafilipxvic/YC-Vault/blob/main/images/2%20survival-rate-over-time.png?raw=true">
</p>
The survival rate over time shows the natural attrition in the startup ecosystem, where only the most viable companies persist over time.

This can be called the *Law of Company Progression.*

### Total Team Size by Batch
<p align="center">
<img src="https://github.com/lukafilipxvic/YC-Vault/blob/main/images/3%20total-team-size-by-batch.png?raw=true">
</p>
Despite YC funding more startups than ever, total batch team size has plateaued, indicating a trend towards leaner, more efficient technical-driven startups. This is obvious from Batch S22. Future datasets should monitor this trend closely.

### Team Size Percentage by Status
<p align="center">
<img src="https://github.com/lukafilipxvic/YC-Vault/blob/main/images/4%20team-size-%25-by-status.png?raw=true">
</p>
Publicly listed YC companies take the majority of team size by batch.
Inactive startups tend to die small. This could suggest that startups that stay small, die small. 

## Future Work
I believe this data is only scraping the surface of YC's company directory. Looking at this data over time will allow us to view the progression of batches naturally.

The project is [open-source](https://github.com/lukafilipxvic/YC-Vault 'YC Analyzed Source Code'), so please feel free to make changes to the directory.
