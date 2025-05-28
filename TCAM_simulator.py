import heapq

class TCAMEntry:
    def __init__(self, pattern: str, value):
        self.pattern = pattern
        self.value = value

    def match(self, key: str):
        if len(self.pattern) != len(key):
            return False

        for p_char, k_char in zip(self.pattern, key):
            if p_char == "X":
                continue
            if p_char != k_char:
                return False
        return True

    def __str__(self):
        return f"Pattern: {self.pattern}, Value: {self.value}"


class TCAMSimulator:
    def __init__(self, width: int):
        self.width = width
        self.entries = []
        self._next_insertion_order = 0

    def _validate_pattern(self, pattern: str):
        if len(pattern) != self.width:
            raise ValueError(
                f"Pattern length ({len(pattern)}) must match TCAM width ({self.width})."
            )
        if not all(c in "01X" for c in pattern):
            raise ValueError("Pattern can only contain 0, 1, or X")

    def _validate_key(self, key: str):
        if len(key) != self.width:
            raise ValueError(
                f"Key length ({len(key)}) must match TCAM width ({self.width})."
            )
        if not all(c in "01" for c in key):
            raise ValueError("Search key can only contain 0 or 1")

    def write(self, pattern: str, value, priority: int = None):
        self._validate_pattern(pattern)
        entry_obj = TCAMEntry(pattern, value)

        current_priority = priority
        if current_priority is None:
            current_priority = float("inf")

        tie_breaker_id = self._next_insertion_order
        self._next_insertion_order += 1

        heap_item = [current_priority, tie_breaker_id, entry_obj]
        heapq.heappush(self.entries, heap_item)
        return tie_breaker_id

    def search(self, key: str):
        self._validate_key(key)

        matching_entries_data = []
        for entry_data in self.entries:
            tcam_entry_obj = entry_data[2]
            if tcam_entry_obj.match(key):
                matching_entries_data.append(entry_data)

        if not matching_entries_data:
            return None

        # Find the best match among those that matched (lowest priority value, then lowest tie_breaker)
        best_match_data = min(matching_entries_data, key=lambda x: (x[0], x[1]))
        return best_match_data[2].value

    def _find_entry_list_index(self, tie_breaker_id):
        for i, entry_data in enumerate(self.entries):
            if entry_data[1] == tie_breaker_id:
                return i
        return -1
    
    def edit_entry(self, tie_breaker_id: int, new_pattern=None, new_value=None):
        list_idx = self._find_entry_list_index(tie_breaker_id)
        
        if list_idx == -1:
            raise ValueError(f"Entry with tie_breaker_id {tie_breaker_id} not found.")

        entry_obj_to_edit = self.entries[list_idx][2]

        if new_pattern is not None:
            self._validate_pattern(new_pattern)
            entry_obj_to_edit.pattern = new_pattern
        
        if new_value is not None:
            entry_obj_to_edit.value = new_value

    def change_priority(self, tie_breaker_id: int, new_priority: int = None):
        list_idx = self._find_entry_list_index(tie_breaker_id)

        if list_idx == -1:
            raise ValueError(f"Entry with tie_breaker_id {tie_breaker_id} not found.")

        actual_new_priority = new_priority
        if actual_new_priority is None:
            actual_new_priority = float('inf')

        old_priority, original_tie_breaker, entry_obj = self.entries[list_idx]

        if list_idx == len(self.entries) - 1:
            self.entries.pop()
        else:
            self.entries[list_idx] = self.entries[-1]
            self.entries.pop() 
            heapq.heapify(self.entries)
        
        heapq.heappush(self.entries, [actual_new_priority, original_tie_breaker, entry_obj])


    def get_entry_details_by_id(self, tie_breaker_id: int):
        list_idx = self._find_entry_list_index(tie_breaker_id)
        if list_idx == -1:
            return None
        
        entry_data = self.entries[list_idx]
        priority_value = entry_data[0]
        display_priority = priority_value if priority_value != float('inf') else "Default (Lowest)"
        
        return {
            "priority_value": priority_value,
            "display_priority": display_priority,
            "tie_breaker_id": entry_data[1],
            "pattern": entry_data[2].pattern,
            "value": entry_data[2].value,
        }

    def get_all_entries_sorted(self):
        return sorted(self.entries, key=lambda x: (x[0], x[1]))
    
    def delete_entry(self, tie_breaker_id: int):
        list_idx = self._find_entry_list_index(tie_breaker_id)

        if list_idx == len(self.entries) - 1:
            self.entries.pop()
        else:
            self.entries[list_idx] = self.entries[-1]
            self.entries.pop()
            heapq.heapify(self.entries)
        
        return True


    def __str__(self):
        output_str = [f"TCAM (Width: {self.width}):"]
        sorted_entries_view = self.get_all_entries_sorted()
        for i, entry_data in enumerate(sorted_entries_view):
            priority_val = entry_data[0]
            tie_breaker = entry_data[1]
            tcam_entry_obj = entry_data[2]
            
            display_priority = priority_val if priority_val != float('inf') else "Default (Lowest)"
            
            output_str.append(f"Priority Value: {str(display_priority)}, ID: {tie_breaker}), Entry: {str(tcam_entry_obj)}")
        return "\n".join(output_str)


if __name__ == "__main__":
    tcam = TCAMSimulator(width=8)

    A = tcam.write(pattern="1010XXXX", value="A", priority=10)
    B = tcam.write(pattern="10100011", value="B")
    C = tcam.write(pattern="XX00110X", value="C", priority=5)
    D = tcam.write(pattern="XX0011XX", value="D", priority=1)
    E = tcam.write(pattern="11110000", value="E")

    search_keys = [
        "10100000",
        "10100011",
        "00001100",
        "11110000",
        "01010101",
        # "1010101X",
    ]

    for key in search_keys:
        result = tcam.search(key)
        if result is not None:
            print(f"Match found! Value: {result}")
        else:
            print(f"No match found.")

    tcam.edit_entry(A, new_pattern="XX11XX00", new_value="New A")
    tcam.change_priority(E, new_priority=0)
    tcam.delete_entry(C)

    for key in search_keys:
        result = tcam.search(key)
        if result is not None:
            print(f"Match found! Value: {result}")
        else:
            print(f"No match found.")
    print(tcam)