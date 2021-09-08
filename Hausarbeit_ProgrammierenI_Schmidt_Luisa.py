import glob
from bs4 import BeautifulSoup
import re
import pandas as pd
from os.path import basename
import numpy as np
import pygal
from pygal.style import CleanStyle
from pygal.style import Style

# eigene Farbwerte entsprechend der Parteifarben definieren
# rosa      rot       grün      schwarz     gelb      hellblau
custom_style = Style(colors=('#E80080', '#FF0000', '#9BC850', '#0F0F0F', '#ffeb44', '#1E90FF',))


# bereits erstellte txt-Listen einlesen und leicht bereinigen
def read_list(filename):
    with open(filename, "r", encoding="utf8") as infile:
        list_import = infile.read()
        list_import = re.sub(r"\n", " ", list_import, flags=re.S)
        list_import = re.sub(", ", ",", list_import, flags=re.S)
        list_import = list_import.split(",")
        return list_import


# XML-Plenarprotokolle einlesen
def read_textfile(textfile):
    with open(textfile, "r", encoding="utf8") as infile:
        text = infile.read()
        return text


# XML-Dokumente bereinigen
def clean_texts(text):
    cleansed = re.sub(r"\t", " ", text)
    cleansed = re.sub("\.", "", cleansed)
    cleansed = re.sub(",", "", cleansed)
    cleansed = re.sub("\?", "", cleansed)
    cleansed = re.sub("!", "", cleansed)
    cleansed = re.sub("\) :", "):", cleansed)
    # Flag re.S sucht über mehrere Zeilen mit "." als special character
    # für Texte der ersten Periode
    cleansed = re.sub(r"<\?xml(.*?) eröffnet.", " ", cleansed, flags=re.S)
    cleansed = re.sub(r"\(Schluß der Sitzung:(.*?)</DOKUMENT>", "", cleansed, flags=re.S)
    cleansed = re.sub(r"\(Schluß: (.*?)</DOKUMENT>", "", cleansed, flags=re.S)
    cleansed = re.sub(r"\(Schluss: (.*?)</DOKUMENT>", "", cleansed, flags=re.S)
    # für Texte der 7. und 14. Periode
    cleansed = re.sub(r"<?xml(.*?)Beginn:", "", cleansed, flags=re.S)
    # für Texte der 19. Periode
    cleansed = re.sub(r"<\?xml (.*?) <rede id", "<rede id", cleansed, flags=re.S)
    cleansed = re.sub(r"</sitzungsverlauf(.*?)</dbtplenarprotokoll>", "", cleansed, flags=re.S)
    cleansed = re.sub(r"<kommentar>(.*?)</kommentar>", "", cleansed, flags=re.S)
    cleansed = re.sub(r"<", " <", cleansed, flags=re.S)
    cleansed = re.sub(r"</", " </", cleansed, flags=re.S)
    cleansed = re.sub(r">", "> ", cleansed, flags=re.S)
    return cleansed


# sucht alle Sprecher anhand der Angabe der Partei in Klammern und mit : raus, da diese Kombination nur
# vorkommt, wenn ein neuer Sprecher beginnt
# mehrere Suchbefehle für eine Partei, da die Parteien in den verschiedenen Perioden unterschiedlich bezeichnet werden
def split_text_new_speaker(cleansed):
    list_search_results = []
    find_all_speakers_CDU1 = re.finditer("\(CDU\):", cleansed)
    for item in find_all_speakers_CDU1:
        list_search_results.append(item.end())
    find_all_speakers_CDU2 = re.finditer("\(CSU\):", cleansed)
    for item in find_all_speakers_CDU2:
        list_search_results.append(item.end())
    find_all_speakers_CDU3 = re.finditer("\(CDU und CSU\):", cleansed)
    for item in find_all_speakers_CDU3:
        list_search_results.append(item.end())
    find_all_speakers_CDU4 = re.finditer("\(CDU/CSU\):", cleansed)
    for item in find_all_speakers_CDU4:
        list_search_results.append(item.end())
    find_all_speakers_CDU5 = re.finditer("\(BP\):", cleansed)
    for item in find_all_speakers_CDU5:
        list_search_results.append(item.end())
    find_all_speakers_CDU6 = re.finditer("\(CDU CSU\):", cleansed)
    for item in find_all_speakers_CDU6:
        list_search_results.append(item.end())
    find_all_speakers_SPD = re.finditer("\(SPD\):", cleansed)
    for item in find_all_speakers_SPD:
        list_search_results.append(item.end())
    find_all_speakers_GRUENE = re.finditer("\(BÜNDNIS 90/DIE GRÜNEN\):", cleansed)
    for item in find_all_speakers_GRUENE:
        list_search_results.append(item.end())
    find_all_speakers_LINKE1 = re.finditer("\(DIE LINKE\):", cleansed)
    for item in find_all_speakers_LINKE1:
        list_search_results.append(item.end())
    find_all_speakers_LINKE2 = re.finditer("\(PDS\):", cleansed)
    for item in find_all_speakers_LINKE2:
        list_search_results.append(item.end())
    find_all_speakers_FDP1 = re.finditer("\(F D P \):", cleansed)
    for item in find_all_speakers_FDP1:
        list_search_results.append(item.end())
    find_all_speakers_FDP2 = re.finditer("\(FDP\):", cleansed)
    for item in find_all_speakers_FDP2:
        list_search_results.append(item.end())
    find_all_speakers_KPD = re.finditer("\(KPD\):", cleansed)
    for item in find_all_speakers_KPD:
        list_search_results.append(item.end())
    find_all_speakers_WAV = re.finditer("\(WAV\):", cleansed)
    for item in find_all_speakers_WAV:
        list_search_results.append(item.end())
    find_all_speakers_DP = re.finditer("\(DP\):", cleansed)
    for item in find_all_speakers_DP:
        list_search_results.append(item.end())
    find_all_speakers_FU = re.finditer("\(FU\):", cleansed)
    for item in find_all_speakers_FU:
        list_search_results.append(item.end())
    find_all_speakers_FRAKTIONSLOS = re.finditer("\(Fraktionslos\):", cleansed)
    for item in find_all_speakers_FRAKTIONSLOS:
        list_search_results.append(item.end())
    find_all_speakers_PDS = re.finditer("\(PDS\):", cleansed)
    for item in find_all_speakers_PDS:
        list_search_results.append(item.end())
    find_all_speakers_Zentrum = re.finditer("\(Z\):", cleansed)
    for item in find_all_speakers_Zentrum:
        list_search_results.append(item.end())
    find_all_speakers_DRP = re.finditer("\(DRP\):", cleansed)
    for item in find_all_speakers_DRP:
        list_search_results.append(item.end())
    list_search_results.append(len(cleansed))
    list_search_results.sort()
    return list_search_results


# findet den Start der Zeile, gleichbedeutend mit Beginn des Namens
# initial ist beginning_of_line das Ende der Parteiklammer, bspw. bei (SPD) die Klammer zu ")"
def find_start_of_line(cleaned_text, list_search_results, i):
    beginning_of_line = list_search_results[i]
    # checken, dass Index in cleaned text ist, damit Index nicht out of range
    if len(cleaned_text) == beginning_of_line:
        return
    begin_found = False
    while not begin_found:
        str = cleaned_text[beginning_of_line]
        if str == "\n":
            begin_found = True
        else:
            beginning_of_line = beginning_of_line - 1
            # nur 1 zurückgehen, weil '\n' als 1 gezählt wird
    # beginning_of_line + 1 um nicht "\n" mitzunehmen
    name_and_party = cleaned_text[int(beginning_of_line + 1):(int(list_search_results[i]))]
    whole_speaker_text = cleaned_text[int(beginning_of_line + 1):(int(list_search_results[i + 1]))]
    return [name_and_party, whole_speaker_text]


# Erstellung des Dictionarys, in dem Geschlecht und Partei der Sprechenden als auch deren Verwendung der
# Substantive und Gesamtlänge des Sprechertextes notiert wird
def create_dictionary(parties, female_MPs, male_words, female_words, neutral_words, single_speakers_texts):
    dict_words = {"Gender of speaker:": " ", "Party of speaker:": " ", "Male words:": 0, "Female words:": 0,
                  "Neutral words:": 0, "Total words:": 0}
    word_tokens_name_party = single_speakers_texts[0].split()
    # fehlerhafte Formatierungen umgehen mit return-Statement:
    # für Sprechertexte, für die aufgrund fehlerhafter Formatierungen Partei und Name nicht richtig
    # ermittelt werden können, wird kein Dictionary erstellt
    if len(word_tokens_name_party) < 2:
        return
    # nach Partei suchen und ins Dictionary eintragen
    party_name = word_tokens_name_party[-1]
    if party_name in parties:
        dict_words["Party of speaker:"] = party_name
    else:
        dict_words["Party of speaker:"] = "?"

    # Nachname mit Liste weiblicher Abgeordneter abgleichen und Geschlecht ins Dictionary eintragen
    surname = word_tokens_name_party[-2]
    if len(word_tokens_name_party) == 1:
        return
    if surname in female_MPs:
        dict_words["Gender of speaker:"] = "w"
    else:
        dict_words["Gender of speaker:"] = "m"

    # männliche, weibliche, neutrale Wörter mit Listen abgleichen und in Dictionary eintragen
    word_tokens_speech = single_speakers_texts[1].split()
    for word in word_tokens_speech:
        dict_words["Total words:"] += 1
        if word in male_words:
            dict_words["Male words:"] += 1
        elif word in female_words:
            dict_words["Female words:"] += 1
        elif word in neutral_words:
            dict_words["Neutral words:"] += 1
    return dict_words


# sucht in SoupObject nach Nachname, Fraktion/Partei und dem Sprechertext
def extract_info_from_soup(single_speeches):
    # findet alle XML-Tags <nachname>
    speaker = single_speeches.find("nachname")
    # findet alle XML-Tags <fraktion> und erstellt einen String, der den Partei-/Fraktionsnamen enthält
    party = single_speeches.find_all("fraktion")
    for element in single_speeches.find_all("fraktion"):
        party = str(element.text)
    # filtert den Redetext anhand der für "Klasse" vergebenen Attribute über Dictionary (siehe Strukturdefinition der
    # Protokolle)
    speech = single_speeches.find_all("p", {"klasse": ("J_1", "J", "Z", "O")})
    return speaker, party, speech


# Erstellung des Dictionarys, in dem Geschlecht und Partei der Sprechenden als auch deren Verwendung der
# Substantive und Gesamtlänge des Sprechertextes notiert wird
def create_dictionary_from_soup(parties, female_MPs, male_words, female_words, neutral_words, analyse):
    # erstellt Dictionary mit gleichem Aufbau wie oben, damit Zusammenführung möglich ist
    dict_words = {"Gender of speaker:": " ", "Party of speaker:": " ", "Male words:": 0, "Female words:": 0,
                  "Neutral words:": 0, "Total words:": 0}
    word_tokens_party = str(analyse[1])
    get_party = word_tokens_party.split()
    party_name = get_party[0]
    if party_name in parties:
        dict_words["Party of speaker:"] = party_name
    else:
        dict_words["Party of speaker:"] = "?"

    # Nachname mit Liste weiblicher Abgeordneter abgleichen und Geschlecht ins Dictionary eintragen
    soup_object_surname = str(analyse[0])
    word_tokens_surname = soup_object_surname.split()
    if len(word_tokens_surname) < 2:
        return
    surname = word_tokens_surname[1]
    if surname in female_MPs:
        dict_words["Gender of speaker:"] = "w"
    else:
        dict_words["Gender of speaker:"] = "m"

    # männliche, weibliche, neutrale Wörter mit Listen abgleichen und in Dictionary eintragen
    soup_object_speech = str(analyse[2])
    word_tokens_speech = soup_object_speech.split()
    for word in word_tokens_speech:
        # zählt Gesamtwortanzahl pro Text, damit am Ende relative Werte verglichen werden können
        dict_words["Total words:"] += 1
        if word in male_words:
            dict_words["Male words:"] += 1
        elif word in female_words:
            dict_words["Female words:"] += 1
        elif word in neutral_words:
            dict_words["Neutral words:"] += 1
    return dict_words


# Abspeichern des Dictionarys als DataFrame zur Weiterverarbeitung
def save_dictionary_as_df(dict_words):
    data_frame = pd.DataFrame(dict_words)
    # tauscht Zeilen und Spalten
    data_frame = data_frame.T
    # füllt Lücken mit 0
    data_frame.fillna(0, inplace=True)
    # speichert den gesamten DataFrame, damit Rohdaten verfügbar bleiben
    with open("HausarbeitRohdaten.csv", "w", encoding="utf-8") as outfile:
        data_frame.to_csv(outfile, sep=",")
    return data_frame


# liest DataFrame mit Rohdaten zur Weiterverarbeitung ein
def read_table():
    with open("HausarbeitRohdaten.csv", "r", encoding="utf-8") as infile:
        table_data = pd.read_csv(infile, sep=",", index_col=0)
    return table_data


# führt Berechnungen durch, die für Erstellung des Liniendiagramms benötigt werden (Summen, Prozentwerte)
def calculations_for_lineplot(table_data):
    # summiert die absolute Anzahl von male/female/neutral words pro Periode zur Weiterverarbeitung in neuen Zeilen auf
    table_data.loc["Gesamt Periode 01, absolut"] = np.sum(table_data.loc["Anfang Periode 01": "Anfang Periode 07",
                                                          "Male words:": "Total words:"], axis=0)
    table_data.loc["Gesamt Periode 07, absolut"] = np.sum(table_data.loc["Anfang Periode 07": "Anfang Periode 14",
                                                          "Male words:": "Total words:"], axis=0)
    table_data.loc["Gesamt Periode 14, absolut"] = np.sum(table_data.loc["Anfang Periode 14": "Anfang Periode 19",
                                                          "Male words:": "Total words:"], axis=0)
    table_data.loc["Gesamt Periode 19, absolut"] = np.sum(table_data.loc["Anfang Periode 19": "ENDE",
                                                          "Male words:": "Total words:"], axis=0)
    # berechnet relative Häufigkeit der Wörter pro Periode
    table_data.loc["Gesamte Periode 01, relativ (in %)"] = table_data.loc["Gesamt Periode 01, absolut",
                                                           "Male words:": "Neutral words:"].div(table_data.loc
                                                                                                [
                                                                                                    "Gesamt Periode 01, absolut", "Total words:"])
    table_data.loc["Gesamte Periode 07, relativ (in %)"] = table_data.loc["Gesamt Periode 07, absolut",
                                                           "Male words:": "Neutral words:"].div(table_data.loc
                                                                                                [
                                                                                                    "Gesamt Periode 07, absolut", "Total words:"])
    table_data.loc["Gesamte Periode 14, relativ (in %)"] = table_data.loc["Gesamt Periode 14, absolut",
                                                           "Male words:": "Neutral words:"].div(table_data.loc
                                                                                                [
                                                                                                    "Gesamt Periode 14, absolut", "Total words:"])
    table_data.loc["Gesamte Periode 19, relativ (in %)"] = table_data.loc["Gesamt Periode 19, absolut",
                                                           "Male words:": "Neutral words:"].div(table_data.loc
                                                                                                [
                                                                                                    "Gesamt Periode 19, absolut", "Total words:"])
    # reduziert Tabelle auf die neu erstellten Zeilen
    table_data_lineplot = table_data.loc["Gesamt Periode 01, absolut":"Gesamte Periode 19, relativ (in %)", :]
    with open("Daten für Lineplot.csv", "w", encoding="utf8") as outfile:
        table_data_lineplot.to_csv(outfile, sep=",")
    return table_data_lineplot


# Erstellung des Liniendiagramms
def make_lineplot_words_used(table_data_lineplot):
    # legt Grundsätzliches fest: Stil, Titel, Achsenbeschriftungen
    line_chart = pygal.Line(style=CleanStyle, legend_at_bottom=True,
                            legend_at_bottom_columns=3)
    # # entkommentieren für Diagrammtitel
    # line_chart.title = "Verwendung verschiedener Substantive je Wahlperiode"
    line_chart.y_title = "Relative Häufigkeit (in %)"
    line_chart.x_labels = ("Periode 1", "Periode 7", "Periode 14", "Periode 19")
    # Daten aus der Tabelle in line plot einpflegen
    line_chart.add("Männliche Substantive", table_data_lineplot.loc["Gesamte Periode 01, relativ (in %)":
                                                                    "Gesamte Periode 19, relativ (in %)",
                                            "Male words:"])
    line_chart.add("Weibliche Substantive", table_data_lineplot.loc["Gesamte Periode 01, relativ (in %)":
                                                                    "Gesamte Periode 19, relativ (in %)",
                                            "Female words:"])
    line_chart.add("Neutrale Substantive", table_data_lineplot.loc["Gesamte Periode 01, relativ (in %)":
                                                                   "Gesamte Periode 19, relativ (in %)",
                                           "Neutral words:"])
    # Speichern der Datei als .svg
    line_chart.render_to_file("Frequency-MFN-words-Periods.svg")


# führt Berechnungen durch, die für Erstellung des ersten Balkendiagramms benötigt werden (Summen, Prozentwerte)
def calculations_for_barchart_speakers(table_data):
    # sammelt Daten der männlichen Sprecher, summiert sie auf und ermittelt relative Häufigkeit
    table_data.loc["Male speakers, absolute use"] = table_data.loc[table_data["Gender of speaker:"] == "m",
                                                                   ["Male words:", "Female words:", "Neutral words:",
                                                                    "Total words:"]].sum()
    table_data.loc["Male speakers, relative use (in %)"] = table_data.loc["Male speakers, absolute use", "Male words:":
                                                                                                         "Neutral words:"].div(
        table_data.loc["Male speakers, absolute use", "Total words:"])

    # sammelt Daten der weiblichen Sprecher, summiert sie auf und ermittelt relative Häufigkeit
    table_data.loc["Female speakers, absolute use"] = table_data.loc[table_data["Gender of speaker:"] == "w",
                                                                     ["Male words:", "Female words:", "Neutral words:",
                                                                      "Total words:"]].sum()
    table_data.loc["Female speakers, relative use (in %)"] = table_data.loc["Female speakers, absolute use",
                                                             "Male words:": "Neutral words:"].div(
        table_data.loc["Female speakers, absolute use", "Total words:"])

    # reduziert die Tabelle auf essenzielle Zeilen und Spalten
    table_data_barchart_speakers = table_data.loc["Male speakers, absolute use": "Female speakers, relative use (" \
                                                                                 "in %)", :]

    with open("Daten für Barchart Sprecher.csv", "w", encoding="utf8") as outfile:
        table_data_barchart_speakers.to_csv(outfile, sep=",")
    return table_data_barchart_speakers


# erstellt Balkendiagramm
def make_barchart_speakers(table_data_barchart_speakers):
    # legt Grundsätzliches fest: Stil, Titel, Achsenbeschriftungen
    bar_chart = pygal.Bar(style=CleanStyle, legend_at_bottom=True)
    # # entkommentieren für Diagrammtitel
    # bar_chart.title = "Verwendung verschiedener Substantive in Abhängigkeit zu Geschlecht"
    bar_chart.y_title = "Relative Häufigkeit (in %)"
    bar_chart.x_labels = ("Männliche Substantive", "Weibliche Substantive", "Neutrale Substantive")

    # Daten aus Tabelle in line chart einpflegen
    bar_chart.add("Männliche Sprecher", [table_data_barchart_speakers.loc["Male speakers, relative use (in %)",
                                                                          "Male words:"],
                                         table_data_barchart_speakers.loc[
                                             "Male speakers, relative use (in %)", "Female words:"],
                                         table_data_barchart_speakers.loc[
                                             "Male speakers, relative use (in %)", "Neutral words:"]])

    bar_chart.add("Weibliche Sprecher", [table_data_barchart_speakers.loc["Female speakers, relative use (in %)",
                                                                          "Male words:"],
                                         table_data_barchart_speakers.loc[
                                             "Female speakers, relative use (in %)", "Female words:"],
                                         table_data_barchart_speakers.loc[
                                             "Female speakers, relative use (in %)", "Neutral words:"]])
    # Speichern der Datei als .svg
    bar_chart.render_to_file("Distribution-MFN-words-Gender.svg")


# führt Berechnungen durch, die für Erstellung des zweiten Balkendiagramms benötigt werden (Summen, Prozentwerte)
def calculations_for_bar_chart_parties(table_data):
    # je Parteien/Fraktionen im Bundestag: sammelt Daten aus Tabelle, summiert sie und berechnet relative
    # Häufigkeit (analog zu Verfahren bei männlichen und weiblichen Redner/-innen)

    # SPD
    table_data.loc["SPD"] = table_data.loc[table_data["Party of speaker:"] == "SPD",
                                           ["Male words:", "Female words:", "Neutral words:",
                                            "Total words:"]].sum()
    table_data.loc["(SPD):"] = table_data.loc[table_data["Party of speaker:"] == "(SPD):",
                                              ["Male words:", "Female words:", "Neutral words:",
                                               "Total words:"]].sum()
    table_data.loc["SPD speakers"] = np.sum(table_data.loc["SPD": "(SPD):", :], axis=0)
    table_data.loc["SPD speakers, relative use (in %)"] = (
        table_data.loc["SPD speakers", "Male words:": "Neutral words:"].div(
            table_data.loc["SPD speakers", "Total words:"]))

    # CDU
    table_data.loc["(CDU):"] = table_data.loc[table_data["Party of speaker:"] == "(CDU):",
                                              ["Male words:", "Female words:", "Neutral words:",
                                               "Total words:"]].sum()
    table_data.loc["(CSU):"] = table_data.loc[table_data["Party of speaker:"] == "(CSU):",
                                              ["Male words:", "Female words:", "Neutral words:",
                                               "Total words:"]].sum()
    table_data.loc["(CDU und CSU):"] = table_data.loc[table_data["Party of speaker:"] == "(CDU und CSU):",
                                                      ["Male words:", "Female words:", "Neutral words:",
                                                       "Total words:"]].sum()
    table_data.loc["(CDU/CSU):"] = table_data.loc[table_data["Party of speaker:"] == "(CDU/CSU):",
                                                  ["Male words:", "Female words:", "Neutral words:",
                                                   "Total words:"]].sum()
    table_data.loc["(BP):"] = table_data.loc[table_data["Party of speaker:"] == "(BP):",
                                             ["Male words:", "Female words:", "Neutral words:",
                                              "Total words:"]].sum()
    table_data.loc["CDU"] = table_data.loc[table_data["Party of speaker:"] == "CDU",
                                           ["Male words:", "Female words:", "Neutral words:", "Total words:"]].sum()
    table_data.loc["CSU"] = table_data.loc[table_data["Party of speaker:"] == "CSU",
                                           ["Male words:", "Female words:", "Neutral words:", "Total words:"]].sum()
    table_data.loc["CDU und CSU"] = table_data.loc[table_data["Party of speaker:"] == "CDU und CSU",
                                                   ["Male words:", "Female words:", "Neutral words:",
                                                    "Total words:"]].sum()
    table_data.loc["CDU/CSU"] = table_data.loc[table_data["Party of speaker:"] == "CDU/CSU",
                                               ["Male words:", "Female words:", "Neutral words:", "Total words:"]].sum()
    table_data.loc["BP"] = table_data.loc[table_data["Party of speaker:"] == "BP",
                                          ["Male words:", "Female words:", "Neutral words:", "Total words:"]].sum()
    table_data.loc["CDU speakers"] = np.sum(table_data.loc["(CDU):": "BP", :], axis=0)
    table_data.loc["CDU speakers, relative use (in %)"] = (
        table_data.loc["CDU speakers", "Male words:": "Neutral words:"].div(
            table_data.loc["CDU speakers", "Total words:"]))

    # BÜNDNIS 90/DIE GRÜNEN
    table_data.loc["GRÜNEN):"] = table_data.loc[table_data["Party of speaker:"] == "GRÜNEN):",
                                                ["Male words:", "Female words:", "Neutral words:",
                                                 "Total words:"]].sum()
    table_data.loc["BÜNDNIS 90/DIE GRÜNEN"] = table_data.loc[table_data["Party of speaker:"] == "BÜNDNIS",
                                                             ["Male words:", "Female words:", "Neutral words:",
                                                              "Total words:"]].sum()
    table_data.loc["Grünen speakers"] = np.sum(table_data.loc["GRÜNEN):": "BÜNDNIS 90/DIE GRÜNEN", :],
                                               axis=0)
    table_data.loc["DIE GRÜNEN speakers, relative use (in %)"] = (table_data.loc["Grünen speakers", "Male words:":
                                                                                                    "Neutral words:"].div(
        table_data.loc["Grünen speakers", "Total words:"]))

    # Die Linke
    table_data.loc["LINKE):"] = table_data.loc[table_data["Party of speaker:"] == "LINKE):",
                                               ["Male words:", "Female words:", "Neutral words:",
                                                "Total words:"]].sum()
    table_data.loc["(PDS):"] = table_data.loc[table_data["Party of speaker:"] == "(PDS):",
                                              ["Male words:", "Female words:", "Neutral words:",
                                               "Total words:"]].sum()
    table_data.loc["DIE LINKE"] = table_data.loc[table_data["Party of speaker:"] == "DIE",
                                                 ["Male words:", "Female words:", "Neutral words:",
                                                  "Total words:"]].sum()
    table_data.loc["Linke speakers"] = np.sum(table_data.loc["LINKE):": "DIE LINKE", :],
                                              axis=0)
    table_data.loc["DIE LINKE speakers, relative use (in %)"] = (table_data.loc["Linke speakers", "Male words:":
                                                                                                  "Neutral words:"].div(
        table_data.loc["Linke speakers", "Total words:"]))

    # AfD
    table_data.loc["(AfD):"] = table_data.loc[table_data["Party of speaker:"] == "(AfD):",
                                              ["Male words:", "Female words:", "Neutral words:",
                                               "Total words:"]].sum()
    table_data.loc["AfD"] = table_data.loc[table_data["Party of speaker:"] == "AfD",
                                           ["Male words:", "Female words:", "Neutral words:",
                                            "Total words:"]].sum()
    table_data.loc["AfD speakers"] = np.sum(table_data.loc["(AfD):": "AfD", :], axis=0)
    table_data.loc["AfD speakers, relative use (in %)"] = (table_data.loc["AfD speakers", "Male words:":
                                                                                          "Neutral words:"].div(
        table_data.loc["AfD speakers", "Total words:"]))

    # FDP
    table_data.loc["(FDP):"] = table_data.loc[table_data["Party of speaker:"] == "(FDP):",
                                              ["Male words:", "Female words:", "Neutral words:",
                                               "Total words:"]].sum()
    table_data.loc["(F D P ):"] = table_data.loc[table_data["Party of speaker:"] == "(F D P ):",
                                                 ["Male words:", "Female words:", "Neutral words:",
                                                  "Total words:"]].sum()
    table_data.loc["FDP"] = table_data.loc[table_data["Party of speaker:"] == "FDP",
                                           ["Male words:", "Female words:", "Neutral words:",
                                            "Total words:"]].sum()
    table_data.loc["F D P "] = table_data.loc[table_data["Party of speaker:"] == "F D P ",
                                              ["Male words:", "Female words:", "Neutral words:",
                                               "Total words:"]].sum()
    table_data.loc["FDP speakers"] = np.sum(table_data.loc["(FDP):": "F D P ", :],
                                            axis=0)
    table_data.loc["FDP speakers, relative use (in %)"] = (table_data.loc["FDP speakers", "Male words:":
                                                                                          "Neutral words:"].div(
        table_data.loc["FDP speakers", "Total words:"]))

    # reduziert Tabelle auf essenzielle Zeilen und Spalten
    table_data_barchart_parties = table_data.loc["SPD": "FDP speakers, relative use (in %)",
                                  "Male words:": "Total words:"]
    with open("Daten für Barchart Partei.csv", "w", encoding="utf8") as outfile:
        table_data_barchart_parties.to_csv(outfile, sep=",")
    return table_data_barchart_parties


# erstellt Balkendiagramm
def make_barchart_parties(table_data_barchart_parties):
    # legt Grundsätzliches fest: Stil, Titel und Achsenbeschriftung
    bar_chart = pygal.Bar(style=custom_style, legend_at_bottom=True)
    # # entkommentieren für Diagrammtitel
    # bar_chart.title = "Verwendung verschiedener Substantive in Abhängigkeit zu Parteizugehörigkeit"
    bar_chart.y_title = "Relative Häufigkeit (in %)"
    bar_chart.x_labels = ("Männliche Substantive", "Weibliche Substantive", "Neutrale Substantive")

    # Daten aus Tabelle für jede Partei/Fraktion in line chart einpflegen
    bar_chart.add("DIE LINKE", [table_data_barchart_parties.loc["DIE LINKE speakers, relative use (in %)",
                                                                "Male words:"],
                                table_data_barchart_parties.loc["DIE LINKE speakers, relative use (in %)",
                                                                "Female words:"],
                                table_data_barchart_parties.loc["DIE LINKE speakers, relative use (in %)",
                                                                "Neutral words:"]])

    bar_chart.add("SPD", [table_data_barchart_parties.loc["SPD speakers, relative use (in %)", "Male words:"],
                          table_data_barchart_parties.loc["SPD speakers, relative use (in %)", "Female words:"],
                          table_data_barchart_parties.loc["SPD speakers, relative use (in %)", "Neutral words:"]])

    bar_chart.add("DIE GRÜNEN", [table_data_barchart_parties.loc["DIE GRÜNEN speakers, relative use (in %)",
                                                                 "Male words:"],
                                 table_data_barchart_parties.loc[
                                     "DIE GRÜNEN speakers, relative use (in %)", "Female words:"],
                                 table_data_barchart_parties.loc[
                                     "DIE GRÜNEN speakers, relative use (in %)", "Neutral words:"]])

    bar_chart.add("CDU/CSU", [table_data_barchart_parties.loc["CDU speakers, relative use (in %)", "Male words:"],
                              table_data_barchart_parties.loc["CDU speakers, relative use (in %)", "Female words:"],
                              table_data_barchart_parties.loc["SPD speakers, relative use (in %)", "Neutral words:"]])

    bar_chart.add("FDP", [table_data_barchart_parties.loc["FDP speakers, relative use (in %)", "Male words:"],
                          table_data_barchart_parties.loc["FDP speakers, relative use (in %)", "Female words:"],
                          table_data_barchart_parties.loc["FDP speakers, relative use (in %)", "Neutral words:"]])

    bar_chart.add("AfD", [table_data_barchart_parties.loc["AfD speakers, relative use (in %)", "Male words:"],
                          table_data_barchart_parties.loc["AfD speakers, relative use (in %)", "Female words:"],
                          table_data_barchart_parties.loc["AfD speakers, relative use (in %)", "Neutral words:"]])

    # speichert Diagramm als .svg-Datei
    bar_chart.render_to_file("Distribution-MFN-words-Party.svg")


def main():
    # leeres Dictionary anlegen
    speeches_data = {}

    # Listen einlesen
    female_MPs = read_list("Female_MPs.txt")
    parties = read_list("Parties.txt")
    male_words = read_list("Male_Words.txt")
    female_words = read_list("Female_Words.txt")
    neutral_words = read_list("Neutral_Words.txt")
    parties_for_soup = read_list("Parties_for_Soup.txt")

    for textfile in filename_list:
        # markiert Periode des Textes
        text_period_beginning = "Anfang Periode " + basename(textfile).split(".xml")[0][0:2]

        # baut Einträge in Dictionary ein, die später als Orientierung und zum Slicing des DataFrames dienen
        speeches_data[text_period_beginning] = {"Gender of speaker:": 0, "Party of speaker:": 0, "Male words:":
            0, "Female words:": 0, "Neutral words:": 0, "Total words:": 0}
        text = read_textfile(textfile)
        cleaned_text = clean_texts(text)

        # ruft Liste mit Positionsangaben der Parteinamen auf
        split_at_place = split_text_new_speaker(cleaned_text)

        # Laufvariable initialisieren
        i = 0

        while i < len(split_at_place):
            # single_speaker_text ist Redebeitrag einzelner Person beginnend mit deren Namen (ab Zeilenumbruch) bis
            # zum nächsten Redebeitrag
            single_speaker_text = find_start_of_line(cleaned_text, split_at_place, i)

            # führt Index ein, bei dem jeder Textabschnitt nummeriert wird für spätere Überführung in Data Frame
            text_file_name = basename(textfile).split(".xml")[0] + "-" + str(i + 1)
            if single_speaker_text is not None:
                word_dict = create_dictionary(parties, female_MPs, male_words, female_words, neutral_words,
                                              single_speaker_text)
                # für jeden einzelnen Redetext wird eine Tabellenspalte erstellt und dem Redetext über Index zugeordnet
                speeches_data[text_file_name] = word_dict
            i += 1

    for file in filename_list_period_19:
        text = read_textfile(file)
        text_cleaned = clean_texts(text)

        # SoupObject erstellen aus bereinigtem Text mit XML-Parser
        soup = BeautifulSoup(text_cleaned, 'lxml')

        # SoupObject durchsuchen nach Tag <rede>
        soup_single_speeches = soup.find_all("rede")
        i = 0

        text_period_beginning = "Anfang Periode " + basename(file).split(".xml")[0][0:2]
        # baut Eintrag in Dictionary ein, der später als Orientierung und zum Slicing des DataFrames dient
        speeches_data[text_period_beginning] = {"Gender of speaker:": 0, "Party of speaker:": 0, "Male words:": 0,
                                                "Female words:": 0, "Neutral words:": 0, "Total words:": 0}
        while i < len(soup_single_speeches):
            analyse = extract_info_from_soup(soup_single_speeches[i])
            word_dict = create_dictionary_from_soup(parties_for_soup, female_MPs, male_words, female_words,
                                                    neutral_words, analyse)
            # führt Index ein, bei dem jeder Textabschnitt nummeriert wird für spätere Überführung in Data Frame
            text_file_name = basename(file).split(".xml")[0] + "-" + str(i + 1)
            speeches_data[text_file_name] = word_dict
            i += 1
    speeches_data["ENDE"] = {"Gender of speaker:": 0, "Party of speaker:": 0, "Male words:": 0, "Female words:": 0,
                             "Neutral words:": 0, "Total words:": 0}

    save_dictionary_as_df(speeches_data)
    csv_doc = read_table()
    total_numbers_per_period = calculations_for_lineplot(csv_doc)
    make_lineplot_words_used(total_numbers_per_period)
    gender_distribution = calculations_for_barchart_speakers(csv_doc)
    make_barchart_speakers(gender_distribution)
    party_distribution = calculations_for_bar_chart_parties(csv_doc)
    make_barchart_parties(party_distribution)


filename_list = glob.glob("Periode_*/*.xml")
filename_list_period_19 = glob.glob("Periode19/*.xml")

if __name__ == "__main__":
    main()
