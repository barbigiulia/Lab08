import copy

from database.DAO import DAO

# SCEGLIERE UN SOTTOINSIEME DI BLACKOUT CHE:
# ORE TOTALI <= Y
# RANGE ANNI <= X
# MASSIMIZZA I CLIENTI COINVOLTI
class Model:
    def __init__(self):
        self._solBest = []
        self._listNerc = None   # per il dropdrown
        self._listEvents = None  # eventi blackout caricati dal DB
        self.loadNerc()

    # =======CARICAMENTO DATI ==============================================
    def loadEvents(self, nerc):
        # carica la lista di oggetti "EVENT"
        # li filtra in base al nerc_id
        self._listEvents = DAO.getAllEvents(nerc)

    def loadNerc(self):
        self._listNerc = DAO.getAllNerc()   # per il menu a tendina (NERC)

    # =========================================================================

    def worstCase(self, nerc, maxY, maxH):
        # è LA FUNZIONE CHE PARTE QUANDO PREMO IL BOTTONE!
        # parametri: area scelta dall'utente (nerc), maxOre_tot, maxAnni_tot
        # 1) carica gli eventi del nerc scelto (nerc_id)
        # 2) inizia la ricorsione
        # 3) salva la soluzione migliore
        self._listEvents = self.loadEvents(nerc) # lista eventi
        # reset della miglior soluzione (ogni click riparte da zero)
        self._solBest = [ ]
        self.ricorsione([], maxY, maxH, 0)
        return self._solBest




    def ricorsione(self, parziale, maxY, maxH, pos):
        # parziale = lista di eventi scelti finora
        # pos = quale evento sto considerando
        # maxY = limite di ore max consentito
        # maxH = limite di anni
        # 1) passo al prox evento --> ricorsione (parziale, pos+1)
        # 2) prendo l'evento --> lo aggiungo, controllo vincoli e se valido continuo
        #    parziale +evento
        #    ricorsione(...)

        # mi fermo quando pos== numero di eventi (da esaminare)
        if pos == len(self._listEvents):
            # quando ho deciso su tutti gli eventi valuto la soluzione parziale!
            # ora controllo le oreTot, rangeAnni e clientiTot
            # se valido --> confronto con migliore
            if self.isValid(parziale, maxY, maxH):
                if self.totalCustormers(parziale) > self.totalCustomers(self._solBest):
                    self._solBest = copy.deepcopy(parziale)
            return
        # 1) RAMO : NON PRENDO L'EVENTO
        self.ricorsione(parziale, maxY, maxH, pos+1)  #aggiorno la posizione

        event = self._listEvents[pos]
        new_parziale = parziale + [event]

        # controllo se la scelta che ho fatto è ancora valida:
        if self.isValid(new_parziale, maxY, maxH):
            self.ricorsione(new_parziale, maxY, maxH, pos+1)

    def isValid(self, soluzione, maxY, maxH):
        # se non ci sono soluzione --> sempre valida
        if len(soluzione)== 0:
            return True
        total_hours = 0
        years = []

        for evento in soluzione:
            hours = (evento.date_event_finished - evento.date_event_began).total_seconds() /3600
            total_hours += hours
            years.append(evento.date_event_began.year)

        if total_hours > maxH:
            return False
        if ( max(years) - min(years)) > maxY:
            return False

        return True

    def totalCustomers(self, soluzione):
        total = 0
        for evento in soluzione:
            total += evento.customers_affected
        return total




        # property per UI
    @property
    def listNerc(self):
        return self._listNerc