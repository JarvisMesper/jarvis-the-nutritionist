# Jarvis the Nutritionist

Jarvis is here to help you for your groceries, food questions and so on ! He's smart, kind and neutral, he won't judge you :)


## Structure

This repo contains some tests about APIs calls and techs. The main thing here is in the `api/` folder where you can find the webservices used by the chatbot to interact with the OpenFood API.

The bot itself is in this repo : [https://github.com/JarvisMesper/jarvis-the-bot](https://github.com/JarvisMesper/jarvis-the-bot).


## Technologies

The chatbot is built with the [Microsoft Bot Framework](https://dev.botframework.com) in NodeJS. It uses [LUIS (Language Understanding Intelligent Service)](https://www.luis.ai) to process and understand what the user is asking him. The bot talks to an API made with [Flask](http://flask.pocoo.org) in Python and hosted on an Ubuntu virtual machine. This API retreive data from [OpenFood](https://www.openfood.ch). All of this is hosted on Azure Bot Service for the demo.

Jarvis is able to understand basic questions like "Who are you ?", both in French and English. He can retrieve product information when the user send him a picture of the barcode using [quaggaJS](https://serratus.github.io/quaggaJS/) library for the scan.

He also remembers the last scanned products, and let you compare products together.


## Context

This project was made during the [Open Food Hackdays](https://food.opendata.ch) (10/11 February 2017) oragnized by [OpenData.ch](https://opendata.ch) @ EPFL.


## Contributors

[1]: http://i.imgur.com/wWzX9uB.png
[2]: https://twitter.com/jackycasas_
[3]: https://twitter.com/nathan_quint

- [Jacky Casas](https://github.com/acknowledge) [![twitter profile][1]][2]
- [Nathan Quinteiro](https://github.com/nathanquinteiro) [![twitter profile][1]][3]
- [Christian Abbet](https://github.com/christlf)


![jarvis the nutritionist icon](statics/bot-icon-squared-400.png)