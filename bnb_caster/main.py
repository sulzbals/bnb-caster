import os
import sys

from bnb_caster.struct import Actor
from bnb_caster.model import CastingProblem

class InvalidInput(Exception):
  '''
  Exceção de entrada inválida
  '''
  def __init__(self, message, fp=sys.stderr):
    # Escreve mensagem de erro no respectivo arquivo (STDERR por padrão):
    fp.write("Entrada inválida: " + message + "\n")

    # Encerra programa:
    quit()


class Line:
  '''
  Linha de entrada/saída
  '''
  def __init__(self):
    self.content = []

  @staticmethod
  def fromString(string):
    '''
    Instancia uma linha dada uma string
    '''
    this = Line()
    this.content = string.split(' ')
    return this

  @staticmethod
  def fromInt(num):
    '''
    Instancia uma linha dado um inteiro ou um conjunto de inteiros
    '''
    this = Line()

    try:
      for n in num:
        this.addInt(n)
    except TypeError:
      this.addInt(num)

    return this

  @staticmethod
  def fromFLoat(flt):
    '''
    Instancia uma linha dado um float ou um conjunto de floats
    '''
    this = Line()

    try:
      for num in flt:
        this.addFloat(num)
    except TypeError:
      this.addFloat(flt)

    return this

  def __len__(self):
    '''
    Definimos tamanho da linha como o número de elementos numéricos dela
    '''
    return len(self.content)

  def __str__(self):
    '''
    Conversão da linha para string (elementos separados por espaço + newline)
    '''
    return " ".join(self.content) + "\n"

  def toInt(self):
    '''
    Conversão da linha para int ou conjunto de ints
    '''
    if len(self) > 1:
      return [int(elm) for elm in self.content]
    else:
      return (int(self.content.pop()))

  def addInt(self, num):
    '''
    Adiciona um inteiro à linha
    '''
    self.content.append("%d" % num)

  def addFloat(self, num):
    '''
    Adiciona um float à linha
    '''
    self.content.append("%.1f" % num)


class Parser:
  '''
  Leitor da entrada do problema
  '''
  def __init__(self, fp=sys.stdin):
    self.fp = fp

  def parse(self):
    '''
    Lê a entrada (STDIN por padrão) linha por linha
    '''
    self.content = self.fp.read()
    self.lines = [Line.fromString(line) for line in self.content.splitlines()]

  def getLine(self, count):
    '''
    Acessa a próxima linha e verifica se o número de valores contidos nela é
    válido
    '''
    try:
      line = self.lines.pop(0)
    except IndexError:
      raise InvalidInput("Fim do arquivo inesperado")

    if len(line) != count:
      raise InvalidInput(
        "%d valor(es) esperado(s) na linha, %d recebido(s)" % (count, len(line))
      )

    return line


class Writer:
  '''
  Escritor da saída do problema
  '''
  def __init__(self, fp=sys.stdout):
    self.fp = fp

  def writeLine(self, line):
    '''
    Escreve uma linha na saída (STDOUT por padrão)
    '''
    self.fp.write(str(line))


def main():
  # Faz o parsing da entrada:
  parser = Parser()
  parser.parse()

  # Lê o número de grupos (l), atores (m) e personagens (n):
  l, m, n = parser.getLine(3).toInt()

  actors = []
  groups = set(range(1, l+1))

  # Para cada ator [1..m]:
  for idx in range(m):
    # Lê valor cobrado pelo ator (v) e número de grupos que faz parte (s):
    v, s = parser.getLine(2).toInt()

    # Instancia novo ator:
    actor = Actor(v, idx)

    # Salva ator:
    actors.append(actor)
  
    # Para cada grupo [1..s]:
    for _ in range(s):
      # Lê índice do grupo que o ator faz parte:
      actor.addGroup(parser.getLine(1).toInt())

  # Se a função bound secundária é selecionada:
  if "-a" in sys.argv[1:]:
    # Troca função bound default (Greedy Bound) para Lazy Bound:
    problem = CastingProblem(actors, groups, n, "Lazy Bound")
  else:
    # Usa Greedy Bound (default):
    problem = CastingProblem(actors, groups, n, "Greedy Bound")

  cast, cost, count, time = problem.solve()

  cast.sort(key=lambda actor: actor.idx)

  writer = Writer()

  if cast:
    line = Line()

    for actor in cast:
      line.addInt(actor.idx + 1)

    writer.writeLine(line)
    writer.writeLine(Line.fromInt(cost))
  else:
    writer.writeLine(Line.fromString("Inviável"))

  errWriter = Writer(fp=sys.stderr)

  errWriter.writeLine(
    Line.fromString(
      "Nós percorridos: %d/%d" % (count, 2**(m + 1) - 1)
    )
  )
  errWriter.writeLine(Line.fromString("Tempo: %f ms" % (time * 1000)))