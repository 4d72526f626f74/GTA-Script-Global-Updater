from __future__ import annotations
from src.signature import Signature
from typing import List, Tuple, NoReturn, Dict
from colorama import Fore, init

init()

import re

class SigMaker:
    @staticmethod
    def create_signatures(data: str, sample: str, padding: int = 8, sigs_amount: int = 20, unique: bool = False) -> Tuple[str, List[Signature]]:
        sigs: List[Signature] = []
        pattern: re.Pattern = re.compile(re.escape(sample.strip()))
        hex_pattern: re.Pattern = re.compile(r'0x[0-9A-Fa-f]{2,10}')
        num_pattern: re.Pattern = re.compile(r'\d')
        tested: List[str] = []
        
        for match in pattern.finditer(data):
            span: Tuple[int, int] = match.span()
            sig: str = data[span[0]-padding:span[1]+padding]
            mask: str = sig
            
            has_brackets: bool = sig.find('[') != -1 and sig.find(']') != -1
            bit_manipulation: bool = mask.find('BIT') != -1
            
            if has_brackets:
                bracket_start: int = sig.find('[') + 1
                bracket_end: int = sig.find(']')
                data_length: int = bracket_end - bracket_start
                mask = sig[:bracket_start] + '?'*data_length + sig[bracket_end:]
                
            mask = re.sub(r'Global_\d{2}', 'Global_xx', mask)
            for match in hex_pattern.finditer(sig): mask = re.sub(match.group(), '?'*len(match.group()), mask)
            
            if bit_manipulation:
                bit: re.Match = re.search(r',\s\d{1,2}', mask)
                if bit:
                    mask = re.sub(bit.group(), ', xx', mask)
                    
            for match in num_pattern.finditer(sig): mask = re.sub(match.group(), '?', mask)
            mask = re.sub('[^?]', 'x', mask)
            hex_sig: str = ' '.join([sig.encode().hex()[i:i+2] for i in range(0, len(sig), 2)]).upper()
            
            if len(sig) == len(mask):
                if hex_sig in tested:
                    continue
                else:
                    tested.append(hex_sig)
                if len(sigs) >= sigs_amount:
                    break
                if not unique:
                    sigs.append(Signature(sig, mask))
                    print(f'{Fore.GREEN}[+]{Fore.RESET} Found signature for {Fore.RED}{sample}{Fore.RESET}')
                else:
                    if SigMaker.check_unique(sig, mask, data):
                        sigs.append(Signature(sig, mask))
                        print(f'{Fore.GREEN}[+]{Fore.RESET} Found signature for {Fore.RED}{sample}{Fore.RESET}')
        return (sample, sigs)
    
    @staticmethod
    def check_unique(sig: str, mask: str, data: str) -> bool:
        matches: int = 0
        for i in range(len(data)):
            if data[i] == sig[0]:
                for j in range(len(sig)):
                    try:
                        if data[i+j] != sig[j] and mask[j] != '?':
                            break
                        else:
                            continue
                    except IndexError:
                        break
                else:
                    matches += 1
                    
        if matches == 1:
            return True
        else:
            return False