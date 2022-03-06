# tsoha-rekrysovellus
_**Helsingin yliopiston tietokantasovellus kurssin harjoitustyönä tehty rekrytointisovellus**_

**Sovelluksessa on seuraavat ominaisuudet:**

- Käyttäjä voi valita kahden roolin väliltä: työntekijä ja työnantaja.
- Kumpikin käyttäjärooli voi luoda itselleen profiilin, johon voi kirjautua sisään. Profiiliin voi lisätä profiilitekstin. Työntekijä voi lisäksi lisätä tietoa työkokemuksesta ja koulutuksesta. Profiilitietoja voi muokata ja poistaa.
- Työnantaja voi luoda uuden työpaikkailmoituksen. Työpaikkailmoitukseen voi lisätä kuvauksen työpaikasta ja luoda työpaikalle hakulomakkeen.
- Työntekijä voi selata avoinna olevia työpaikkoja. Hän voi hakea työpaikkaa täyttämällä hakulomakkeen.
- Työnantaja näkee, kuinka monta henkilöä on hakenut kyseistä työpaikkaa ja voi tarkastella hakijoiden hakemuksia.
- Työnantaja voi valita hakijan työpaikkaan. Tällöin työpaikka siirtyy kategoriaan "Saadut työpaikat" kyseisen hakijan kohdalla. Muiden hakijoiden kohdalla työpaikka siirretään kategoriaan "Suljetut työpaikkailmoitukset". Työpaikkailmoitus suljetaan.
- Työntekijä voi selata hakemiaan työpaikkoja työnhaun statuksen mukaan. Statukset ovat: auki olevat haut, saadut työpaikat ja suljetut haut. Työntekijä voi tarkastella hakemustaan.
- Työnantaja voi poistaa työpaikkailmoituksen. Tällöin työpaikkailmoitus ei näy missään aiemmin mainituista kategorioista.
- Työpaikkailmoitus siirtyy automaattisesti "Suljetut haut" -kategoriaan, jos sen hakuaika umpeutuu.

Sovellus on testattavissa Herokussa osoitteessa: https://tsoha-rekrysovellus.herokuapp.com/ 
