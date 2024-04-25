
from tabulate import tabulate
from amiya.automation_handler.units.sequence import AutomationSequence

class AutomationViewer:
    @staticmethod
    def tabulate_sequence(sequence: AutomationSequence, tablefmt) -> str:
        table = [[sequence.sequence_name, sequence.date_created, sequence.other_data, len(sequence.actions)]]
        headers = ["Name", "Time Created", "Other Data", "Actions Count"]
        return tabulate(table, headers, tablefmt=tablefmt)
    
    @staticmethod
    def tabulate_multi_sequences(sequence_list: list[AutomationSequence], tablefmt) -> str:
        table = [[seq.sequence_name, seq.date_created, seq.other_data, len(seq.actions)] for seq in sequence_list]
        table = sorted(table, key=lambda x: x[1]) # Sort by date created (not sure if this will have to be changed to IDs later)
        headers = ["Name", "Time Created", "Other Data", "Actions Count"]
        return tabulate(table, headers, tablefmt=tablefmt)
    
