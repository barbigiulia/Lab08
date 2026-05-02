import flet as ft

from model.nerc import Nerc


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._idMap = {}
        self.fillIDMap()

    # BOTTONE
    def handleWorstCase(self, e):
        self._view.txt_result.controls.clear()

        # RECUPERO L'INPUT DELL'UTENTE DAL VIEW
        nerc_value = self._view._ddNerc.value
        try:
            maxYears = int (self._view._txtYears.value)
            maxHours = int(self._view._txtHours.value)
        except:
            self._view.create_alert("Inserisci numeri validi")
            return

        # OGGETTO "Nerc" : (id: int, value: str)
        nerc = self._idMap[nerc_value]

        soluzione = self._model.worstCase(nerc, maxYears, maxHours)
        # stampo risultato
        self._view.txt_result.controls.append(ft.Text(
                f"Clienti totali: {self._model.totalCustomers(soluzione)}"))

        self._view.txt_result.controls.append(ft.Text(
            f"Ore totali: {self._model.totalHours(soluzione)}"))
        for e in soluzione:
            self._view.txt_result.controls.append(ft.Text(str(e)))
        self._view.update_page()




    def fillDD(self):  # CREA LA LISTA DEI NOMI DEL MENU A TENDINA --> NERC
        nercList = self._model.listNerc
        for n in nercList:
            self._view._ddNerc.options.append(ft.dropdown.Option(text=n.value))
        self._view.update_page()


    def fillIDMap(self):
        # Da Dbeaver arriva [
        #     Nerc(1, "WECC"),
        #     Nerc(2, "RFC"),
        #     Nerc(3, "SERC")
        # ]

        # Con questa funzione ottengo:
        #self._idMap = {
        #                "WECC": Nerc(1, "WECC"),
         #               "RFC": Nerc(2, "RFC"),
         #               "SERC": Nerc(3, "SERC")
          #          }
        values = self._model.listNerc   # lista di oggetti Nerc (id, str)
        for v in values:
            self._idMap[v.value] = v
