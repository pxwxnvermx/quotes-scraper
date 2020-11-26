# Quotes Scraper

A python script to get quotes from goodreads author quotes page url. Outputs json to a txt file called demo.txt.

```
https://www.goodreads.com/author/quotes/21559.Nassim_Nicholas_Taleb
```
### Prerequisites

Run the following command to install dependencies

```
python -m pip install -r requirements.txt
```

### Running the script

```
git clone https://github.com/PawanVerma1337/quotes-scraper.git
cd quotes-scraper
./quote.py [url] --output [filename]
```

### TODO
[x] Command line arguments and help.
[x] Output to file.\
[x] Made the script faster with lxml and multithreading
[ ] Fetch with author name.
[ ] Save previous author.
[ ] Save previous author quotes to file.

