from pygments import highlight
from pygments.lexers import Python3Lexer
from pygments.formatters import HtmlFormatter
from pygments.formatters import Terminal256Formatter
from pygments.formatters import TerminalFormatter

# https://pygments.org/docs/formatters/

#code = 'print("Hello World")'

code = """
ans1 = "OK", df.select(
    "Type 1",
    "Type 2",
    pl.col("Attack").mean().over("Type 1").alias("avg_attack_by_type"),
    pl.col("Defense")
    .mean()
    .over(["Type 1", "Type 2"])
    .alias("avg_defense_by_type_combination"),
    pl.col("Attack").mean().alias("avg_attack"),
)
"""
#print(highlight(code, Python3Lexer(), HtmlFormatter()))
#print(highlight(code, Python3Lexer(), Terminal256Formatter()))
print(highlight(code, Python3Lexer(), TerminalFormatter()))
