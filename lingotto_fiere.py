class LingottoFiere:
    def __init__(self, nome):
        """Inizializza gli attributi e le strutture dati"""
        self._nome = nome
        self.stands = {}       # codice stand -> oggetto Stand
        self.espositori = {}   # codice espositore -> oggetto Espositore

    """Aggiungere setter e getter se necessari"""
    @property
    def nome(self):
        return self._nome

    @nome.setter
    def nome(self, nuovo_nome):
        self._nome = nuovo_nome

    def carica_file_dati(self, file_path):
        """Carica i dati (stand ed espositori) dal file"""
        nuovi_stand = {}
        nuovi_espositori = {}

        with open(file_path, "r", encoding="utf-8") as f:   # se manca: FileNotFoundError
            for riga in f:
                riga = riga.strip()
                if not riga:
                    continue
                campi = [c.strip() for c in riga.split(",")]
                codice = campi[0]

                if codice.startswith("ST"):
                    superficie = int(campi[1])
                    padiglione = int(campi[2])
                    prezzo_base = float(campi[3])
                    if len(campi) == 4:
                        stand = Stand(codice, superficie, padiglione, prezzo_base)
                    else:
                        extra = campi[4]
                        if extra.isdigit():
                            stand = StandPrese(codice, superficie, padiglione,
                                               prezzo_base, int(extra))
                        else:
                            stand = StandPremium(codice, superficie, padiglione,
                                                 prezzo_base, extra)
                    nuovi_stand[codice] = stand

                elif codice.startswith("ES"):
                    nuovi_espositori[codice] = Espositore(codice, campi[1], campi[2])

        self.stands = nuovi_stand
        self.espositori = nuovi_espositori
    def assegna_stand_a_espositore(self, codice_stand, codice_espositore):
        """Associa uno stand a un espositore"""
        if codice_stand not in self.stands:
            raise ValueError(f"Lo stand {codice_stand} non esiste")
        if codice_espositore not in self.espositori:
            raise ValueError(f"L'espositore {codice_espositore} non esiste")

        stand = self.stands[codice_stand]
        espositore = self.espositori[codice_espositore]

        if not stand.disponibile:
            raise ValueError(f"Lo stand {codice_stand} non è disponibile")
        if espositore.stand is not None:
            raise ValueError(f"L'espositore {codice_espositore} ha già lo stand "
                             f"{espositore.stand.codice}")

        stand.disponibile = False
        stand.espositore = espositore
        espositore.stand = stand

    def elenca_espositori(self):
        """Stampa l'elenco degli espositori mostrando, per ognuno, lo stand a cui è associato, quando applicabile """
        for espositore in self.espositori.values():
            print(espositore)

    def stand_ordinati_per_prezzo(self):
        """Restituisce la lista ordinata degli stand in base al prezzo"""
        return sorted(self.stands.values())
