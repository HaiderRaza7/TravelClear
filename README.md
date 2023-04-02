# TravelClear
 
## Inspiration
When we heard about this weekend's theme of exploration, we all instantly thought of a tourist spot recommendation site because we understand just how tedious it is to plan out a trip to a city that you and (probably) no one else you know have visited before.

## What it does
After the user submits the name of the city they are currently considering planning a trip for, the python script receives this piece of information and uses various APIs to scrape the web for information about this city. If the user doesn't have any city in mind, then they could ask for a random city to be suggested (which the site gets from a preset list of 100 very popular tourist destinations).

## How we built it
This website was developed using HTML, CSS, React, and Python with the help of flask to integrate these technologies together. This website is also powered by ChatGPT and OpenWeatherMap through their respective APIs openai and OpenWeatherMap API.

## Challenges we ran into
We ran into two massive roadblocks while building this project: Finding a relevant, working web scraping API, and integrating React and Python using the flask framework. We are able to discover the OpenWeatherMap API fairly quickly, but was held back for hours because there was no easily accessible and free APIs that could actually recommend tourist spots for a specific city. Eventually we settled on ChatGPT since it can do that and more which is why we later added a general description for the city.

## Accomplishments that we're proud of
As discussed above, finding the relevant APIs proved to be a bigger challenge than expected so when we were able to solve that issue it felt like a great milestone in our project. Integrating React and Python using flask was also a quite rewarding experience since no one on the team knew all three technologies so it took quite a bit of teamwork and coordination to accomplish this part of our website.

## What we learned
Those of us who worked on the back-end side of the project learned quite a bit about web scraping and optimizing ChatGPT prompts to get exactly what we need for our purposes. We also explored a lot of different API options to see which ones would be able to be integrated with our project and the various languages that were used. Overall this improved our backend knowledge and overall familiarity with Pythin. On the other hand, our front-end devs absorbed knowledge and experience on how to integrate two completely different technologies (Python and React) through a library (flask). In short, it was a learning experience for everyone regardless of the role they played in the making of our project.

## What's next for TravelClear
We've been thinking about introducing more flexibility to it so that user can not only enter a city, but maybe a state, province, or even a country. Maybe we can take this project to the next level by not only recommending tourist spots, but going so far as to recommend accommodation options or, if the user is comfortable with providing their current location, travel fares. 