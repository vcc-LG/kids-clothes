# kids-clothes
A project to try and quantify the differences in animals on boys' and girls' clothes.

### Introduction

What animals do you associate with boys' clothes? Or girls' clothes? Strangely you don't have to think too long or hard to find examples for each. Cats? Well, that's a girl animal isn't it? Dinosaurs? Those are for little boys.

This project doesn't answer why that's the case. Instead it attempts to put some numbers to the problem.

I've been surprised in the past by how strong confirmation bias can be for things that you think are intuitively true. Like, does Radio X really play the Stone Roses all the time? It turns out, no not really (a previous half-done project of mine). So is it really true that you only ever find certain animals on boys' or girls' clothes? Can we measure just how big the divide is, if there is one at all?

Just a disclaimer from the outset: I don't think there even should be girls' clothes or boys' clothes; there should just be kids' clothes.

### Methods

I wrote several Python functions to scrap the websites of some of the top retailers of kids' clothes in the UK (I haven't looked at international retailers because I'm based in the UK and I'm not swimming in free time). I'm using [Selenium](http://selenium-python.readthedocs.io/) to do this, storing the results in a MongoDB database for no reason other than I find using MongoDB really satisfying. It also means that querying the dataset is slightly more convenient than interrogating a giant Python dictionary.

The retailers under investigation are:

- [Asda (George)](https://direct.asda.com/george/kids/D25,default,sc.html)
- [Tesco](https://www.tesco.com/direct/clothing-accessories/baby-kids-clothing-shoes/cat3376645.cat)
- [Matalan](https://www.matalan.co.uk/kids-clothing)
- [Sainsburys (Tu)](https://tuclothing.sainsburys.co.uk/c/kids/kids)
- [Debenhams](http://www.debenhams.com/kids)
- [Mothercare](http://www.mothercare.com/clothing/)
- [H&M](http://www2.hm.com/en_gb/kids.html)
- [Next](http://www.next.co.uk/children)
- [Marks and Spencer](http://www.marksandspencer.com/c/kids)
- [Mamas and Papas](https://www.mamasandpapas.com/en-gb/c/clothing/)
- [Boots](http://www.boots.com/baby-child/kids-clothes-mini-club)
- [boohoo](http://www.boohoo.com/kids)
- [Peacocks](https://www.peacocks.co.uk/kidswear)
- [Primark](https://www.primark.com/en/products/new-arrivals/kids)

These were chosen according to picking the top results on a Google search for "UK+kids+clothes". I think they represent a pretty mainstream selection of where I might go to get clothes for my kids.
