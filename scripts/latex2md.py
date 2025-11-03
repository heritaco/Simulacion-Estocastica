"""
import pyperclip, latex2md
pyperclip.copy(latex2md.latex_to_markdown(pyperclip.paste()))
"""
import re
from typing import List

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
    if s.lstrip().startswith('---'):
        m = re.match(r"(?s)^\s*---\s*\n.*?\n---\s*\n", s)
        if m:
            s = s[m.end():]
    s = re.sub(r"(?m)^\s*---\s*$", "", s)
    return s

# ---------- [ … ] blocks to $$ … $$ ----------
def _convert_square_bracket_blocks(text: str) -> str:
    def repl(m):
        inner = m.group(1).strip("\n")
        return f"$$\n{inner}\n$$"
    text = re.sub(r"(?ms)^\s*\[\s*\n(.*?)\n\s*\]\s*$", repl, text)
    text = re.sub(r"(?m)^\s*\[\s*(.+?)\s*\]\s*$", lambda m: f"$$\n{m.group(1)}\n$$", text)
    return text

# ---------- Standard LaTeX math delimiters ----------
def _convert_standard_latex_delims(text: str) -> str:
    # \[ ... \] -> $$
    text = re.sub(r"(?s)\\\[\s*(.*?)\s*\\\]", r"$$\n\1\n$$", text)
    # \( ... \) -> $
    # FIXED: removed extra ')'
    text = re.sub(r"\\\((.+?)\\\)", r"$\1$", text, flags=re.S)
    # environments -> $$
    envs = [
        "equation", "equation*",
        "align", "align*",
        "gather", "gather*",
        "eqnarray", "eqnarray*",
        "displaymath"
    ]
    for env in envs:
        text = re.sub(
            rf"(?s)\\begin\{{{env}\}}\s*(.*?)\s*\\end\{{{env}\}}",
            r"$$\n\1\n$$",
            text,
        )
    return text

# ---------- De-size /left /right ----------
_SIZE_CMD = r"(?:big|Big|bigg|Bigg)(?:gl|gr|l|r)?"
def _desize_and_fix_big_delims(text: str) -> str:
    s = text
    s = re.sub(rf"\\{_SIZE_CMD}\s*\{{", "(", s)
    s = re.sub(rf"\\{_SIZE_CMD}\s*\}}", ")", s)
    s = re.sub(rf"\\{_SIZE_CMD}\s*\(", "(", s)
    s = re.sub(rf"\\{_SIZE_CMD}\s*\)", ")", s)
    s = re.sub(r"\\left\s*\(", "(", s)
    s = re.sub(r"\\right\s*\)", ")", s)
    s = re.sub(r"\\left\s*\{", "(", s)
    s = re.sub(r"\\right\s*\}", ")", s)
    return s

# ---------- Inline (…) -> $…$ heuristic ----------
_MATHY_HINT = re.compile(r"(\\[A-Za-z]+|[=<>^_]|\\{|\\}|\\left|\\right|\\frac|\d[A-Za-z]|[A-Za-z]\d)")
_ENGLISHISH = re.compile(r"\s(?<!\\|\{)[A-Za-zÁÉÍÓÚáéíóúñÑ]{2,}(?=\s|[.,;:)]|$)") 

def _convert_paren_inline_math_balanced(text: str) -> str:
    out = []
    i, n = 0, len(text)
    while i < n:
        ch = text[i]
        if ch != '(':
            out.append(ch); i += 1; continue
        depth, j, found = 0, i, -1
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

# ---------- LaTeX noise ----------
def _strip_latex_noise(text: str) -> str:
    s = text
    s = re.sub(r"\\label\{[^{}]*\}", "", s)
    s = re.sub(r"(^|[^\\])%.*?$", r"\1", s, flags=re.M)
    return s

# ---------- NEW: [npt] -> '\\' ----------
def _replace_pt_breaks(text: str) -> str:
    return re.sub(r"\[\s*\d+\s*pt\s*\]", r"\\\\", text, flags=re.I)

# ---------- NEW: clean math internals ----------
def _fix_math_internals(text: str) -> str:
    def fix(inner: str) -> str:
        s = inner

        s = re.sub(r"\s*;\s*([<>]=?)\s*;\s*", r" \1 ", s)         # '; < ;' -> '<'
        s = re.sub(r"\s*;\s*", " ", s)                            # remove lone ';'
        s = re.sub(r",\s*(?=[)\]])", "", s)                       # ',)' ',]' -> ')',']'
        s = re.sub(r",\s*(?=(?:d|\\mathrm\s*\{\s*d\s*\})\s*[A-Za-z])", " ", s)  # ',dx' -> ' dx'
        s = re.sub(r",\s*(?=\\[A-Za-z])", " ", s)                 # ',\cmd' -> '\cmd'
        s = re.sub(r"\+,\s*", "+ ", s)                            # '+,' -> '+ '

        s = re.sub(                                              # '\cmd!' -> '\cmd\!'
            r"(\\[A-Za-z]+)!(?=\s*(\(|\[|\\frac|\\left|\\right|\\Big|\\big|\\Bigg|\\bigg))",
            r"\1\\!", s)

        s = re.sub(r"!\s*(?=\\[A-Za-z])", "", s)                  # '!\cmd' -> '\cmd'
        s = re.sub(r"\s*!\s*-\s*!\s*", " - ", s)                  # '!-!' -> ' - '

        # NEW: remove spacing '!' before '(' or '[' (e.g., S_0!\left( -> S_0()
        s = re.sub(r"(?<=[\w}\]])\s*!\s*(?=[\(\[])", " ", s)

        s = re.sub(r"(?<![\w)])\s*!\s*(?=\S)", " ", s)            # other stray '!' spacing

        # drop comma before '('
        s = re.sub(r",\s*(?=\()", " ", s)

        # drop comma before a letter (variable)
        s = re.sub(r",\s*(?=[A-Za-z])", " ", s)


        return s

    def blk(m): return "$$\n" + fix(m.group(1)) + "\n$$"
    text = re.sub(r"(?s)\$\$\n?(.*?)\n?\$\$", blk, text)

    def inl(m): return "$" + fix(m.group(1)) + "$"
    text = re.sub(r"\$(.+?)\$", inl, text, flags=re.S)

    return text




def _normalize_ws(text: str) -> str:
    s = re.sub(r"[ \t]+\n", "\n", text)
    s = re.sub(r"\n{3,}", "\n\n", s)
    s = re.sub(r"[ \t]{2,}", " ", s)
    return s.strip() + "\n"

# ---------- Public API ----------
def latex_to_markdown(text: str) -> str:
    s = text
    s = _strip_triple_dash_and_frontmatter(s)
    s = _replace_pt_breaks(s)                 # [2pt] -> \\
    s = _convert_square_bracket_blocks(s)
    s = _convert_standard_latex_delims(s)     # <<< fixed here
    s = _desize_and_fix_big_delims(s)
    s, blks, inls = _protect_math(s)
    s = _convert_paren_inline_math_balanced(s)
    s = _restore_math(s, blks, inls)
    s = _strip_latex_noise(s)
    s = _fix_math_internals(s)
    s = _normalize_ws(s)
    # replace "# " with "## " to avoid top-level headers
    s = re.sub(r"(?m)^# ", "## ", s)
    return s
