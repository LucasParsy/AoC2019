from typing import List


class Machine:

    def __init__(self, inp: List[int], mem_str: str):
        self._input = inp
        self._mem = [int(x) for x in mem_str.split(',')]
        self._mem.extend([0] * 10000)
        self._counter = 0
        self._relative_base = 0
        self._output = []
        self._ended = False

    def ended(self) -> bool:
        return self._ended

    def add_input(self, n: int):
        self._input.append(n)

    def _add(self, a1, a2, pos):
        self._mem[pos] = a1 + a2

    def _mul(self, a1, a2, pos):
        self._mem[pos] = a1 * a2

    def _inp(self, a1):
        self._output = []
        val = self._input.pop(0)
        # val = int(input())
        self._mem[a1] = val

    def _out(self, a1):
        self._output.append(a1)
        # print(a1, file=self._file_output)

    def _nz(self, a1: int, a2: int) -> int:
        if a1 != 0:
            return a2

    def _ez(self,a1, a2) -> int:
        if a1 == 0:
            return a2

    def _lt(self, a1, a2, a3):
        self._mem[a3] = 1 if a1 < a2 else 0

    # def gt(mem: List[int], a1, a2, a3):
    #    mem[a3] = 1 if a1 > a2 else 0

    def _eq(self, a1, a2, a3):
        self._mem[a3] = 1 if a1 == a2 else 0

    def _rb(self, a1):
        self._relative_base += a1

    def _ex(self):
        self._ended = True
        # print("end program")
        # print("mem[0]:", mem[0])
        # exit()

    opcodes = {
        1: (_add,  [0, 0, 1]),
        2: (_mul,  [0, 0, 1]),
        3: (_inp,  [1]),
        4: (_out,  [0]),
        5: (_nz, [0, 0]),
        6: (_ez, [0, 0]),
        7: (_lt, [0, 0, 1]),
        8: (_eq, [0, 0, 1]),
        9: (_rb, [0]),
        99: ( _ex, []),
    }

    def step(self):
        op = self._mem[self._counter] % 100
        method = self.opcodes[op][0]
        if op == 3 and not self._input:
            #print("inputting without value...")
            self._input.append(-1)
            #return self._output

        mem_params = self.opcodes[op][1]
        num_params = len(mem_params)
        params = self._mem[self._counter + 1: self._counter + 1 + num_params]

        inst = str(self._mem[self._counter])
        modes_list = [int(x) for x in list(inst.zfill(num_params + 2)[:-2])]
        modes_list.reverse()
        for u in range(0, len(modes_list)):
            if modes_list[u] == 0 and mem_params[u] != 1:
                params[u] = self._mem[params[u]]
            elif modes_list[u] == 2:
                if mem_params[u] != 1:
                    params[u] = self._mem[params[u] + self._relative_base]
                else:
                    params[u] = params[u] + self._relative_base

        new_pos = method(self, *params)
        if isinstance(new_pos, int):
            self._counter = new_pos
        else:
            self._counter += num_params + 1

        if self._ended:
            self._ended = False
            return self._output

        return None

    def run(self) -> List[int]:
        self._output = []
        mem = self._mem
        while self._counter < len(mem):
            res = self.step()
            if res is not None:
                return res
