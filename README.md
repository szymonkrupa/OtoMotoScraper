# OtoMotoScraper
Scrape data from OtoMoto.pl car offers
<hr align="left">
<h3>Requirements:</h3>
<p >
  tqdm==4.62.2</br>
  getuseragent==0.0.7</br>
  pandas==1.3.2</br>
  beautifulsoup4==4.10.0</br>
</p>
<hr align="left">
<h3>Quick tutorial:</h3>

The scrape is based on 4 parameters:
<table>
    <tr>
        <td>
            • car brand,
        </td>
    </tr>
    <tr>
        <td>
            • car model,
        </td>
    </tr>
    <tr>
        <td>
            • year range (start year (in default 2013) and end year (in default current year)).
        </td>
    </tr>
</table>
<p>To get the proper name of the car brand and car model go to otomoto.pl website and manually select the desired manufacturer as well as model.
Click search and let's come back to the address bar.</p>
<p>Here we operate on an example search for BMW, series 5.</p>
<a href="https://imgbb.com/"><img src="https://i.ibb.co/NWgBT7f/Bar.png" alt="Bar" border="0"></a>
</br>
</br>
<p>The red highlight shows the correct spelling for the car brand; the green one shows the correct spelling for the car model.</p>
<p>Now what you need to do is to run the scraper script and provide above information,</br>
Example screen from terminal: (empty years means default values are selected; all pages tell how many subpages will be scrape.)</br></p>
<a href="https://imgbb.com/"><img src="https://i.ibb.co/rmzkfJ9/Scraper1.png" alt="Scraper1" border="0"></a>
</br>
</br>
<hr align="left">
<p>Data is saved in the CSV file in the script location</p>
