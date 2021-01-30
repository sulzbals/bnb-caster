class Actor():
  def __init__(self, value, idx):
    self.value = value
    self.idx = idx

    self.groups = set()

  def addGroup(self, group):
    self.groups.add(group)


class Node():
  def __init__(self, idx, cost, candidates, cast, represented, num_roles):
    self.idx = idx                           # Índice do candidato
    self.cost = cost                         # Custo acumulado da árvore
    try:
      self.candidate = candidates[0]         # Candidato representado
      self.next_candidates = candidates[1:]  # Próximos candidatos na fila
    except IndexError:
      self.candidate = None                  # Candidato representado
      self.next_candidates = []              # Próximos candidatos na fila
    self.cast = cast                         # Candidatos elencados
    self.represented = represented           # Grupos representados
    self.num_roles = num_roles               # Número de vagas totais

  def lazy_bound(self):
    # Retorna o custo acumulado na raiz da subárvore:
    return self.cost

  def greedy_bound(self):
    # Simula o elenco menos custoso possível:
    sim_cast = self.next_candidates[:self.num_roles-len(self.cast)]

    # Retorna o menor custo possível da subárvore:
    return self.cost + sum(candidate.value for candidate in sim_cast)

  # Greedy Bound é a função padrão:
  bound = lazy_bound

  def branch(self):
    # Se o elenco até o momento é menor do que o número de vagas, novos
    # candidatos podem ser elencados (BRANCH IN):
    if len(self.cast) < self.num_roles:
      yield Node(
        self.idx + 1,
        self.cost + self.candidate.value,
        self.next_candidates,
        self.cast + [self.candidate],
        self.represented | self.candidate.groups,
        self.num_roles
      )

    # Se o número de vagas não preenchidas é menor do que o número de candidatos
    # restantes, novos candidatos podem ser rejeitados (BRANCH OUT):
    if self.num_roles - len(self.cast) < len(self.next_candidates) + 1:
      yield Node(
        self.idx + 1,
        self.cost,
        self.next_candidates,
        self.cast,
        self.represented,
        self.num_roles
      )

  def __str__(self):
    try:
      return "({}/{}) Custo: {}, Grupos: {}".format(
        self.idx,
        self.candidate.idx,
        self.cost,
        self.represented
      )
    except AttributeError:
      return "({}) Custo: {}, Grupos: {}".format(
        self.idx,
        self.cost,
        self.represented
      )


class Tree():
  def __init__(self, candidates, num_roles):
    self.candidates = candidates  # Candidatos
    self.num_roles = num_roles    # Número de vagas

    # Estrutura de fila (lista) para emular a árvore:
    self.queue = [
      # Nó raiz:
      Node(
        0,
        0,
        self.candidates,
        [],
        set(),
        self.num_roles
      )
    ]

  def push(self, node):
    self.queue.insert(0, node)

  def pop(self):
    return self.queue.pop(0)

  def isEmpty(self):
    return not self.queue


class CastingProblem():
  def __init__(self, candidates, groups, num_roles):
    self.candidates = candidates  # Candidatos
    self.groups = groups          # Grupos
    self.num_roles = num_roles    # Número de vagas

    # Custo mínimo (ótimo) inicializado com valor não plausível:
    self.min_cost = sum([candidate.value for candidate in self.candidates]) + 1

    # Ordena os candidatos por valor (custo):
    self.candidates.sort(key=lambda candidate: candidate.value)

    # Lista de candidatos elencados
    self.cast = []

    # Árvore a ser construída:
    self.tree = Tree(self.candidates, self.num_roles)

  def solve(self):
    while not self.tree.isEmpty():
      # Percorre o próximo nó:
      node = self.tree.pop()

      # Se é um nó folha, pode ser uma solução:
      if node.idx >= len(self.candidates):
        # Se todas as vagas foram preenchidas e todos os grupos foram
        # representados, é uma solução plausível:
        if len(node.cast) == self.num_roles and node.represented == self.groups:
          # Se a solução (custo) atual é melhor que a solução ótima até então,
          # esta é a nova solução ótima:
          if node.cost < self.min_cost:
            self.cast = node.cast
            self.min_cost = node.cost
      else:
        # Obtém valor da função bound:
        bound = node.bound()

        # Se a subárvore a ser construída tem potencial de resultar em uma
        # solução melhor:
        if bound < self.min_cost:
          for branched_node in list(node.branch()):
            self.tree.push(branched_node)

    return self.cast, self.min_cost