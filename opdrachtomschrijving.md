# Opdrachtomschrijving

<html>
  <style>
    th {
      padding-right: 48px;
      padding-left: 12px;
    }
    td {
      padding-left: 8px;
      padding-right: 8px;
    }
  </style>
  <table>
    <tr>
      <th>Naam</th>
      <td>Floris Kappen</td>
    </tr>
    <tr>
      <th>Jaar</th>
      <td>2022</td>
    </tr>
    <tr>
      <th>Vak</th>
      <td>IPASS</td>
    </tr>
    <tr>
      <th>Klas</th>
      <td>V1B</td>
    </tr>
  </table>
</html>

## Het project
Voor het IPASS project maak ik een muziekgenre herkenningsalgoritme. Dit zal gedaan worden door middel van een neuraal netwerk.

Het algoritme ondersteund een aantal genres. Het moet uiteindelijk te gebruiken zijn via een website waar een audiobestand geüpload moet kunnen worden. Dit audiobestand wordt dan naar het juiste formaat en de juiste lengte geconverteerd en geanalyseerd door het neurale netwerk. Het neurale netwerk trekt dan een conclusie en stuurt dit terug naar de gebruiker op de website.

## Stappenplan
Om dit te bereiken moet er hoog over het volgende gebeuren:

1. Onderzoeken welke neurale netwerkarchitectuur het beste past bij de probleemstelling
2. Verzameling van data
3. Datavergroting
4. Dataverwerking
5. Trainen van het neurale netwerk
6. Bruikbaar maken van het neurale netwerk door middel van een website

## Opdrachtgever
Dit is gemaakt voor een opdrachtgever. Op het moment is de opdrachtgever mijn vader. Dit algoritme en het bijbehorende product kan gebruikt worden om discussies over welk genre een liedje is te voorkomen.

Verder zal dit ook een nuttig product zijn voor platforms zoals Youtube Music en Soundcloud, die hiermee de liedjes die hun gebruikers uploaden automatisch kunnen taggen met een passend genre.

## Ervaring
Uit interesse heb ik in het verleden al een aantal online cursussen gevolgt rondom neurale netwerken. Dit specifieke idee kwam vanuit een cursus van Valerio Velardo, [The Sound of AI](https://www.youtube.com/playlist?list=PL-wATfeyAMNrtbkCNsLcpoAyBBRJZVlnf). 

Deze cursus legt uit hoe je vanaf 0 een neuraal netwerk maakt in python en de cursus focust zich specifiek op hoe je het toe kunt passen op muziek. Ook maak je een "genre classification" network met 3 verschillende architecturen, CNN, RNN en LSTM. Die laatste zal het meest relevant zijn aangezien het dingen onthoud en eerdere informatie erg belangrijk is bij muziek.

Met de kennis van de cursus heb ik een duidelijk stappenplan voor **stap 1, 4 en 5**. Verder heeft Valerio ook een youtube playlist voor [Audio Data Augmentation](https://www.youtube.com/playlist?list=PL-wATfeyAMNoR4aqS-Fv0GRmS6bx5RtTW) (voor **stap 3**).

Voor **stap 2** ben ik van plan om een aantal youtube playlists op te zoeken met muziek die bij verschillende genres past. Vervolgens schrijf ik een scriptje om de audio van die youtube filmpjes te downloaden en in het juiste formaat om te zetten. Dit is goed te doen gezien mijn ervaring als software engineer

Voor **stap 6** ben ik van plan om een super simpele website te maken die communiceert met een API endpoint die het gegeven audiobestand opsplitst in audiofragmenten met de juiste lengte en bitrate (de lengte en bitrate waarop het netwerk getraind is) en deze dan één voor één aan het netwerk geeft. De vaakst voorkomende voorspelling wordt dan terug gestuurd naar de front-end en weergegeven aan de gebruiker. Dit is goed te doen gezien mijn ervaring als full-stack web developer.

Voor meer details over mijn werkervaring zie mijn [LinkedIn](https://www.linkedin.com/in/floriskappen/).

Qua rekenkracht zal het inderdaad wat tijd kosten, hier moet ik natuurlijk rekening mee houden. Ik moet sowieso tensorflow met een GPU via CUDA werkend hebben, anders duurt het veelste lang. Ik ben niet van plan om een gigantische dataset te gebruiken, de voorspellingen hoeven uiteindelijk niet meer dan 95% accuraat te zijn neem ik aan.

