#!/usr/bin/env python3
"""
Specific keyboard layout definitions for RelayKeys.

This module contains detailed character mappings for various keyboard layouts,
including special characters, diacritics, and language-specific symbols.
"""

from typing import Dict, List


def get_french_azerty_layout() -> Dict[str, List]:
    """
    French AZERTY keyboard layout.
    Based on the standard French keyboard layout used in France.
    """
    return {
        # Control characters
        "\r": [None, None],
        "\t": ["TAB", []],
        " ": ["SPACE", []],
        "\n": ["ENTER", []],
        
        # Numbers row (unshifted)
        "²": ["BACKQUOTE", []],
        "&": ["1", []],
        "é": ["2", []],
        "\"": ["3", []],
        "'": ["4", []],
        "(": ["5", []],
        "-": ["6", []],
        "è": ["7", []],
        "_": ["8", []],
        "ç": ["9", []],
        "à": ["0", []],
        ")": ["MINUS", []],
        "=": ["EQUALS", []],
        
        # Numbers row (shifted)
        "³": ["BACKQUOTE", ["LSHIFT"]],
        "1": ["1", ["LSHIFT"]],
        "2": ["2", ["LSHIFT"]],
        "3": ["3", ["LSHIFT"]],
        "4": ["4", ["LSHIFT"]],
        "5": ["5", ["LSHIFT"]],
        "6": ["6", ["LSHIFT"]],
        "7": ["7", ["LSHIFT"]],
        "8": ["8", ["LSHIFT"]],
        "9": ["9", ["LSHIFT"]],
        "0": ["0", ["LSHIFT"]],
        "°": ["MINUS", ["LSHIFT"]],
        "+": ["EQUALS", ["LSHIFT"]],
        
        # Top row (unshifted)
        "a": ["Q", []],
        "z": ["W", []],
        "e": ["E", []],
        "r": ["R", []],
        "t": ["T", []],
        "y": ["Y", []],
        "u": ["U", []],
        "i": ["I", []],
        "o": ["O", []],
        "p": ["P", []],
        "^": ["LEFTBRACKET", []],
        "$": ["RIGHTBRACKET", []],
        
        # Top row (shifted)
        "A": ["Q", ["LSHIFT"]],
        "Z": ["W", ["LSHIFT"]],
        "E": ["E", ["LSHIFT"]],
        "R": ["R", ["LSHIFT"]],
        "T": ["T", ["LSHIFT"]],
        "Y": ["Y", ["LSHIFT"]],
        "U": ["U", ["LSHIFT"]],
        "I": ["I", ["LSHIFT"]],
        "O": ["O", ["LSHIFT"]],
        "P": ["P", ["LSHIFT"]],
        "¨": ["LEFTBRACKET", ["LSHIFT"]],
        "£": ["RIGHTBRACKET", ["LSHIFT"]],
        "*": ["BACKSLASH", []],
        "µ": ["BACKSLASH", ["LSHIFT"]],
        
        # Home row (unshifted)
        "q": ["A", []],
        "s": ["S", []],
        "d": ["D", []],
        "f": ["F", []],
        "g": ["G", []],
        "h": ["H", []],
        "j": ["J", []],
        "k": ["K", []],
        "l": ["L", []],
        "m": ["SEMICOLON", []],
        "ù": ["QUOTE", []],
        
        # Home row (shifted)
        "Q": ["A", ["LSHIFT"]],
        "S": ["S", ["LSHIFT"]],
        "D": ["D", ["LSHIFT"]],
        "F": ["F", ["LSHIFT"]],
        "G": ["G", ["LSHIFT"]],
        "H": ["H", ["LSHIFT"]],
        "J": ["J", ["LSHIFT"]],
        "K": ["K", ["LSHIFT"]],
        "L": ["L", ["LSHIFT"]],
        "M": ["SEMICOLON", ["LSHIFT"]],
        "%": ["QUOTE", ["LSHIFT"]],
        
        # Bottom row (unshifted)
        "<": ["NON-US-BACKSLASH", []],
        "w": ["Z", []],
        "x": ["X", []],
        "c": ["C", []],
        "v": ["V", []],
        "b": ["B", []],
        "n": ["N", []],
        ",": ["M", []],
        ";": ["COMMA", []],
        ":": ["PERIOD", []],
        "!": ["SLASH", []],
        
        # Bottom row (shifted)
        ">": ["NON-US-BACKSLASH", ["LSHIFT"]],
        "W": ["Z", ["LSHIFT"]],
        "X": ["X", ["LSHIFT"]],
        "C": ["C", ["LSHIFT"]],
        "V": ["V", ["LSHIFT"]],
        "B": ["B", ["LSHIFT"]],
        "N": ["N", ["LSHIFT"]],
        "?": ["M", ["LSHIFT"]],
        ".": ["COMMA", ["LSHIFT"]],
        "/": ["PERIOD", ["LSHIFT"]],
        "§": ["SLASH", ["LSHIFT"]],
        
        # AltGr combinations (common ones)
        "~": ["2", ["RALT"]],
        "#": ["3", ["RALT"]],
        "{": ["4", ["RALT"]],
        "[": ["5", ["RALT"]],
        "|": ["6", ["RALT"]],
        "`": ["7", ["RALT"]],
        "\\": ["8", ["RALT"]],
        "^": ["9", ["RALT"]],
        "@": ["0", ["RALT"]],
        "]": ["MINUS", ["RALT"]],
        "}": ["EQUALS", ["RALT"]],
        "€": ["E", ["RALT"]],
        "¤": ["RIGHTBRACKET", ["RALT"]],
    }


def get_spanish_qwerty_layout() -> Dict[str, List]:
    """
    Spanish QWERTY keyboard layout.
    Based on the standard Spanish keyboard layout used in Spain.
    """
    return {
        # Control characters
        "\r": [None, None],
        "\t": ["TAB", []],
        " ": ["SPACE", []],
        "\n": ["ENTER", []],
        
        # Numbers row (unshifted)
        "º": ["BACKQUOTE", []],
        "1": ["1", []],
        "2": ["2", []],
        "3": ["3", []],
        "4": ["4", []],
        "5": ["5", []],
        "6": ["6", []],
        "7": ["7", []],
        "8": ["8", []],
        "9": ["9", []],
        "0": ["0", []],
        "'": ["MINUS", []],
        "¡": ["EQUALS", []],
        
        # Numbers row (shifted)
        "ª": ["BACKQUOTE", ["LSHIFT"]],
        "!": ["1", ["LSHIFT"]],
        "\"": ["2", ["LSHIFT"]],
        "·": ["3", ["LSHIFT"]],
        "$": ["4", ["LSHIFT"]],
        "%": ["5", ["LSHIFT"]],
        "&": ["6", ["LSHIFT"]],
        "/": ["7", ["LSHIFT"]],
        "(": ["8", ["LSHIFT"]],
        ")": ["9", ["LSHIFT"]],
        "=": ["0", ["LSHIFT"]],
        "?": ["MINUS", ["LSHIFT"]],
        "¿": ["EQUALS", ["LSHIFT"]],
        
        # Top row (unshifted)
        "q": ["Q", []],
        "w": ["W", []],
        "e": ["E", []],
        "r": ["R", []],
        "t": ["T", []],
        "y": ["Y", []],
        "u": ["U", []],
        "i": ["I", []],
        "o": ["O", []],
        "p": ["P", []],
        "`": ["LEFTBRACKET", []],
        "+": ["RIGHTBRACKET", []],
        
        # Top row (shifted)
        "Q": ["Q", ["LSHIFT"]],
        "W": ["W", ["LSHIFT"]],
        "E": ["E", ["LSHIFT"]],
        "R": ["R", ["LSHIFT"]],
        "T": ["T", ["LSHIFT"]],
        "Y": ["Y", ["LSHIFT"]],
        "U": ["U", ["LSHIFT"]],
        "I": ["I", ["LSHIFT"]],
        "O": ["O", ["LSHIFT"]],
        "P": ["P", ["LSHIFT"]],
        "^": ["LEFTBRACKET", ["LSHIFT"]],
        "*": ["RIGHTBRACKET", ["LSHIFT"]],
        
        # Home row (unshifted)
        "a": ["A", []],
        "s": ["S", []],
        "d": ["D", []],
        "f": ["F", []],
        "g": ["G", []],
        "h": ["H", []],
        "j": ["J", []],
        "k": ["K", []],
        "l": ["L", []],
        "ñ": ["SEMICOLON", []],
        "´": ["QUOTE", []],
        "ç": ["BACKSLASH", []],
        
        # Home row (shifted)
        "A": ["A", ["LSHIFT"]],
        "S": ["S", ["LSHIFT"]],
        "D": ["D", ["LSHIFT"]],
        "F": ["F", ["LSHIFT"]],
        "G": ["G", ["LSHIFT"]],
        "H": ["H", ["LSHIFT"]],
        "J": ["J", ["LSHIFT"]],
        "K": ["K", ["LSHIFT"]],
        "L": ["L", ["LSHIFT"]],
        "Ñ": ["SEMICOLON", ["LSHIFT"]],
        "¨": ["QUOTE", ["LSHIFT"]],
        "Ç": ["BACKSLASH", ["LSHIFT"]],
        
        # Bottom row (unshifted)
        "<": ["NON-US-BACKSLASH", []],
        "z": ["Z", []],
        "x": ["X", []],
        "c": ["C", []],
        "v": ["V", []],
        "b": ["B", []],
        "n": ["N", []],
        "m": ["M", []],
        ",": ["COMMA", []],
        ".": ["PERIOD", []],
        "-": ["SLASH", []],
        
        # Bottom row (shifted)
        ">": ["NON-US-BACKSLASH", ["LSHIFT"]],
        "Z": ["Z", ["LSHIFT"]],
        "X": ["X", ["LSHIFT"]],
        "C": ["C", ["LSHIFT"]],
        "V": ["V", ["LSHIFT"]],
        "B": ["B", ["LSHIFT"]],
        "N": ["N", ["LSHIFT"]],
        "M": ["M", ["LSHIFT"]],
        ";": ["COMMA", ["LSHIFT"]],
        ":": ["PERIOD", ["LSHIFT"]],
        "_": ["SLASH", ["LSHIFT"]],
        
        # AltGr combinations
        "\\": ["BACKQUOTE", ["RALT"]],
        "|": ["1", ["RALT"]],
        "@": ["2", ["RALT"]],
        "#": ["3", ["RALT"]],
        "~": ["4", ["RALT"]],
        "€": ["5", ["RALT"]],
        "¬": ["6", ["RALT"]],
        "[": ["LEFTBRACKET", ["RALT"]],
        "]": ["RIGHTBRACKET", ["RALT"]],
        "{": ["QUOTE", ["RALT"]],
        "}": ["BACKSLASH", ["RALT"]],

        # Accented vowels (common in Spanish)
        "á": ["A", ["RALT"]],
        "é": ["E", ["RALT"]],
        "í": ["I", ["RALT"]],
        "ó": ["O", ["RALT"]],
        "ú": ["U", ["RALT"]],
        "Á": ["A", ["RALT", "LSHIFT"]],
        "É": ["E", ["RALT", "LSHIFT"]],
        "Í": ["I", ["RALT", "LSHIFT"]],
        "Ó": ["O", ["RALT", "LSHIFT"]],
        "Ú": ["U", ["RALT", "LSHIFT"]],
    }


def get_italian_qwerty_layout() -> Dict[str, List]:
    """
    Italian QWERTY keyboard layout.
    Based on the standard Italian keyboard layout.
    """
    return {
        # Control characters
        "\r": [None, None],
        "\t": ["TAB", []],
        " ": ["SPACE", []],
        "\n": ["ENTER", []],
        
        # Numbers row (unshifted)
        "\\": ["BACKQUOTE", []],
        "1": ["1", []],
        "2": ["2", []],
        "3": ["3", []],
        "4": ["4", []],
        "5": ["5", []],
        "6": ["6", []],
        "7": ["7", []],
        "8": ["8", []],
        "9": ["9", []],
        "0": ["0", []],
        "'": ["MINUS", []],
        "ì": ["EQUALS", []],
        
        # Numbers row (shifted)
        "|": ["BACKQUOTE", ["LSHIFT"]],
        "!": ["1", ["LSHIFT"]],
        "\"": ["2", ["LSHIFT"]],
        "£": ["3", ["LSHIFT"]],
        "$": ["4", ["LSHIFT"]],
        "%": ["5", ["LSHIFT"]],
        "&": ["6", ["LSHIFT"]],
        "/": ["7", ["LSHIFT"]],
        "(": ["8", ["LSHIFT"]],
        ")": ["9", ["LSHIFT"]],
        "=": ["0", ["LSHIFT"]],
        "?": ["MINUS", ["LSHIFT"]],
        "^": ["EQUALS", ["LSHIFT"]],
        
        # Top row (unshifted)
        "q": ["Q", []],
        "w": ["W", []],
        "e": ["E", []],
        "r": ["R", []],
        "t": ["T", []],
        "y": ["Y", []],
        "u": ["U", []],
        "i": ["I", []],
        "o": ["O", []],
        "p": ["P", []],
        "è": ["LEFTBRACKET", []],
        "+": ["RIGHTBRACKET", []],
        "ù": ["BACKSLASH", []],
        
        # Top row (shifted)
        "Q": ["Q", ["LSHIFT"]],
        "W": ["W", ["LSHIFT"]],
        "E": ["E", ["LSHIFT"]],
        "R": ["R", ["LSHIFT"]],
        "T": ["T", ["LSHIFT"]],
        "Y": ["Y", ["LSHIFT"]],
        "U": ["U", ["LSHIFT"]],
        "I": ["I", ["LSHIFT"]],
        "O": ["O", ["LSHIFT"]],
        "P": ["P", ["LSHIFT"]],
        "é": ["LEFTBRACKET", ["LSHIFT"]],
        "*": ["RIGHTBRACKET", ["LSHIFT"]],
        "§": ["BACKSLASH", ["LSHIFT"]],
        
        # Home row (unshifted)
        "a": ["A", []],
        "s": ["S", []],
        "d": ["D", []],
        "f": ["F", []],
        "g": ["G", []],
        "h": ["H", []],
        "j": ["J", []],
        "k": ["K", []],
        "l": ["L", []],
        "ò": ["SEMICOLON", []],
        "à": ["QUOTE", []],
        
        # Home row (shifted)
        "A": ["A", ["LSHIFT"]],
        "S": ["S", ["LSHIFT"]],
        "D": ["D", ["LSHIFT"]],
        "F": ["F", ["LSHIFT"]],
        "G": ["G", ["LSHIFT"]],
        "H": ["H", ["LSHIFT"]],
        "J": ["J", ["LSHIFT"]],
        "K": ["K", ["LSHIFT"]],
        "L": ["L", ["LSHIFT"]],
        "ç": ["SEMICOLON", ["LSHIFT"]],
        "°": ["QUOTE", ["LSHIFT"]],
        
        # Bottom row (unshifted)
        "<": ["NON-US-BACKSLASH", []],
        "z": ["Z", []],
        "x": ["X", []],
        "c": ["C", []],
        "v": ["V", []],
        "b": ["B", []],
        "n": ["N", []],
        "m": ["M", []],
        ",": ["COMMA", []],
        ".": ["PERIOD", []],
        "-": ["SLASH", []],
        
        # Bottom row (shifted)
        ">": ["NON-US-BACKSLASH", ["LSHIFT"]],
        "Z": ["Z", ["LSHIFT"]],
        "X": ["X", ["LSHIFT"]],
        "C": ["C", ["LSHIFT"]],
        "V": ["V", ["LSHIFT"]],
        "B": ["B", ["LSHIFT"]],
        "N": ["N", ["LSHIFT"]],
        "M": ["M", ["LSHIFT"]],
        ";": ["COMMA", ["LSHIFT"]],
        ":": ["PERIOD", ["LSHIFT"]],
        "_": ["SLASH", ["LSHIFT"]],
        
        # AltGr combinations
        "@": ["QUOTE", ["RALT"]],
        "#": ["BACKSLASH", ["RALT"]],
        "€": ["5", ["RALT"]],
        "[": ["LEFTBRACKET", ["RALT"]],
        "]": ["RIGHTBRACKET", ["RALT"]],
        "{": ["7", ["RALT"]],
        "}": ["0", ["RALT"]],
    }


# Layout registry for easy access
LAYOUT_REGISTRY = {
    "fr_azerty": get_french_azerty_layout,
    "es_qwerty": get_spanish_qwerty_layout,
    "it_qwerty": get_italian_qwerty_layout,
}


def get_layout(layout_name: str) -> Dict[str, List]:
    """Get a specific layout by name."""
    if layout_name not in LAYOUT_REGISTRY:
        raise ValueError(f"Unknown layout: {layout_name}. Available: {list(LAYOUT_REGISTRY.keys())}")
    
    return LAYOUT_REGISTRY[layout_name]()


def list_available_layouts() -> List[str]:
    """List all available predefined layouts."""
    return list(LAYOUT_REGISTRY.keys())
