# OtoMotoScraper

*Scrape data from OtoMoto.pl - polish car offers website.*

## Project description

We always want to get the best value for money, and this applies not only to cars. Browsing dozens of car offers is time-consuming. Multiple tabs, open in your browser give you a headache. Thanks to this simple, script you can have all the necessary information in tabular form, which is easier to compare. See the example screenshot output at the bottom of the readme.

## Requirements:

tqdm==4.62.2</br>
getuseragent==0.0.7</br>
pandas==1.3.2</br>
beautifulsoup4==4.10.0</br>

## Quick Tutorial:

<p>The scrape is based on 4 parameters:</br>
• car brand</br>
• bar model</br>
• year range (start year (in default 2013) and end year (in default current year))
</p>
<p>For the exact name and model of the car, go to www.otomoto.pl. Please select the appropriate manufacturer and model from their search lists. Click search and go back to your browser address bar.
</br>
Let's take BMW, series 5, as an example. (You should see a similar result with your selected car).</p>
<a href="https://imgbb.com/"><img src="https://i.ibb.co/NWgBT7f/Bar.png" alt="Bar" border="10"></a>
</br>
The red highlight shows the correct spelling for the car brand; the green one shows the correct spelling for the car model.
</br>
<p>Now, let's run the OtoMotoScraper.py script and feed it with the above information,</br>
Example screen from a terminal: (empty years means default values are selected; all pages tell how many subpages will be scraped).</p>
<a href="https://imgbb.com/"><img src="https://i.ibb.co/rmzkfJ9/Scraper1.png" alt="Scraper1" border="10"></a>
</br>
<p>Data is saved in the CSV file in the script location. Gather data will need to be cleaned for further analysis.</br>Example output:</p>
<a href="https://ibb.co/fHPG2My"><img src="https://i.ibb.co/jD1ZThQ/Output-example.png" alt="Output-example" border="10"></a>
