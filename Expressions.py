from dataclasses import dataclass

class Exp:
    pass

@dataclass
class IdExp(Exp):
    name:str

@dataclass
class CallExp(Exp):
    func: IdExp 
    args: list[Exp]

@dataclass
class IntLiteral(Exp):
    value: int

@dataclass
class BooleanLiteral(Exp):
    value: bool