from __future__ import annotations
from typing import NoReturn
from colorama import Fore, init
init()

class Signature(object):
    def __init__(self, sig: str, mask: str) -> NoReturn:
        self.sig: str = sig
        self.mask: str = mask
        
    def __repr__(self) -> str:
        sig_as_hex = self.sig.encode().hex()
        sig_as_hex = ' '.join([sig_as_hex[i:i+2] for i in range(0, len(sig_as_hex), 2)]).upper()
        return f'Signature(sig={sig_as_hex} mask={self.mask})'
    
    @property
    def hex(self) -> str:
        hexa: str = f'{" ".join([self.sig.encode().hex().upper()[i:i+2] for i in range(0, len(self.sig), 2)])}'
        return f'{Fore.YELLOW}{hexa}{Fore.RESET}'