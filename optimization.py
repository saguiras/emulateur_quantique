
class  Optimization:

    def optimize(self):
        self.optimize_gate()
        self.remove_unused()
        self.optimize_connections()
        self.remove_unused()

    def optimize_gate(self):
        
        for idx, operation in enumerate(self.operations):
            continu = False
            if not operation[3]:
                for target in operation[1]:
                    for next_idx in range(idx + 1, len(self.operations)):
                        if target in self.operations[next_idx][1]:
                            if self.operations[next_idx][0] == operation[0]:
                                        self.operations[next_idx][1].remove(target)
                                        operation[1].remove(target)
                                        self.optimize_gate()
                                        return
                            else:
                                continu = True
                                break
                    if continu:
                        continue   

    def remove_unused(self):
        self.operations = [operation for operation in self.operations if operation[1]]

    def optimize_connections(self):
        for idx, operation in enumerate(self.operations):
            if not operation[3]:
                if idx < len(self.operations) - 1 and self.operations[idx + 1][0] == operation[0]:
                    for target in self.operations[idx + 1][1]:
                        if target not in operation[1]:
                            operation[1].append(target)
                            self.operations[idx + 1][1].remove(target)
                            self.optimize_connections()
                            return