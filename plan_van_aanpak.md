# Plan van aanpak

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

## Probleemstelling

De opdrachtgever heeft vaak discussies over welk genre een liedje is. De opdrachtgever verwacht een MVP (minimum viable product) applicatie met het gebruik van kunstmatige intelligentie (deep learning) het genre van een audiobestand vastlegt.

Deze eerste versie hoeft alleen de fundamentele muziekgenres te ondersteunen. Dat is de volgende lijst aan muziek:

Deze 4 zijn het belangrijkst:
- Blues
- Klassiek
- Jazz
- Reggae

Daarna is het ook mooi als deze genres ondersteund worden:
- Country
- Electronisch
- Volksmuziek
- Hip-hop
- Rock

## Beschrijving gekozen algoritme

In de "feature extraction" fase van de training pipeline is ervoor gekozen om het mel-frequency cepstrum (MFC) algoritme algoritme te gebruiken en dan ook zelf te implementeren. 

> MFCC's worden vaak gebruikt als functies in spraakherkenningssystemen, zoals de systemen die automatisch nummers kunnen herkennen die in een telefoon worden ingesproken.     
> MFCC's worden ook steeds vaker gebruikt in toepassingen voor het ophalen van muziekinformatie, zoals genreclassificatie, metingen van audio-overeenkomst, enz.    
>-- <cite>[Wikipedia: Mel-frequency cepstrum](https://en.wikipedia.org/wiki/Mel-frequency_cepstrum)</cite>

Toepasselijke bronnen:
- [Music Genre Classification using MFCC, SVM and BPNN](http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.695.7456&rep=rep1&type=pdf)
- [Feature extraction methods LPC, PLP and MFCC in speech recognition](https://www.researchgate.net/publication/261914482_Feature_extraction_methods_LPC_PLP_and_MFCC_in_speech_recognition)
- [Mel Frequency Cepstral Coefficients for Music Modelling](https://ismir2000.ismir.net/papers/logan_paper.pdf)
- [Wikipedia: Mel-frequency cepstrum](https://en.wikipedia.org/wiki/Mel-frequency_cepstrum)

## Uit te voeren taken
1. Verzameling van data*
2. Datavergroting
3. Ontwikkeling eigen implementatie van MFC algoritme*
4. Feature extraction (dataverwerking)*
5. Trainen van het neurale netwerk*
6. Bruikbaar maken van het neurale netwerk in de command line*
7. Schrijven van een test om de uitkomst te valideren*
8. Documentatie schrijven*
9. Projectsamenvatting*
10. Poster*
11. Bruikbaar maken van het neurale netwerk door middel van een website


\* noodzakelijk

## Planning

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
      <th>Projectweek</th>
      <th>Uit te voeren taken</th>
    </tr>
    <tr>
      <td>Elke projectweek</td>
      <td>8</td>
    </tr>
    <tr>
      <td>D9 (13-06-2022)</td>
      <td>1, 2 en start 3</td>
    </tr>
    <tr>
      <td>D10 (20-06-2022)</td>
      <td>Afmaken 3, 4, 5, 6, 7</td>
    </tr>
    <tr>
      <td>D11 (27-06-2022)</td>
      <td>9, 10, indien tijd 11</td>
    </tr>
  </table>
</html>

De taaknummers refereren naar de takenlijst hierboven.

## Risico's

Gezien mijn gebrek aan ervaring rondom het zelf implementeren van algoritmes ligt er wat onzekerheid rondom het implementeren van het MFC algoritme. Er is een 50% kans dat dit extra lang duurt. Om de impact hiervan tot een minimum te houden heb ik hier de meeste tijd voor ingepland. 

Ook ligt er wat risico rondom het beschikbaar maken van de uiteindelijke applicatie via een website. Dit kost namelijk vrij veel tijd en is daarom alleen mogelijk als ik tijd over heb, bijvoorbeeld als de implementatie van het algoritme meevalt. Die taak (nummer 11) is daarom ook niet verplicht.

Als laatste is er wat onzekerheid rondom de datavergroting (taak nummer 2). Dit komt omdat ik nog niet eerder audio data heb vergroot en dus goed moet onderzoeken welke technieken er bestaan en wat de effectiviteit hiervan is. Na dit onderzoek zal ik bepalen of ik hier tijd aan ga besteden, daarom is deze taak ook optioneel. De impact hiervan zal te zien zijn in de nauwkeurigheid van het neurale netwerk. Gelukkig is nauwkeurigheid niet het aller belangrijkste binnen dit project dus de impact is dan vrij klein. Ik gok op een 70% kans dat datavergroting wel te doen is in de beschikbare tijdsspanne.
