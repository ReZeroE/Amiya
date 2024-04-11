
from tabulate import tabulate
from amiya.automation_handler.actions_controller.units.sequence import ActionsSequence

class ActionsViewer:
    @staticmethod
    def tabulate_sequence(sequence: ActionsSequence, tablefmt) -> str:
        table = [[sequence.sequence_name, sequence.date_created, sequence.other_data, len(sequence.actions)]]
        headers = ["Name", "Date Created", "Other Data", "Actions Count"]
        return tabulate(table, headers, tablefmt=tablefmt)
    
    @staticmethod
    def tabulate_multi_sequences(sequence_list: list[ActionsSequence], tablefmt) -> str:
        table = [[seq.sequence_name, seq.date_created, seq.other_data, len(seq.actions)] for seq in sequence_list]
        table = sorted(table, key=lambda x: x[1]) # Sort by date created (not sure if this will have to be changed to IDs later)
        headers = ["Name", "Date Created", "Other Data", "Actions Count"]
        return tabulate(table, headers, tablefmt=tablefmt)
    
