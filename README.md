# tsoha-rekrysovellus
_**Helsingin yliopiston tietokantasovellus kurssin harjoitustyönä tehty rekrytointisovellus**_

**Sovelluksessa on tällä hetkellä seuraavat ominaisuudet:**

- Käyttäjä voi valita kahden roolin väliltä: työntekijä ja työnantajä.
- Kumpikin käyttäjärooli voi luoda itselleen profiilin, johon voi kirjautua sisään. Profiiliin voi lisätä profiilitekstin (toteutettu).
- Työntekijä voi lisätä tietoa työkokemuksesta ja koulutuksesta. 
- Työnantaja voi luoda uuden työpaikkailmoituksen. Työpaikkailmoitukseen voi lisätä kuvauksen työpaikasta ja hakulomakkeen. Hakulomakkeen kenttiä voi muokata.
- Työnantaja näkee, kuinka monta henkilöä on hakenut kyseistä työpaikkaa ja voi tarkastella hakijoiden hakemuksia.
- Työnantaja voi valita hakijan työpaikkaan. Tällöin valitulle hakijalle ilmoitetaan kyseisen työpaikkailmoituksen kohdalla, että hänet on valittu. Muille hakijoille ilmoitetaan, että heitä ei ole valittu kyseiseen paikkaan. Työpaikkailmoitus suljetaan eikä siihen voi enää vastata tämän jälkeen.
- Työntekijä voi selata avoinna olevia työpaikkoja. Hän voi hakea työpaikkaa täyttämällä hakulomakkeen.
- Työntekijä voi selata hakemiaan työpaikkoja työnhaun statuksen mukaan. Statukset ovat: auki olevat haut, päättyneet haut (saadut työpaikat ja ei saadut työpaikat) ja poistetut ilmoitukset. Työntekijä voi tarkastella hakemustaan.

**Puuttuvat ominaisuudet 20.2.2022:**

- Sovelluksen ulkoasu on vielä hyvin puutteellinen. Ulkoasussa on epäloogisuuksia (esim. näyttää profiilissa "Työkokemuksesi" -otsikon, vaikka käyttäjä ei lisännyt työkokemusta). Lomakkeiden vastauskentät ovat liian pieniä.
- Hakulomakkeissa on aina viisi kysymystä. Valmiissa versiossa kysymyksiä voi olla mitä tahansa väliltä 1-5.
- CSRF-haavoittuvuutta ei ole korjattu.
- Työntekijä voi poistaa ja muokata lisäämiänsä tietoja koulutuksesta ja työkokemuksesta.
- Työnantaja voi tarkastella paikkaa hakeneiden työntekijöiden profiilia.
- Työnantaja voi poistaa työpaikkailmoituksen halutessaan, jolloin se poistuu etusivulta ja kaikki siihen liittyvät hakemukset poistetaan. Tällöin työpaikkailmoitus siirtyy "Poistetut ilmoitukset" -kategoriaan paikkaa hakeneiden käyttäjien työpaikkailmotuksissa.
- Työpaikkailmoitus siirtyy automaattisesti "haku päättynyt" -kategoriaan, kun työopaikkailmoituksessa kerrottu hakuaika päättyy.

**Mahdollisuuksien mukaan valmiiseen sovellukseen toteutetaan seuraavat ominaisuudet:**

- Profiiliin voi lisätä kuvan.
- Käyttäjä voi poistaa tilinsä, jolloin hänen profiilinsa ei ole enää tarkasteltavissa. 
- Jos työpaikan hakuaika on vielä auki, työntekijä voi muokata lähettämäänsä hakulomaketta.

**HUOM!** Sovellusta ei voi vielä testata Herokussa. Tavoitteena on korjata tämä 21.2.2022.
