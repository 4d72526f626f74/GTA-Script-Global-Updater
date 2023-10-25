from __future__ import annotations
from typing import NoReturn, List, Dict, Tuple, TYPE_CHECKING
from src.signature import Signature
from src.sigmaker import SigMaker
from colorama import Fore, init
from concurrent.futures import ProcessPoolExecutor

if TYPE_CHECKING:
    from concurrent.futures import Future

init()

import mmap
import re
import os

class Updater(object):
    def __init__(self, new: str, old: str) -> NoReturn:
        self.new: str = ''
        self.old: str = ''
        self._sigs: List[Signature] = []
        
        with open(new, 'rb') as fp:
            with mmap.mmap(fp.fileno(), 0, access=mmap.ACCESS_READ) as m:
                self.new = m.read().decode()
                m.close()
            fp.close()
            
        with open(old, 'rb') as fp:
            with mmap.mmap(fp.fileno(), 0, access=mmap.ACCESS_READ) as m:
                self.old = m.read().decode()
                m.close()
            fp.close()
        
    def __repr__(self) -> str:
        return f'Updater()'
    
    def load_globals(self, file: str) -> List[str]:
        globals: List[str] = []
        
        with open(file, 'r') as fp:
            for line in fp.readlines():
                globals.append(line.strip())
            fp.close()
        return globals
    
    @property
    def sigs(self) -> List[Signature]:
        return self._sigs
    
    @sigs.setter
    def sigs(self, value: List[Signature]) -> NoReturn:
        self._sigs = value
        
    @sigs.deleter
    def sigs(self) -> NoReturn:
        del self._sigs
        self._sigs = []
        
    def search(self, globals_file: str, padding: int, sigs_amount: int, unique: bool = False) -> NoReturn:
        globals = self.load_globals(globals_file)
        sigs: Dict[str, List[Signature]] = {}
        found: bool = False
        pattern: re.Pattern = re.compile(r'Global_')
        futures: List[Future] = []
        longest_global: str = max(globals, key=len)
        
        with ProcessPoolExecutor() as executor:
            for (i, global_) in enumerate(globals):
                futures.append(executor.submit(SigMaker.create_signatures, self.old, global_, padding, sigs_amount, unique))
                
        for future in futures:
            if future.done():
                try:
                    result: Tuple[str, List[Signature]] = future.result(5)
                    sigs[result[0]] = result[1]
                except Exception as err:
                    pass
                
        os.system('cls')

        for (key, value) in sigs.items():
            sig: Signature = None
            for (i, sig) in enumerate(value):
                if found:
                    found = False
                    break
                for j in range(len(self.new)):
                    if self.new[j] == sig.sig[0]:
                        for k in range(len(sig.sig)):
                            if self.new[j+k] != sig.sig[k] and sig.mask[k] != '?':
                                break
                            else:
                                continue
                        else:
                            code: str = self.new[j:j+len(sig.sig)]    
                            matches: List[str] = []
                            for match in pattern.finditer(code):
                                span: Tuple[int, int] = match.span()
                                g: str = code[span[0]:span[1]+len(key)-len('Global_')].replace('\n', '')
                                matches.append(g) 
                                lineno: int = self.new.count('\n', 0, j) + 3  
                            print(f'{Fore.RED}{key:<{len(longest_global)}}{Fore.RESET} {Fore.GREEN}->{Fore.RESET} {Fore.GREEN}{matches[0]} (line: {lineno}){Fore.RESET}')
                            found = True
                            break
                    else:
                        continue