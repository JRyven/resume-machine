from typing import Any, Dict, List
import copy


class Composer:
    """Simple, testable composer that merges a base resume dict with fragments.

    Merge rules:
    - dict + dict => deep merge
    - list + list => extend
    - scalar or type-mismatch => override with fragment value
    """

    def __init__(self) -> None:
        pass

    def merge(self, base: Dict[str, Any], fragments: List[Dict[str, Any]]) -> Dict[str, Any]:
        result = copy.deepcopy(base) if base is not None else {}
        for frag in fragments or []:
            self._merge_dict(result, frag)
        return result

    def _merge_dict(self, dst: Dict[str, Any], src: Dict[str, Any]) -> None:
        for k, v in src.items():
            if k in dst:
                if isinstance(dst[k], dict) and isinstance(v, dict):
                    self._merge_dict(dst[k], v)
                elif isinstance(dst[k], list) and isinstance(v, list):
                    dst[k].extend(copy.deepcopy(v))
                else:
                    dst[k] = copy.deepcopy(v)
            else:
                dst[k] = copy.deepcopy(v)
