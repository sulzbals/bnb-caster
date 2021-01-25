class Actor():
  def __init__(self, value, idx):
    self.value = value
    self.idx = idx
    self.groups = []

  def appendGroup(self, group):
    self.groups.append(group)

  def __str__(self):
    return "Actor Object (Value: {}, Groups: {}, Index: {})".format(
      self.value,
      self.groups,
      self.idx
    )


class Node():
  def __init__(self, actor, cost, rejections, cast, represented, idx):
    self.actor = actor
    self.cost = cost
    self.rejections = rejections
    self.cast = cast
    self.represented = represented
    self.idx = idx

  @staticmethod
  def root(actor):
    return Node(
      actor,      # Primeiro ator da fila
      0,          # Custo inicial é nulo
      0,          # Nenhuma rejeição
      [],         # Nenhum ator elencado
      [],         # Nenhum grupo representado
      0           # Índice (nível) 0
    )

  def bound(self, next_actors, num_characters):
    # Extrai valores dos próximos candidatos:
    values = [actor.value for actor in next_actors]

    # Obtém a combinação de elenco de menor custo (independente da solução):
    values = values[:num_characters - len(self.cast)]

    # Retorna o menor custo possível dentro da subárvore:
    return self.cost + sum(values)

  def branch(self, next_actor, num_characters, num_rejections, num_actors):
    # Se o elenco até o momento é menor do que o número de personagens:
    if len(self.cast) < num_characters:
      yield Node(
        next_actor,
        self.cost + self.actor.value,
        self.rejections,
        self.cast + [self.actor],
        list(set(self.represented) | set(self.actor.groups)),
        self.idx + 1
      )

    # Se ainda não foram feitas o máximo de rejeições:
    if self.rejections < num_rejections:
      yield Node(
        next_actor,
        self.cost,
        self.rejections + 1,
        self.cast,
        self.represented,
        self.idx + 1
      )


class CastingProblem():
  def __init__(self, actors, characters, groups):
    self.actors = actors
    self.characters = characters
    self.groups = set(groups)

    self.num_actors = len(actors)
    self.num_characters = len(characters)
    self.num_rejections = len(actors) - len(characters)
    self.min_cost = sum([actor.value for actor in actors]) + 1
    self.cast = []

    self.actors.sort(key=lambda actor: actor.value)

    self.tree = []

  def solve(self):
    self.tree.append(Node.root(self.actors[0]))

    while self.tree:
      node = self.tree.pop(0)

      # Se é um nó folha:
      if node.idx >= self.num_actors:
        # Se todos os grupos foram representados:
        if set(node.represented) == self.groups:
          # Se o custo da combinação atual é menor que o menor custo até então:
          if node.cost < self.min_cost:
            self.cast = node.cast
            self.min_cost = node.cost
      else:
        # Obtém bound:
        bound = node.bound(
          self.actors[:node.idx + 1],
          self.num_characters
        )

        if bound < self.min_cost:
          try:
            actor = self.actors[node.idx + 1]
          except IndexError:
            actor = None

          self.tree = list(
            node.branch(
              actor,
              self.num_characters,
              self.num_rejections,
              self.num_actors
            )
          ) + self.tree

    return self.cast, self.min_cost