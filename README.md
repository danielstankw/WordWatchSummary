## Goals
Create an application to automatically scrape links containing articles with specified key-phrases. Save the urls + content. 
Use LLM to sumamrize (100-150) the content of the article and define the sentiment (positive, negative, critical etc - prompt). Aggregate the results in read friendly format, embed it in the email and send it to the user.

## Task List
- [ ] Cronjob (last part)
- [ ] SMTP email sender (locally)
- [x] LLM url content summarizer (locally - or non locall but FREE)
- [x] Prompt chaining + prompt engineering
- [x] Google Search URL generator + save: `main.py`
- [x] Extract content of the URLs and save them: `link_scrape.py`