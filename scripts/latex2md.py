"""
import pyperclip, latex2md
pyperclip.copy(latex2md.latex_to_markdown(pyperclip.paste()))
"""


import re
from typing import List, Tuple

__all__ = ["latex_to_markdown"]

# ---------- Protect / restore existing $…$ and $$…$$ ----------
def _protect_math(text: str):
    blocks: List[str] = []
    inlines: List[str] = []

    def _blk(m):
        blocks.append(m.group(0))
        return f"__MD_MATH_BLOCK_{len(blocks)-1}__"
    text = re.sub(r"\$\$(.*?)\$\$", _blk, text, flags=re.S)

    def _inl(m):
        inlines.append(m.group(0))
        return f"__MD_MATH_INLINE_{len(inlines)-1}__"
    text = re.sub(r"\$(.+?)\$", _inl, text, flags=re.S)

    return text, blocks, inlines

def _restore_math(text: str, blocks: List[str], inlines: List[str]) -> str:
    for i, s in enumerate(inlines):
        text = text.replace(f"__MD_MATH_INLINE_{i}__", s)
    for i, s in enumerate(blocks):
        text = text.replace(f"__MD_MATH_BLOCK_{i}__", s)
    return text

# ---------- Remove '---' and YAML front matter ----------
def _strip_triple_dash_and_frontmatter(text: str) -> str:
    s = text
    # YAML front matter at top
    if s.lstrip().startswith('---'):
        m = re.match(r"(?s)^\s*---\s*\n.*?\n---\s*\n", s)
        if m:
            s = s[m.end():]
    # Standalone '---' lines anywhere
    s = re.sub(r"(?m)^\s*---\s*$", "", s)
    return s

# ---------- [ … ] blocks to $$ … $$ ----------
def _convert_square_bracket_blocks(text: str) -> str:
    def repl(m):
        inner = m.group(1).strip("\n")
        return f"$$\n{inner}\n$$"
    # Multiline [ ... ] with optional indentation
    text = re.sub(r"(?ms)^\s*\[\s*\n(.*?)\n\s*\]\s*$", repl, text)
    # Single-line [ ... ]
    text = re.sub(r"(?m)^\s*\[\s*(.+?)\s*\]\s*$", lambda m: f"$$\n{m.group(1)}\n$$", text)
    return text

# ---------- Standard LaTeX math delimiters ----------
def _convert_standard_latex_delims(text: str) -> str:
    # \[...\] -> $$...$$
    text = re.sub(r"(?s)\\\[\s*(.*?)\s*\\\]", r"$$\n\1\n$$", text)
    # \(...\) -> $...$
    text = re.sub(r"\\\((.+?)\\\)", r"$\1$", text, flags=re.S)
    # Common display environments -> $$...$$
    envs = ["equation", "equation*", "align", "align*", "gather", "gather*", "eqnarray", "eqnarray*", "displaymath"]
    for env in envs:
        text = re.sub(rf"(?s)\\begin\{{{env}\}}\s*(.*?)\s*\\end\{{{env}\}}", r"$$\n\1\n$$", text)
    return text

# ---------- De-size \big, \Big, \bigl, \Bigr, etc. and map to '(' / ')' ----------
_SIZE_CMD = r"(?:big|Big|bigg|Bigg)(?:gl|gr|l|r)?"
def _desize_and_fix_big_delims(text: str) -> str:
    s = text
    # Map size macros on braces to parentheses
    s = re.sub(rf"\\{_SIZE_CMD}\s*\{{", "(", s)
    s = re.sub(rf"\\{_SIZE_CMD}\s*\}}", ")", s)
    # Map size macros on real parens
    s = re.sub(rf"\\{_SIZE_CMD}\s*\(", "(", s)
    s = re.sub(rf"\\{_SIZE_CMD}\s*\)", ")", s)
    # \left / \right pairs
    s = re.sub(r"\\left\s*\(", "(", s)
    s = re.sub(r"\\right\s*\)", ")", s)
    # Optionally normalize curly to round as requested
    s = re.sub(r"\\left\s*\{", "(", s)
    s = re.sub(r"\\right\s*\}", ")", s)
    return s

# ---------- Heuristic: inline math in (…) ----------
_MATHY_HINT = re.compile(r"(\\[A-Za-z]+|[=<>^_]|\\{|\\}|\\left|\\right|\\frac|\d[A-Za-z]|[A-Za-z]\d)")
_ENGLISHISH = re.compile(r"\s(?<!\\|\{)[A-Za-zÁÉÍÓÚáéíóúñÑ]{2,}(?=\s|[.,;:)]|$)")

def _convert_paren_inline_math_balanced(text: str) -> str:
    out = []
    i, n = 0, len(text)
    while i < n:
        ch = text[i]
        if ch != '(':
            out.append(ch); i += 1; continue
        # find matching ')'
        depth = 0
        j = i
        found = -1
        while j < n:
            cj = text[j]
            if cj == '(':
                depth += 1
            elif cj == ')':
                depth -= 1
                if depth == 0:
                    found = j
                    break
            if cj == '\n' and depth == 1 and j > i:
                break
            j += 1
        if found == -1:
            out.append(ch); i += 1; continue
        inner = text[i+1:found]
        if ('$' not in inner) and _MATHY_HINT.search(inner) and not _ENGLISHISH.search(inner):
            out.append('$'); out.append(inner); out.append('$')
        else:
            out.append('('); out.append(inner); out.append(')')
        i = found + 1
    return ''.join(out)

# ---------- Light cleanup and normalization ----------
def _strip_latex_noise(text: str) -> str:
    s = text
    s = re.sub(r"\\label\{[^{}]*\}", "", s)
    s = re.sub(r"(^|[^\\])%.*?$", r"\1", s, flags=re.M)
    return s

def _cleanup_math_minor(text: str) -> str:
    # Fix misplaced '!' after commands when followed by sizing or left/right
    def fix_inside(s: str) -> str:
        return re.sub(r"(?<=\\[A-Za-z])!(?=\\(Big|big|left|right))", r"\\!", s)
    def blk(m):
        inner = m.group(1)
        return "$$\n" + fix_inside(inner) + "\n$$"
    s = re.sub(r"(?s)\$\$\n?(.*?)\n?\$\$", blk, text)
    def inl(m):
        inner = m.group(1)
        return "$" + fix_inside(inner) + "$"
    s = re.sub(r"\$(.+?)\$", inl, s, flags=re.S)
    return s

def _normalize_ws(text: str) -> str:
    s = re.sub(r"[ \t]+\n", "\n", text)
    s = re.sub(r"\n{3,}", "\n\n", s)
    return s.strip() + "\n"

# ---------- Public API ----------
def latex_to_markdown(text: str) -> str:
    s = text
    s = _strip_triple_dash_and_frontmatter(s)   # remove --- and YAML front matter
    s = _convert_square_bracket_blocks(s)       # [ … ] blocks -> $$ … $$
    s = _convert_standard_latex_delims(s)       # \[ \], \(...\), environments
    s = _desize_and_fix_big_delims(s)           # \bigl{, \Big(, \left{ … -> ( and ) 
    s, blks, inls = _protect_math(s)            # protect existing $ / $$ 
    s = _convert_paren_inline_math_balanced(s)  # inline (…) -> $…$ when math-like
    s = _restore_math(s, blks, inls)
    s = _strip_latex_noise(s)
    s = _cleanup_math_minor(s)
    s = _normalize_ws(s)
    return s
