# tsoha-rekrysovellus
Helsingin yliopiston tietokantasovellus kurssin harjoitustyönä tehty rekrytointisovellus

Sovelluksessa on seuraavat ominaisuudet:

- Käyttäjä voi valita kahden roolin väliltä: työntekijä ja työnantaja
- Kumpikin käyttäjärooli voi luoda itselleen profiilin, johon voi kirjautua sisään. Profiiliin voi lisätä kuvan ja profiilitekstin.

Lisäksi käyttäjäkohtaisesti on tarjolla seuraavat ominaisuudet:

- Työnantaja voi luoda uuden työpaikkailmoituksen. Työpaikkailmoitukseen voi lisätä kuvauksen työpaikasta ja hakulomakkeen. Hakulomakkeen kenttiä voi muokata.
- Työnantaja näkee, kuinka monta henkilöä on hakenut kyseistä työpaikkaa ja voi tarkastella hakijoiden hakemuksia.
- Työnantaja voi valita hakijan työpaikkaan. Tällöin valitulle hakijalle ilmoitetaan kyseisen työpaikkailmoituksen kohdalla, että hänet on valittu. Muille hakijoille ilmoitetaan, että heitä ei ole valittu kyseiseen paikkaan. Työpaikkailmoitukseen ei voi enää vastata tämän jälkeen.
- Työnantaja voi poistaa työpaikkailmoituksen halutessaan, jolloin se poistuu etusivulta ja kaikki siihen liittyvät hakemukset poistetaan. Tällöin paikkaa hakeneille näytetään viesti, että työpaikkailmoitus on poistettu.

- Työntekijä voi lisätä profiiliinsa työkokemus- ja koulutus -osiot.
- Työntekijä voi selata avoinna olevia työpaikkoja. Hän voi hakea työpaikkaa täyttämällä hakulomakkeen.
- Työntekijä voi selata hakemiaan työpaikkoja työnhaun statuksen mukaan. Statukset ovat: auki olevat haut, päättyneet haut (saadut työpaikat ja ei saadut työpaikat) ja poistetut ilmoitukset. Jos haku on vielä auki, työntekijä voi muokata hakulomakettaan.

Sovelluksen tila 20.2.2022:

- Lähes kaikki sovelluksen pääominaisuudet ovat valmiita. Seuraavat ominaisuudet puuttuvat:
      - Sovelluksen ulkoasu on vielä hyvin puutteellinen ja sisältää pelkkää html -kieltä.
      - Kysymyslomakkeissa on aina viisi kysymystä. Valmiissa versiossa kysymyksiä voi olla mitä tahansa väliltä 1-5.
      - CSRF-haavoittuvuutta ei ole korjattu.
      - Sovellusta ei voi vielä testata Herokussa.
