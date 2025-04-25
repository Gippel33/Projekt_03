**Projekt_03**

Třetí projekt na Python Akademii od Engeta.

**Popis Projektu**

Projekt slouží k extrahování výsledků z parlamentních voleb v roce 2017.

Odkaz k prohlédnutí
[zde](https://www.volby.cz/pls/ps2017nss/ps3?xjazyk=CZ).

**Instalace knihoven**

Knihovny použité v kódu a jejich verze jsou v souboru `requirments.txt`.

Pro instalaci doporučuji použít nové virtuální prostředí a
s nainstalovaným manažerem spustit následovně:

$ pip --version                     # kontrola verze manažeru

$ pip install -r requirments.txt    # nainstalujeme knihovny

**Spouštění projektu**

Spuštění programu `main.py` v rámci příkazového řádku vyžaduje dva povinné
argumenty.

- Prvním je odkaz (vložený do uvozovek) okresu, do kterého se proklikni
  přes `X` ve sloupci `Výběr obce`.

Odkaz zapiš v této podobě:

    --district_ref "<tvůj_odkaz>"

- Druhým je název výstupního souboru s příponou .csv.

Název zapiš za první argument takto:

    --file_name <tvůj_název>.csv

**Ukázka projektu**

Výsledky hlasování pro okres Benešov:

1\. argument \-- district_ref
\"[https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2101](https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2101)\"

2\. argument results_Benešov.csv

Spouštění programu:

python main.py \--district_ref
\"https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2101\"
\--file_name results_Benešov.csv
