# kids-clothes
A project to try and quantify the differences in animals on boys' and girls' clothes.

### Introduction

What animals do you associate with boys' clothes? Or girls' clothes? Strangely you don't have to think too long or hard to find examples for each. Cats? Well, that's a girl animal isn't it? Dinosaurs? Those are for little boys.

This project doesn't answer why that's the case. Instead it attempts to put some numbers to it.

I've been surprised in the past by how strong confirmation bias can be for things that you think are intuitively true. Like, does Radio X really play the Stone Roses all the time? It turns out, no not really (a previous half-done project of mine). So is it really true that you only ever find certain animals on boys' or girls' clothes? Can we measure just how big the divide is, if there is one at all?

Just a disclaimer from the outset: I don't think there even should be girls' clothes or boys' clothes; there should just be kids' clothes.

### Methods

I wrote a Python script to scrape the websites of some of the top retailers of kids' clothes in the UK. I'm using [Selenium](http://selenium-python.readthedocs.io/) to do this, storing the results in a MongoDB database for no reason other than I find using MongoDB really satisfying. It also means that querying the dataset is slightly more convenient than interrogating a giant Python dictionary.

The retailers under investigation are:

- [Asda (George)](https://direct.asda.com/george/kids/D25,default,sc.html)
- [Tesco](https://www.tesco.com/direct/clothing-accessories/baby-kids-clothing-shoes/cat3376645.cat)
- [Matalan](https://www.matalan.co.uk/kids-clothing)
- [Sainsburys (Tu)](https://tuclothing.sainsburys.co.uk/c/kids/kids)
- [Debenhams](http://www.debenhams.com/kids)
- [Next](http://www.next.co.uk/children)
- [Marks and Spencer](http://www.marksandspencer.com/c/kids)
- [Mamas and Papas](https://www.mamasandpapas.com/en-gb/c/clothing/)
- [Boots](http://www.boots.com/baby-child/kids-clothes-mini-club)
- [boohoo](http://www.boohoo.com/kids)
- [Peacocks](https://www.peacocks.co.uk/kidswear)
- [Primark](https://www.primark.com/en/products/new-arrivals/kids)

These were chosen according to picking the top results on a Google search for "UK+kids+clothes". I think they represent a pretty mainstream selection of where I might go to get clothes for my kids.

Each of these sites presents their items slightly differently, so each store has their own function to look for the relevant HTML tags using [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) and to use Selenium to scroll down the page if there are items loaded dynamically. I then have a MongoDB database with a collection of every animal I could think of which might be on kids clothes. Even weird ones like camels and swans. Most of the animals have a list of aliases so I don't miss things like 'piggy', 'piglet', 'pigs' etc. for 'pig'. Just to test out a couple of theories that may be total nonsense, I've also assigned each animal a weight (a *really* broad average of male/female weights from Wikipedia) and their diet (herbivore, carnivore, omnivore). My guess is that the 'boy' animals tend to be big and eat meat.

The script goes through each of the HTML tags where the clothing item's name is stored and cross matches each string with the animals and their aliases in the database. If it finds a match it increments a total count for that animal, as well as an individual count for that retailer in the document. The total code takes a while to run because it's got loads of URLs to investigate as well as simulating the browser doing loads of human-speed scrolling.

#### Limitations:

- The list of animals isn't complete and almost certainly misses some variants on animal names
- The study assumes that the animal name is in the item title - which is not always true
- The study was performed near Christmas, skewing the results to include penguins etc. I suppose ideally this would be done during an animal-agnostic time of year (i.e. not Halloween, Christmas, Easter etc.)

### Usage

Install packages with:

```
pip install -r requirements.txt
```

Make sure MongoDB is running locally, then run:

```
python src/create_db.py
python src/scrape_pages.py
```

The process takes around 10-15 mins to run completely. You can produce some of the results using:

```
python analyse_results.py
```

### Results

Total number of boys clothes found = 654
Total number of girls clothes found = 1169

The top 5 animals for boys were:

| Animal        | Number (% of total boys' items)           | Equivalent girls' number (% of total girls' items)  |
| ------------- |:-------------| :-----|
|Dinosaur |195 (32.83 %)	| 17 (2.00 %)|
|Pig | 47 (7.91 %)	           |58 (6.82 %)|
|Shark | 46 (7.74 %)		 |0 (0.0 %)|
|Bear | 43 (7.24 %)		 | 35 (4.12 %)|
|Mouse | 23 (3.87 %) 	 | 51 (6.00 %)|

The top 5 animals for girls were:

| Animal        | Number (% of total girls' items)           | Equivalent boys' number (% of total boys' items)  |
| ------------- |:-------------| :-----|
|Unicorn | 226 (26.59 %)	 | 2 (0.34 %)|
|Rabbit | 119 (14.00 %)	 | 5 (0.84 %)|
|Cat | 103 (12.12 %)	 |3 (0.51 %)|
|Horse | 75 (8.82 %)		|1 (0.17 %)|
|Pig | 58 (6.82 %)	 	|47 (7.91 %)|
